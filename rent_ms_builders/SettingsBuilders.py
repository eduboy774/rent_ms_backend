from rent_ms_dto.Settings import *
from rent_ms_settings.models import *
from rent_ms_builders.UserAccountsBuilders import UserAccountBuilder


class SettingsBuilders:
# Houses
    def get_house_data(id):
        if id is not None:
            house = House.objects.filter(uuid=id).first()
            if house:
                return HouseObject(
                    id = house.id,
                    uuid = house.uuid,
                    name = house.name,
                    address = house.address,
                    description = house.description,
                    owner_info = UserAccountBuilder.get_user_profile_data(house.owner_info.profile_unique_id),
                    is_active = house.is_active,
                )
            else:
                return HouseObject()
        else:
            HouseObject()

# Rooms
    def get_room_data(id):
        if id is not None:
            room = Room.objects.filter(uuid=id).first()
            if room:
                return RoomObject(
                    id = room.id,
                    uuid = room.uuid,
                    name = room.name,
                    number = room.number,
                    capacity = room.capacity,
                    price_per_night = room.price_per_night,
                    house_info = SettingsBuilders.get_house_data(room.house_info.uuid),
                    is_active = room.is_active,
                )
            else:
                return RoomObject()
        else:
            RoomObject()

# Notifications
    def get_notification_data(id):
        if id is not None:
            notification = Notification.objects.filter(uuid=id).first()
            if notification:
                return NotificationObject(
                    id = notification.id,
                    uuid = notification.uuid,
                    medium = notification.medium,
                    payload = notification.payload,
                    status = notification.status,
                    attempts = notification.attempts,
                    error_message = notification.error_message,
                    is_active = notification.is_active,
                )
            else:
                return NotificationObject()
        else:
            NotificationObject()


 # ---------------- ROOM RENTAL ----------------
    def get_room_rental_data(id):
        if id is not None:
            rental = RoomRental.objects.filter(uuid=id).first()
            if rental:
                return RoomRentalObject(
                    id=rental.id,
                    uuid=str(rental.uuid),
                    room=SettingsBuilders.get_room_data(
                        rental.room.uuid if rental.room else None
                    ),
                    renter=SettingsBuilders.get_user_profile_data(
                        rental.renter.profile_unique_id if rental.renter else None
                    ),
                    period=str(rental.period),
                    status=rental.status,
                    created_at=rental.created_at,
                    is_active=rental.is_active,
                )
            else:
                return RoomRentalObject()
        else:
            return RoomRentalObject()