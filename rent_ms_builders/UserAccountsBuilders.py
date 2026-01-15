from rent_ms_accounts.models import *
from rent_ms_dto.UserAccounts import *
from rent_ms_builders.UAABuilder import UAABuilder
from rent_ms_uaa.models import *


class UserAccountBuilder:
    def get_user_profile_data(id):
        try: 
            user_profile=UsersProfiles.objects.filter(profile_unique_id=id).first()
            
            return UserProfileObject(
                id = user_profile.id,
                profile_unique_id = user_profile.profile_unique_id,
                user_first_name = user_profile.profile_user.first_name,
                user_last_name = user_profile.profile_user.last_name,
                user_email = user_profile.profile_user.email,
                profile_phone = user_profile.profile_phone,
                profile_title = user_profile.profile_title,
                profile_photo = user_profile.profile_photo,
                profile_is_active = user_profile.profile_is_active,
                profile_type = user_profile.profile_type,
                profile_level = user_profile.profile_level,
                profile_gender = user_profile.profile_gender
            )
        except Exception as e:
            print(e)
            return UserProfileObject()
        

    def get_user_profile_and_role_data(id):
     
            user_profile=UsersProfiles.objects.filter(profile_is_active=True,profile_unique_id=id).first()
            user_with_role= UsersWithRoles.objects.filter(user_with_role_user=user_profile.profile_user).first()

            roles = UsersWithRoles.objects.filter(user_with_role_user=user_profile.profile_user).values('user_with_role_role__role_unique_id')
            roles_list = list(map(lambda x: UAABuilder.get_role_data(str(x['user_with_role_role__role_unique_id'])), roles))
            
            return UserProfileAndRoleObjects(
                id = user_profile.id,
                user_profile = UserAccountBuilder.get_user_profile_data(user_profile.profile_unique_id),
                user_roles = roles_list,
            )
           
        

    def get_user_data(id):
        try:
            user=User.objects.filter(is_active=True,id=id).first()
            return UserProfileObjects(
                id=user.id,
                user_first_name = user.first_name,
                user_last_name = user.last_name,
                user_email = user.email,
                password = user.password,
            )
        except Exception as e:
            print(e)
            return UserProfileObjects()
        
        



