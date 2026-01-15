from rent_ms_dto.Settings import *
from rent_ms_settings.models import *
from rent_ms_builders.UserAccountsBuilders import UserAccountBuilder


class SettingsBuilders:
# Drivers
    def get_vm_is_driver_data(id):
        if id is not None:
            vm_is_driver = VmIsDrivers.objects.filter(uuid=id).first()
            if vm_is_driver:
                return VmIsDriverObject(
                    id = vm_is_driver.id,
                    uuid = vm_is_driver.uuid,
                    tin_number = vm_is_driver.tin_number,
                    driver_licence = vm_is_driver.driver_licence,
                    driver_info = UserAccountBuilder.get_user_profile_data(vm_is_driver.driver_info.profile_unique_id),
                    is_active = vm_is_driver.is_active,
                )
            else:
                return VmIsDriverObject()
        else:
            VmIsDriverObject()

# Trustees
    def get_vm_is_driver_trustee_data(id):
        if id is not None:
            vm_is_driver_trustee = VmIsTrustees.objects.filter(uuid=id).first()
            if vm_is_driver_trustee:
                return VmIsTrusteeObject(
                    id = vm_is_driver_trustee.id,
                    uuid = vm_is_driver_trustee.uuid,
                    first_name = vm_is_driver_trustee.first_name,
                    middle_name = vm_is_driver_trustee.middle_name,
                    last_name = vm_is_driver_trustee.last_name,
                    relationship = vm_is_driver_trustee.relationship,
                    is_active = vm_is_driver_trustee.is_active,
                )
            else:
                return VmIsTrusteeObject()
        else:
            VmIsTrusteeObject()

# Vehicles
    def get_vm_is_vehicle_data(id):
        if id is not None:
            vm_is_vehicle = VmIsVehicles.objects.filter(uuid=id).first()
            if vm_is_vehicle:
                return VmIsVehicles(
                    id = vm_is_vehicle.id,
                    uuid = vm_is_vehicle.uuid,
                    Chassis_number = vm_is_vehicle.chassis_number,
                    registration_number = vm_is_vehicle.registration_number,
                    vehicle_model = vm_is_vehicle.vehicle_model,
                    vehicle_colour = vm_is_vehicle.vehicle_colour,
                    vehicle_type = vm_is_vehicle.vehicle_type,
                    vehicle_usage_category = vm_is_vehicle.vehicle_usage_category,
                    transmission_category = vm_is_vehicle.transmission_category,
                    vehicle_classification = vm_is_vehicle.vehicle_classification,
                    vehicle_attachment = vm_is_vehicle.vehicle_attachment,
                    is_active = vm_is_vehicle.is_active,
                )
            else:
                return VmIsVehicleObject()
        else:
            VmIsVehicleObject()
            

# Contracts
    def get_vm_is_contract_data(id):
        if id is not None:
            vm_is_contract = VmIsContracts.objects.filter(uuid=id).first()
            if vm_is_contract:
                return VmIsContracts(
                    id = vm_is_contract.id,
                    uuid = vm_is_contract.uuid,
                    contract_start_date = vm_is_contract.contract_start_date,
                    contract_end_date = vm_is_contract.contract_end_date,
                    vehicle = vm_is_contract.vehicle,
                    driver = vm_is_contract.driver,
                    contract_amount = vm_is_contract.contract_amount,
                    interest_rate = vm_is_contract.interest_rate,
                    total_month = vm_is_contract.total_month,
                    is_active = vm_is_contract.is_active,
                )
            else:
                return VmIsContractObject()
        else:
            VmIsContractObject()