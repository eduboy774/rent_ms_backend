import graphene
import base64
from graphene import ObjectType
from rent_ms_backend.decorators.Permission import has_query_access
from rent_ms_dto.Uaa import UserRoleResponseObject, UserRolesFilteringInputObjects, GroupedPermissionsResponseObject, PermisionFilteringInputObjects
from rent_ms_dto.Response import ResponseObject
from rent_ms_uaa.models import UserRoles, UserPermissionsGroup
from rent_ms_builders.UAABuilder import UAABuilder
from django.template.loader import render_to_string

class Query(ObjectType): 
    get_roles = graphene.Field(UserRoleResponseObject,filtering=UserRolesFilteringInputObjects(required=True))
    get_system_permissions = graphene.Field(GroupedPermissionsResponseObject,filtering=PermisionFilteringInputObjects(required=True))


    # @has_query_access(permissions=['can_manage_institution_settings'])
    def resolve_get_roles(self, info,filtering=None,**kwargs):
        try:

            roles=UserRoles.objects.filter(role_is_active=True).all()

            if filtering.institution_unique_id is not None:
                roles=roles.filter(role_institution__institution_unique_id=filtering.institution_unique_id).all()

            if filtering.role_unique_id is not None:
                roles=roles.filter(role_unique_id=filtering.role_unique_id).all()
                
            else:
                roles=roles.filter(role_is_system_default=False,role_institution__institution_unique_id=filtering.institution_unique_id).all()

            roles_list=[]
            for role in roles:
                roles_list.append(UAABuilder.get_role_data(role.role_unique_id))
            
            return UserRoleResponseObject(response=ResponseObject.get_response(id="1"),data=roles_list)
        except:
            return UserRoleResponseObject(response=ResponseObject.get_response(id="4"))
        
    # @has_query_access(permissions=['can_manage_institution_settings'])
    def resolve_get_system_permissions(self, info,filtering=None,**kwargs):
        try:
            permision_groups=UserPermissionsGroup.objects.filter(permission_group_is_global=False).all()
            
            if filtering.group_is_global is not None:
                permision_groups=permision_groups.filter(permission_group_is_global=filtering.group_is_global).all()
            
            if filtering.permission_group_unique_id is not None :
                permision_groups=permision_groups.filter(permission_group_unique_id=filtering.permission_group_unique_id).all()    
            
            permision_group_list=[]
            for permision_group in permision_groups:
                permision_group_list.append(UAABuilder.get_group_permissions_data(permision_group.permission_group_unique_id))
            
            return GroupedPermissionsResponseObject(response=ResponseObject.get_response(id="1"),data=permision_group_list)
        except:
            return GroupedPermissionsResponseObject(response=ResponseObject.get_response(id="4"))
        


        
        
               
        
        