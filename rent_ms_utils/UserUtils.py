from graphql import GraphQLError
from rest_framework.permissions import IsAuthenticated
from rent_ms_uaa.models import UsersWithRoles
from rent_ms_accounts.models import UsersProfiles
from .BearerTokenAuthentication import BearerTokenAuthentication
from rent_ms_builders.UAABuilder import UAABuilder 
import uuid


class UserUtils:
    
    def get_user(request):
        is_authenticated, user = BearerTokenAuthentication.authenticate(request)
        profile=UsersProfiles.objects.filter(profile_user=user).first()
        user_data={
            'profile_unique_id':str(profile.profile_unique_id),
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'email':user.email,
            'user_permissions':UserUtils.get_user_permissions(user),
            'user_type':profile.profile_type,
            "profile_phone":profile.profile_phone
        }      
        
        return user_data
      
    def __profile__(request):
        user_data = UserUtils.get_user(request)
        return user_data['profile_unique_id']
    
    def get_user_permissions(user):
        user_with_role= UsersWithRoles.objects.filter(user_with_role_user=user).first()
        if not user_with_role:
            return []
        user_roles = UAABuilder.get_role_data(id=user_with_role.user_with_role_role.role_unique_id)
        user_permissions =[]
        for permission in user_roles.role_permissions:
            user_permissions.append(permission.permission_code)
        return user_permissions
    
    
    
    def get_forgot_password_token():
        token =  str(uuid.uuid4())
        return token
    
    # 
    def get_enum_value(enum_class, value):
        if isinstance(value, enum_class):
            return value.value
        elif isinstance(value, str):
            try:
                return enum_class[value].value
            except KeyError:
                raise GraphQLError(f"Invalid enum value provided: {value}")
        return None

    