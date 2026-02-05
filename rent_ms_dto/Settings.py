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
class RoomInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    house_uuid = graphene.String()
    name = graphene.String()
    number = graphene.Int()
    capacity = graphene.Int()
    price_per_night = graphene.Int()

class RoomObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    house_info = graphene.Field(HouseObject)
    name = graphene.String()
    number = graphene.Int()
    capacity = graphene.Int()
    price_per_night = graphene.Int()
    
    is_active = graphene.Boolean()

class RoomResponseObject(graphene.ObjectType):
    data = graphene.List(RoomObject)
    response = graphene.Field(ResponseObject)

class RoomFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    name = graphene.String()
    number = graphene.String()

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



    # 

class RoomRentalInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    room_uuid = graphene.String(required=True)
    renter_uuid = graphene.String(required=True)
    period_start = graphene.Date(required=True)
    period_end = graphene.Date(required=True)
    status = graphene.String()
class RoomRentalObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    room = graphene.Field(RoomObject)
    renter = graphene.Field(UserProfileObject)
    period = graphene.String()  # ISO range string
    status = graphene.String()
    created_at = graphene.DateTime()
    is_active = graphene.Boolean()



class RoomRentalResponseObject(graphene.ObjectType):
    data = graphene.List(RoomRentalObject)
    response = graphene.Field(ResponseObject)


class RoomRentalFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    room_uuid = graphene.String()
    renter_uuid = graphene.String()
    status = graphene.String()
