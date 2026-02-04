import graphene
from .Uaa import UserRoleObjects
from .Response import  PageObject, ResponseObject
from .Enum import GenderEnum, ProfileLevelEnum, UserProfileEnum


class UserInputObject(graphene.InputObjectType):
    profile_unique_id = graphene.String()
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    profile_phone = graphene.String()
    profile_title = graphene.String()
    profile_photo = graphene.String()
    profile_gender = GenderEnum()
    profile_type = UserProfileEnum()
    profile_level = ProfileLevelEnum()
    role_unique_id = graphene.String()
    password = graphene.String()


class UserAcountInputObject(graphene.InputObjectType):
    profile_unique_id = graphene.String()
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    password = graphene.String()    
    profile_gender = GenderEnum()
    profile_type = UserProfileEnum()
    profile_level = ProfileLevelEnum()
    role_unique_id = graphene.String()
    profile_phone = graphene.String()
    profile_title = graphene.String()



class UserProfileObject(graphene.ObjectType):
    id = graphene.String()
    profile_unique_id = graphene.String()
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    profile_phone = graphene.String()
    profile_title = graphene.String()
    profile_photo = graphene.String()
    profile_is_active = graphene.Boolean()
    profile_type = UserProfileEnum()
    profile_level = ProfileLevelEnum()
    profile_gender = GenderEnum()

class ProfileResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.List(UserProfileObject)

class UserFilteringInputObject(graphene.InputObjectType):
    profile_type = UserProfileEnum()
    profile_is_active = graphene.Boolean()
    page_number = graphene.Int(required=True)
    profile_unique_id = graphene.String()


class UserProfileAndRoleObjects(graphene.ObjectType):
    id = graphene.String()
    user_profile = graphene.Field(UserProfileObject)
    user_roles = graphene.List(UserRoleObjects)
    
class UserProfileObjects(graphene.ObjectType):
    id = graphene.String()
    profile_unique_id = graphene.String()
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    password = graphene.String() 
    profile_phone = graphene.String()
    profile_title = graphene.String()
    profile_photo = graphene.String()
    profile_is_active = graphene.Boolean()
    profile_type = UserProfileEnum()
    profile_level = ProfileLevelEnum()
    profile_gender = GenderEnum()   


class UserProfileAndRoleResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileAndRoleObjects)

class UsersAndRoleResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.List(UserProfileAndRoleObjects)
    page = graphene.Field(PageObject)

class UsersResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.List(UserProfileObjects) 
    page = graphene.Field(PageObject)

class SetPasswordFilteringInputObject(graphene.InputObjectType):
    request_token = graphene.String()
    user_password = graphene.String()

class ForgortPasswordFilteringInputObject(graphene.InputObjectType):
    old_password = graphene.String()
    new_password = graphene.String()

class ActivateDeactivateFilteringInputObject(graphene.InputObjectType):
    profile_unique_id = graphene.String()
    profile_is_active = graphene.Boolean()
