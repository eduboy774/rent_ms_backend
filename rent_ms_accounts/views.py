import graphene
from graphene_federation import build_schema
from graphql import GraphQLError
from rent_ms_backend.decorators.Permission import has_mutation_access

from rent_ms_dto.Enum import GenderTypeInum, ProfileLevelInum, UserProfileInum
from rent_ms_dto.UserAccounts import  *
from rent_ms_dto.Response import ResponseObject
from django.contrib.auth.models import User
from rent_ms_accounts.models import *
from rent_ms_builders.UserAccountsBuilders import UserAccountBuilder
from rent_ms_uaa.models import *
from rent_ms_utils.EmailUtils import EmailNotifications
from rent_ms_utils.UserUtils import UserUtils
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from dotenv import dotenv_values

config = dotenv_values(".env")

class CreateUsersMutation(graphene.Mutation):
    class Arguments:
        input = UserInputObject(required=True)
        

    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileAndRoleObjects) 

    @classmethod
    # @has_mutation_access(permissions=['can_manage_settings'])
    def mutate(self, root, info,  input):
      if User.objects.filter(username=input.user_email).first():
        return self(response=ResponseObject.get_response(id="4"))

      else:   
            user = User.objects.create(
                first_name=input.user_first_name,
                last_name=input.user_last_name,
                username=input.user_email,
                email=input.user_email,
            )

            user_profile = UsersProfiles.objects.create(
                profile_type=input.profile_type.value,
                profile_phone=input.profile_phone,
                profile_title=input.profile_title,
                profile_level=input.profile_level.value,
                profile_gender=input.profile_gender.value,
                profile_user=user
            )
  
            if input.role_unique_id is not None:
                UsersWithRoles.objects.create(
                    user_with_role_role = UserRoles.objects.filter(role_unique_id=input.role_unique_id).first(),
                    user_with_role_user=user
                )
                
            response_body = UserAccountBuilder.get_user_profile_and_role_data(id=user_profile.profile_unique_id)
            return self(response=ResponseObject.get_response(id="1"), data=response_body)
      
class CreateMyAccountMutation(graphene.Mutation):
    class Arguments:
        input = UserAcountInputObject(required=True)
    response = graphene.Field(ResponseObject)
    data = graphene.Field(UsersResponseObject) 

    @classmethod
    def mutate(self, root, info,  input):
      
      # Validate email format
        try:
            validate_email(input.user_email)
            is_valid_format = True
        except ValidationError:
            is_valid_format = False
            return self(response=ResponseObject.get_response(id="7"),data=[])

        if  is_valid_format and User.objects.filter(username=input.user_email,email=input.user_email).exists():
            return self(response=ResponseObject.get_response(id="4"),data=[])
        
        elif is_valid_format:   
             user = User.objects.create(
                    first_name=input.user_first_name,
                    last_name=input.user_last_name,
                    username=input.user_email,
                    email=input.user_email,
                )
             user.set_password(input.password)
             user.save()

        UsersProfiles.objects.create(
                profile_phone=input.profile_phone,
                profile_title=input.profile_title,
                profile_type = UserUtils.get_enum_value(UserProfileInum, input.profile_type or 'NORMAL_PROFILE'),
                profile_level = UserUtils.get_enum_value(ProfileLevelInum, input.profile_level or 'REGION'),
                profile_gender = UserUtils.get_enum_value(GenderTypeInum, input.profile_gender or 'NONE'),
                profile_user=user
            )
  
        if input.role_unique_id is not None:
                UsersWithRoles.objects.create(
                    user_with_role_role = UserRoles.objects.filter(role_unique_id=input.role_unique_id).first(),
                    user_with_role_user=user
                )

        response_body = UserAccountBuilder.get_user_data(id=user.id)
        print(response_body)
        return self(response=ResponseObject.get_response(id="8"), data=None)     

class UpdateUsersMutation(graphene.Mutation):
    class Arguments:
        input = UserInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileAndRoleObjects)

    @classmethod
    # @has_mutation_access(permissions=['can_manage_settings'])
    def mutate(self, root, info,  input):
        profile = UsersProfiles.objects.filter(profile_is_active=True, profile_unique_id=input.profile_unique_id).first()
        if profile is None:
            return self(response=ResponseObject.get_response(id="5"), data=None)
        
        try:
            profile.profile_phone = input.profile_phone
            profile.profile_title = input.profile_title
            profile.profile_photo = input.profile_photo
            # 
            profile.profile_type = UserUtils.get_enum_value(UserProfileInum, input.profile_type)
            profile.profile_level = UserUtils.get_enum_value(ProfileLevelInum, input.profile_level or 'REGION')
            profile.profile_gender = UserUtils.get_enum_value(GenderTypeInum, input.profile_gender)
            profile.save()

            profile.profile_user.first_name = input.user_first_name
            profile.profile_user.last_name = input.user_last_name
            profile.profile_user.email = input.user_email
            profile.profile_user.save()

            if input.role_unique_id is not None:
                user_with_role = UsersWithRoles.objects.filter(user_with_role_role__role_unique_id=input.role_unique_id).first()
                user_with_role.user_with_role_role = UserRoles.objects.filter(role_unique_id=input.role_unique_id).first()
                user_with_role.save()
            
            response_body = UserAccountBuilder.get_user_profile_and_role_data(id=profile.profile_unique_id)
            return self(response=ResponseObject.get_response(id="1"), data=response_body)
        except Exception as e:
            print('Exception While Updating User',e)
            return self(response=ResponseObject.get_response(id="6"), data=[])

    
class DeleteUsersMutation(graphene.Mutation):
    class Arguments:
        profile_unique_id = graphene.String(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    # @has_mutation_access(permissions=['can_manage_settings'])
    def mutate(self, root, info,  profile_unique_id):

        admin_profile = UsersProfiles.objects.filter(profile_unique_id=profile_unique_id).first()
        admin_profile.profile_is_active = False
        admin_profile.save()
        admin_profile.profile_user.is_active = False
        admin_profile.profile_user.save()

        return self(response=ResponseObject.get_response(id="1"))

class UpdateMyProfileMutation(graphene.Mutation):
    class Arguments:
        input = UserInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileObject)

    @classmethod
    def mutate(self, root, info,  input):

        profile = UsersProfiles.objects.filter(profile_unique_id=input.profile_unique_id, profile_is_active=True).first()

        if profile is None:
            return self(response=ResponseObject.get_response(id="6"), data=None)

        profile.profile_phone = input.profile_phone
        profile.profile_title = input.profile_title
        profile.profile_photo = input.profile_photo
        # 
        profile.profile_type = UserUtils.get_enum_value(UserProfileInum, input.profile_type)
        profile.profile_level = UserUtils.get_enum_value(ProfileLevelInum, input.profile_level or 'REGION')
        profile.profile_gender = UserUtils.get_enum_value(GenderTypeInum, input.profile_gender)
        # 
        profile.save()

        profile.profile_user.first_name = input.user_first_name
        profile.profile_user.last_name = input.user_last_name
        profile.profile_user.email = input.user_email
        profile.profile_user.save()


        response_body = UserAccountBuilder.get_user_profile_data(id=profile.profile_unique_id)

        return self(response=ResponseObject.get_response(id="1"), data=response_body)


class ForgotPasswordMutation(graphene.Mutation):
    class Arguments:
        user_email = graphene.String(required=True)
    
    response = graphene.Field(ResponseObject)
    
    @classmethod
    # @has_mutation_access(permissions=['can_manage_settings'])
    def mutate(self, root, info,  user_email):
        try:
            user = User.objects.filter(username = user_email ).first()
            if user is None:
                return self(response=ResponseObject.get_response(id="3"))
            
            request_token = UserUtils.get_forgot_password_token()
           
            ForgotPasswordRequestUsers.objects.create(
                request_user = user,
                request_token = request_token
            )

            url = config['FRONTEND_DOMAIN'] + f"password-reset/{request_token}/"

            body = {
                'receiver_details': user.email,
                'user': user,
                'url': url,
                'subject': "Vilcom Password Reset"
            }

            EmailNotifications.send_email_notification(body, 'password_reset.html')


            return self(response=ResponseObject.get_response(id="1"))
        except Exception as e:
            return self(response=ResponseObject.get_response(id="5"))

class ChangeUserPasswordMutation(graphene.Mutation):
    class Arguments:
        input = ForgortPasswordFilteringInputObject(required=True)

    response = graphene.Field(ResponseObject)
    @classmethod
    def mutate(self, root, info,  input):

        profile_unique_id = UserUtils.__profile__(info.context.headers)

        user = UsersProfiles.objects.filter(profile_unique_id=profile_unique_id, profile_is_active=True).first()

        if not authenticate(username=user.profile_user.username, password=input.old_password):
            return self(response=ResponseObject.get_response(id="16"))

        user.profile_user.set_password(input.new_password)
        user.profile_user.save()

        return self(response=ResponseObject.get_response(id="1"))




class Mutation(graphene.ObjectType):
    create_users_mutation = CreateUsersMutation.Field()
    create_my_account_mutation= CreateMyAccountMutation().Field()
    update_users_mutation = UpdateUsersMutation.Field()
    delete_users_mutation = DeleteUsersMutation.Field()
    
    update_user_profile_mutation = UpdateUsersMutation.Field()
    update_my_profile_mutation = UpdateMyProfileMutation.Field()
    forgot_password_mutation = ForgotPasswordMutation.Field()
    change_user_password_mutation = ChangeUserPasswordMutation.Field()


schema = build_schema(Mutation, types=[])

