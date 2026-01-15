from graphene import ObjectType
import graphene
from rent_ms_builders.SettingsBuilders import SettingsBuilders
from rent_ms_dto.Settings import *
from rent_ms_settings.models import *


class Query(ObjectType): 
    get_vm_is_drivers = graphene.Field(VmIsDriverResponseObject, filtering=VmIsDriverFilteringInputObject())
    
    @staticmethod
    def resolve_get_vm_is_drivers(self, info,filtering=None,**kwargs):

        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        vm_is_driver = VmIsDrivers.objects.filter(is_active=True).values('uuid')

        if filtering.uuid is not None:
            vm_is_driver = vm_is_driver.filter(uuid=filtering.uuid).values('uuid')
        if filtering.tin_number is not None:
            vm_is_driver = vm_is_driver.filter(name=filtering.tin_number).values('tin_number')

        driver_list = list(map(lambda x: SettingsBuilders.get_vm_is_driver_data(str(x['uuid'])),vm_is_driver))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = driver_list)
    
    get_vm_is_driver_trustees = graphene.Field(VmIsDriverTrusteeResponseObject, filtering=VmIsDriverTrusteeFilteringInputObject())
    
    @staticmethod
    def resolve_get_vm_is_trustees(self, info,filtering=None,**kwargs):
        
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        vm_is_trustee = VmIsTrustees.objects.filter(is_active=True).values('uuid')
        
        if filtering.uuid is not None:
            vm_is_trustee = vm_is_trustee.filter(uuid=filtering.uuid).values('uuid')
        if filtering.first_name and filtering.last_name is not None:
            vm_is_trustee = vm_is_trustee.filter(firstName=filtering.first_name).values('first_name')
            vm_is_trustee = vm_is_trustee.filter(lastName=filtering.last_name).values('last_name')
            
        trustee_list = list(map(lambda x: SettingsBuilders.get_vm_is_driver_trustee_data(str(x['uuid'])), vm_is_trustee))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = trustee_list)
    
    get_vm_is_vehicles = graphene.Field(VmIsVehicleResponseObject, filtering=VmIsVehicleFilteringInputObject())
    
    @staticmethod
    def resolve_get_vm_is_vehicles(self, info,filtering=None,**kwargs):
        
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        vm_is_vehicle = VmIsVehicles.objects.filter(is_active=True).values('uuid')
        
        if filtering.uuid is not None:
            vm_is_vehicle = vm_is_vehicle.filter(uuid=filtering.uuid).values('uuid')
        if filtering.chassis_number and filtering.registration_number is not None:
            vm_is_vehicle = vm_is_vehicle.filter(chassisNumber=filtering.chassis_number).values('chassis_number')
            vm_is_vehicle = vm_is_vehicle.filter(registrationNumber=filtering.registration_number).values('registration_number')
            
        vehicle_list = list(map(lambda x: SettingsBuilders.get_vm_is_vehicle_data(str(x['uuid'])), vm_is_vehicle))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = vehicle_list)
    
    get_vm_is_contracts = graphene.Field(VmIsContractResponseObject, filtering=VmIsContractFilteringInputObject())
    
    @staticmethod
    def resolve_get_vm_is_contracts(self, info,filtering=None,**kwargs):
        
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        vm_is_contract = VmIsContracts.objects.filter(is_active=True).values('uuid')
        
        if filtering.uuid is not None:
            vm_is_contract = vm_is_contract.filter(uuid=filtering.uuid).values('uuid')
        if filtering.contract_start_date and filtering.contract_end_date is not None:
            vm_is_contract = vm_is_contract.filter(contractStartDate=filtering.contract_start_date).values('contract_start_date')
            vm_is_contract = vm_is_contract.filter(contractEndDate=filtering.contract_end_date).values('contract_end_date')
            
        contract_list = list(map(lambda x: SettingsBuilders.get_vm_is_contract_data(str(x['uuid'])), vm_is_contract))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = contract_list)