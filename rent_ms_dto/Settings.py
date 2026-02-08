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
    phone_number = graphene.Int()
    nida_number = graphene.String()

class RenterObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    full_name = graphene.String()
    phone_number = graphene.Int()
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
    owner_uuid = graphene.String(required=True)
    renter_uuid = graphene.String(required=True)
    duration = graphene.String(required=True)
    amount = graphene.Float(required=True)
    status = graphene.String()

class HouseRentalObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    house = graphene.Field(HouseObject)
    owner = graphene.Field(UserProfileObject)
    renter = graphene.Field(RenterObject)
    duration = graphene.String()
    notice_period_days = graphene.Int()
    amount = graphene.Float()
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
