import graphene
from rent_ms_builders.SettingsBuilders import SettingsBuilders
from rent_ms_dto.Response import ResponseObject
from rent_ms_dto.Settings import *
from rent_ms_settings.models import *
from django.utils import timezone

# DRIVERS API
class CreateVmIsDriverMutation(graphene.Mutation):
    class Arguments:
        input = VmIsDriverInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VmIsDriverObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.user_profile_uuid:
            user_profile = UsersProfiles.objects.filter(profile_unique_id=input.user_profile_uuid,profile_is_active=True).first()
        
        vm_is_driver, success = VmIsDrivers.objects.update_or_create(
            tin_number = input.tin_number,
            driver_licence = input.driver_licence,
            driver_info = user_profile,
            defaults={
                'is_active': True
            }
        )

        data = SettingsBuilders.get_vm_is_driver_data(id=vm_is_driver.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class UpdateVmIsDriverMutation(graphene.Mutation):
    class Arguments:
        input = VmIsDriverInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VmIsDriverObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.user_profile_uuid:
            user_profile = UsersProfiles.objects.filter(uuid=input.user_profile_uuid,is_active=True).first()
        
        vm_is_driver, success = VmIsDrivers.objects.update_or_create(
            uuid = input.uuid,
            defaults={
                'tin_number' : input.tin_number,
                'driver_licence':input.driver_licence,
                'driver_info':user_profile,
                'is_active': True
            }
        )

        data = SettingsBuilders.get_vm_is_driver_data(id=vm_is_driver.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class DeleteVmIsDriverMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        
        vm_is_driver = VmIsDrivers.objects.filter(uuid=uuid).first()
        vm_is_driver.is_active = False
        vm_is_driver.save()
        return self(ResponseObject.get_response(id='1'))


# TRUSTEES API
class CreateVmIsTrusteeMutation(graphene.Mutation):
    class Arguments:
        input = VmIsDriverInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VmIsTrusteeObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.driver_uuid:
            driver = VmIsDrivers.objects.filter(uuid=input.driver_uuid, is_active=True).first()
            
        vm_is_driver_trustee, success = VmIsTrustees.objects.update_or_create(
            first_name = input.first_name,
            middle_name = input.middle_name,
            last_name = input.last_name,
            driver = driver,
            relationship = input.relationship,
            defaults={
                'is_active': True
            }
        )

        data = SettingsBuilders.get_vm_is_driver_trustee_data(id=vm_is_driver_trustee.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)


class UpdateVmIsTrusteeMutation(graphene.Mutation):
    class Arguments:
        input = VmIsTrusteeInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VmIsTrusteeObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.driver_uuid:
            driver = VmIsDrivers.objects.filter(uuid=input.driver_uuid, is_active=True).first()
        
        vm_is_driver_trustee, success = VmIsTrustees.objects.update_or_create(
            uuid = input.uuid,
            defaults={
                'first_name' : input.first_name,
                'middle_name' : input.middle_name,
                'middle_name' : input.last_name,
                'last_name' : input.last_name,
                'driver' : driver,
                'relationship' : input.relationhip,
                'photo' : input.photo,
                'is_active': True
            }
        )

        data = SettingsBuilders.get_vm_is_driver_trustee_data(id=vm_is_driver_trustee.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class DeleteVmIsTrusteeMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        vm_is_driver_trustee = VmIsTrustees.objects.filter(uuid=uuid).first()
        vm_is_driver_trustee.is_active = False
        vm_is_driver_trustee.save()
        return self(ResponseObject.get_response(id='1'))


# VEHICLE's API
class CreateVmIsVehicleMutation(graphene.Mutation):
    class Arguments:
        input = VmIsVehicleInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VmIsVehicleObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.user_profile_uuid:
            user_profile = UsersProfiles.objects.filter(uuid=input.user_profile_uuid,is_active=True).first()
        
        vm_is_vehicle, success = VmIsVehicles.objects.update_or_create(
            chassis_number = input.chassis_number,
            registration_number = input.registration_number,
            vehicle_model = input.vehicle_model,
            vehicle_colour = input.vehicle_colour,
            defaults={
                'is_active': True
            }
        )

        data = SettingsBuilders.get_vm_is_vehicle_data(id=vm_is_vehicle.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class UpdateVmIsVehicleMutation(graphene.Mutation):
    class Arguments:
        input = VmIsVehicleInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VmIsVehicleObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.user_profile_uuid:
            user_profile = UsersProfiles.objects.filter(uuid=input.user_profile_uuid,is_active=True).first()
        
        vm_is_vehicle, success = VmIsVehicles.objects.update_or_create(
            uuid = input.uuid,
            defaults={
                'chassis_number' : input.chassis_number,
                'registration_number' : input.registration_number,
                'vehicle_model' : input.vehicle_model,
                'vehicle_colour' : input.vehicle_colour,
                'vehicle_type' : input.vehicle_type,
                'vehicle_usage_category' : input.vehicle_usage_category,
                'transmission_category' : input.transmission_category,
                'vehicle_classification' : input.vehicle_classification,
                'vehicle_attachment' : input.vehicle_attachment,
                'is_active': True
            }
        )

        data = SettingsBuilders.get_vm_is_vehicle_data(id=vm_is_vehicle.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class DeleteVmIsVehicleMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        vm_is_vehicle = VmIsVehicles.objects.filter(uuid=uuid).first()
        vm_is_vehicle.is_active = False
        vm_is_vehicle.save()
        return self(ResponseObject.get_response(id='1'))
    
    
# CONTRACT's API
class CreateVmIsContractMutation(graphene.Mutation):
    class Arguments:
        input = VmIsContractInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VmIsContractObject)

    @classmethod
    def mutate(self, root, info, input):
        contract_created_at_time = timezone.now()
        if input.vehicle_uuid:
            vehicle = VmIsVehicles.objects.filter(uuid=input.vehicle_uuid,is_active=True).first()
        if input.driver_uuid:
            driver = VmIsDrivers.objects.filter(uuid=input.driver_uuid, is_active=True).first()
        
        vm_is_contract, success = VmIsContracts.objects.update_or_create(
            contract_start_date = input.contract_start_date,
            contract_end_date = input.contract_end_date,
            vehicle = vehicle,
            driver = driver,
            contract_amount = input.contract_amount,
            interest_rate = input.interest_rate,
            total_month = input.total_month,
            created_at = contract_created_at_time,
            defaults={
                'is_active': True
            }
        )

        data = SettingsBuilders.get_vm_is_contract_data(id=vm_is_contract.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class UpdateVmIsContractMutation(graphene.Mutation):
    class Arguments:
        input = VmIsContractInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VmIsContracts)

    @classmethod
    def mutate(self, root, info, input):
        contract_created_at_time = timezone.now()
        if input.vehicle_uuid:
            vehicle = VmIsVehicles.objects.filter(uuid=input.vehicle_uuid,is_active=True).first()
        if input.driver_uuid:
            driver = VmIsDrivers.objects.filter(uuid=input.driver_uuid, is_active=True).first()
        
        vm_is_contract, success = VmIsContracts.objects.update_or_create(
            uuid = input.uuid,
            defaults={
                'contract_start_date ' : input.contract_start_date,
                'contract_end_date' : input.contract_end_date,
                'vehicle' : vehicle,
                'driver' : driver,
                'contract_amount' : input.contract_amount,
                'interest_rate' : input.interest_rate,
                'total_month' : input.total_month,
                'created_at' : contract_created_at_time,
                'is_active': True
            }
        )

        data = SettingsBuilders.get_vm_is_contract_data(id=vm_is_contract.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class DeleteVmIsContractMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        vm_is_contract = VmIsContracts.objects.filter(uuid=uuid).first()
        vm_is_contract.is_active = False
        vm_is_contract.save()
        return self(ResponseObject.get_response(id='1'))


class Mutation(graphene.ObjectType):
    
    # Drivers Mutation
    delete_driver_mutation = DeleteVmIsDriverMutation().Field()
    update_driver_mutation = UpdateVmIsDriverMutation().Field()
    create_driver_mutation = CreateVmIsDriverMutation().Field()
    
    # Trustees Mutation
    delete_trustee_mutation = DeleteVmIsTrusteeMutation().Field()
    update_trustee_mutation = UpdateVmIsTrusteeMutation().Field()
    create_trustee_mutation = CreateVmIsTrusteeMutation().Field()
    
    # Vehicle Mutation
    delete_vehicle_mutation = DeleteVmIsVehicleMutation().Field()
    update_vehicle_mutation = UpdateVmIsVehicleMutation().Field()
    create_vehicle_mutation = CreateVmIsVehicleMutation().Field()
    
    # Contract Mutation
    delete_contract_mutation = DeleteVmIsContractMutation().Field()
    # update_contract_mutation = UpdateVmIsContractMutation().Field()
    create_contract_mutation = CreateVmIsContractMutation().Field()