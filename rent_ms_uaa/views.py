import graphene
from graphene_federation import build_schema
from rent_ms_backend.decorators.Permission import has_mutation_access
from .models import *
from vm_is_dto.Uaa import UserRolesInputObjects, UserRoleObjects, UserPermisionInputObjects
from vm_is_builders.UAABuilder import UAABuilder
from vm_is_dto.Response import ResponseObject


class CreateUserRolesMutation(graphene.Mutation):
    class Arguments:
        input = UserRolesInputObjects(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserRoleObjects)
    
    @classmethod
    # @has_mutation_access(permissions=['can_manage_institution_settings'])
    def mutate(self, root, info,  input):
        try:

            created_role, _ = UserRoles.objects.update_or_create(
                role_name = input.role_name, 
                defaults={
                    'role_description': input.role_description
                }
            )

            for permision in input.role_permissions:
                UserRolesWithPermissions.objects.create(
                    role_with_permission_role_id=created_role.primary_key,
                    role_with_permission_permission=UserPermissions.objects.filter(permission_unique_id=permision).first(),
                )

            role=UAABuilder.get_role_data(created_role.role_unique_id)    

            return self(ResponseObject.get_response(id="1"),data=role)
        except Exception as e:
            return self(ResponseObject.get_response(id="4"),data=None)
    
class UpdateUserRolesMutation(graphene.Mutation):
    class Arguments:
        input = UserRolesInputObjects(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserRoleObjects)

    @classmethod
    # @has_mutation_access(permissions=['can_manage_institution_settings'])
    def mutate(cls, root, info,  input):
        try:
            role = UserRoles.objects.filter(role_unique_id=input.role_unique_id).first()
            role.role_name = input.role_name
            role.role_description = input.role_description
            role.save()

            UserRolesWithPermissions.objects.filter(role_with_permission_role=role).delete()

            for permision in input.role_permissions:
                UserRolesWithPermissions.objects.create(
                    role_with_permission_role=role,
                    role_with_permission_permission=UserPermissions.objects.filter(permission_unique_id=permision).first(),
                )

            role=UAABuilder.get_role_data(role.role_unique_id) 

            return UpdateUserRolesMutation(ResponseObject.get_response(id="1"),data=role)
        except Exception as e:
            return UpdateUserRolesMutation(ResponseObject.get_response(id="4"),data=None)
        
class DeleteUserRolesMutation(graphene.Mutation):
    class Arguments:
        role_unique_id = graphene.String(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    # @has_mutation_access(permissions=['can_manage_institution_settings'])
    def mutate(cls, root, info,  role_unique_id):
        try:
            UserRoles.objects.filter(role_unique_id=role_unique_id).delete()

            return DeleteUserRolesMutation(ResponseObject.get_response(id="1"))
        except Exception as e:
            return DeleteUserRolesMutation(ResponseObject.get_response(id="4"))



class SeedPermissionsMutation(graphene.Mutation):
    
    # TODO Seeding new permission to the system. 
    
    # This endpoint will used only on development time, and must be commented when system
    # goes to production phase.
    # The aim of this endpoint is to enable frontend developers to add any new
    # that is not available or pre seeded by backend to fasten the development.

    class Arguments:
        permissions = graphene.List(UserPermisionInputObjects)

    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(cls, root, info, permissions):
        for permission in permissions:
            UserPermissions.objects.update_or_create(
                permission_code=permission.code,
                permission_group=UserPermissionsGroup.objects.filter(permission_group_unique_id=permission.group).first(),
                defaults={
                    'permission_name': permission.name,
                    'permission_createdby_id': 2,
                }
            )

        return SeedPermissionsMutation(ResponseObject.get_response(id="1"))


class Mutation(graphene.ObjectType):
    create_user_roles = CreateUserRolesMutation.Field()
    update_user_roles = UpdateUserRolesMutation.Field()
    delete_user_roles = DeleteUserRolesMutation.Field()

    seed_user_permissions = SeedPermissionsMutation.Field()

    
schema = build_schema(Mutation, types=[])