import graphene
from rent_ms_dto.Response import ResponseObject
from rent_ms_dto.UserAccounts import UserProfileObject

# HOUSE's
class HouseInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    owner_uuid = graphene.String()
    name = graphene.String()
    address = graphene.String()
    description = graphene.String()

class HouseObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    name = graphene.String()
    owner_info = graphene.Field(UserProfileObject)
    address = graphene.String()
    description = graphene.String()
    is_active = graphene.Boolean()

class HouseResponseObject(graphene.ObjectType):
    data = graphene.List(HouseObject)
    response = graphene.Field(ResponseObject)

class HouseFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    name = graphene.String()

# Room's
class RenterInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    full_name = graphene.String()
    phone_number = graphene.String()
    nida_number = graphene.String()
    renter_title = graphene.String()


class RenterObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    full_name = graphene.String()
    renter_title = graphene.String()
    phone_number = graphene.String()
    nida_number = graphene.String()
    is_active = graphene.Boolean()


class RenterResponseObject(graphene.ObjectType):
    data = graphene.List(RenterObject)
    response = graphene.Field(ResponseObject)

class RenterFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    full_name = graphene.String()
    phone_number = graphene.String()

# Notification's
class NotificationInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    medium = graphene.String()
    payload = graphene.String()
    status = graphene.String()
    attempts = graphene.String()
    error_message = graphene.String()
    sent_at = graphene.String()

class NotificationObject(graphene.ObjectType):
    uuid = graphene.String()
    medium = graphene.String()
    payload = graphene.String()
    status = graphene.String()
    attempts = graphene.String()
    error_message = graphene.String()
    is_active = graphene.Boolean()

class NotificationResponseObject(graphene.ObjectType):
    data = graphene.List(NotificationObject)
    response = graphene.Field(ResponseObject)

class NotificationFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    medium = graphene.String()
    payload = graphene.String()



    # house rental
class HouseRentalInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    house_uuid = graphene.String(required=True)
    renter_uuid = graphene.String(required=True)
    duration = graphene.String(required=True)
    amount = graphene.Float(required=True)
    status = graphene.String()
    auto_renew = graphene.Boolean()
    notice_period_days = graphene.Float(required=False)


class HouseRentalObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    house = graphene.Field(HouseObject)
    owner = graphene.Field(UserProfileObject)
    renter = graphene.Field(RenterObject)
    duration = graphene.String()
    notice_period_days = graphene.Int()
    amount = graphene.Float()
    total_amount = graphene.Float()
    auto_renew = graphene.Boolean()
    status = graphene.String()
    expired_at = graphene.DateTime()
    terminated_at = graphene.DateTime()
    created_at = graphene.DateTime()
    is_active = graphene.Boolean()



class HouseRentalResponseObject(graphene.ObjectType):
    data = graphene.List(HouseRentalObject)
    response = graphene.Field(ResponseObject)


class HouseRentalFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    house_uuid = graphene.String()
    owner_uuid = graphene.String()
    renter_uuid = graphene.String()
    status = graphene.String()


# Regions
class RegionsObject(graphene.ObjectType):
    id = graphene.String()
    regional_unique_id = graphene.String()
    reginal_name = graphene.String()
    reginal_postcode = graphene.String()
    reginal_napa_id = graphene.String()
    reginal_code = graphene.String()

class RegionsResponseObject(graphene.ObjectType):
    data = graphene.List(RegionsObject)
    response = graphene.Field(ResponseObject)

class RegionFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    name = graphene.String()


# Districts
class DistrictObject(graphene.ObjectType):
    id = graphene.String()
    district_unique_id = graphene.String()
    district_name = graphene.String()
    district_postcode = graphene.String()
    district_napa_id = graphene.String()
    district_parent_region = graphene.Field(RegionsObject)

class DistrictResponseObject(graphene.ObjectType):
    data = graphene.List(DistrictObject)
    response = graphene.Field(ResponseObject)

class DistrictFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    name = graphene.String()
    region_uuid = graphene.String()


# Dashboard
class DashboardSummaryObject(graphene.ObjectType):
    total_users = graphene.Int()
    total_houses = graphene.Int()
    total_renters = graphene.Int()
    total_rentals = graphene.Int()
    active_rentals_count = graphene.Int()
    pending_rentals_count = graphene.Int()
    expired_rentals_count = graphene.Int()
    users = graphene.List(UserProfileObject)
    houses = graphene.List(HouseObject)
    renters = graphene.List(RenterObject)
    active_rentals = graphene.List(HouseRentalObject)
    pending_rentals = graphene.List(HouseRentalObject)
    expired_rentals = graphene.List(HouseRentalObject)


class DashboardSummaryResponseObject(graphene.ObjectType):
    data = graphene.Field(DashboardSummaryObject)
    response = graphene.Field(ResponseObject)
