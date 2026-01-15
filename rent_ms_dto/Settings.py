import graphene
from rent_ms_dto.Enum import VehicleTypeEnum
from rent_ms_dto.Response import ResponseObject
from rent_ms_dto.UserAccounts import UserProfileObject

# DRIVERS
class VmIsDriverInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    tin_number = graphene.String()
    user_profile_uuid = graphene.String()
    driver_licence = graphene.String()

class VmIsDriverObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    tin_number = graphene.String()
    driver_info = graphene.Field(UserProfileObject)
    driver_licence = graphene.String()
    is_active = graphene.Boolean()

class VmIsDriverResponseObject(graphene.ObjectType):
    data = graphene.List(VmIsDriverObject)
    response = graphene.Field(ResponseObject)

class VmIsDriverFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    tin_number = graphene.String()

# TRUSTEE's
class VmIsTrusteeInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    driver_uuid = graphene.String()
    first_name = graphene.String()
    middle_name = graphene.String()
    last_name = graphene.String()
    relationship = graphene.String()
    photo = graphene.String()

class VmIsTrusteeObject(graphene.ObjectType):
    uuid = graphene.String()
    driver_uuid = graphene.String()
    first_name = graphene.String()
    middle_name = graphene.String()
    last_name = graphene.String()
    relationship = graphene.String()
    photo = graphene.String()
    is_active = graphene.Boolean()

class VmIsDriverTrusteeResponseObject(graphene.ObjectType):
    data = graphene.List(VmIsTrusteeObject)
    response = graphene.Field(ResponseObject)

class VmIsDriverTrusteeFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

# VEHICLE's
class VmIsVehicleInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    chassis_number = graphene.String()
    registration_number = graphene.String()
    vehicle_model = graphene.String()
    vehicle_colour = graphene.String()
    vehicle_type = graphene.String()
    vehicle_usage_category = graphene.String()
    transmission_category = graphene.String()
    vehicle_classification = graphene.String()
    vehicle_attachment = graphene.String()

class VmIsVehicleObject(graphene.ObjectType):
    uuid = graphene.String()
    chassis_number = graphene.String()
    registration_number = graphene.String()
    vehicle_model = graphene.String()
    vehicle_colour = graphene.String()
    vehicle_type = graphene.String()
    vehicle_usage_category = graphene.String()
    transmission_category = graphene.String()
    vehicle_classification = graphene.String()
    vehicle_attachment = graphene.String()
    is_active = graphene.Boolean()

class VmIsVehicleResponseObject(graphene.ObjectType):
    data = graphene.List(VmIsVehicleObject)
    response = graphene.Field(ResponseObject)

class VmIsVehicleFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    chassis_number = graphene.String()
    registration_number = graphene.String()

# CONTRACT's
class VmIsContractInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    contract_start_date = graphene.DateTime()
    contract_end_date = graphene.DateTime()
    vehicle_uuid = graphene.String()
    driver_uuid = graphene.String()
    contract_amount = graphene.Decimal()
    interest_rate = graphene.Float()
    total_month = graphene.Int()

class VmIsContractObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    contract_start_date = graphene.DateTime()
    contract_end_date = graphene.DateTime()
    vehicle = graphene.Field(VmIsVehicleObject)
    driver = graphene.Field(VmIsDriverObject)
    contract_amount = graphene.Decimal()
    interest_rate = graphene.Float()
    total_month = graphene.Int()
    is_active = graphene.Boolean()

class VmIsContractResponseObject(graphene.ObjectType):
    data = graphene.List(VmIsContractObject)
    response = graphene.Field(ResponseObject)

class VmIsContractFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    contract_start_date = graphene.Date()
    contract_end_date = graphene.Date()
    contract_amount = graphene.Decimal()