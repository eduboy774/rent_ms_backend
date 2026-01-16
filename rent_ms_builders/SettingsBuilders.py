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
