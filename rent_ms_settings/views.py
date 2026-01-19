import graphene
from rent_ms_builders.SettingsBuilders import SettingsBuilders
from rent_ms_dto.Response import ResponseObject
from rent_ms_dto.Settings import *
from rent_ms_settings.models import *
from django.utils import timezone

# House API
class CreateHouseMutation(graphene.Mutation):
    class Arguments:
        input = HouseInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(HouseObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.owner_uuid:
            owner_info = UsersProfiles.objects.filter(profile_unique_id=input.owner_uuid,profile_is_active=True).first()

        house, success = House.objects.update_or_create(
            name = input.name,
            owner_info = owner_info,
            address = input.address,
            description = input.description,
            defaults={
                'is_active': True
            }
        )

        data = SettingsBuilders.get_house_data(id=house.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class UpdateHouseMutation(graphene.Mutation):
    class Arguments:
        input = HouseInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(HouseObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.owner_uuid:
            owner_info = UsersProfiles.objects.filter(profile_unique_id=input.owner_uuid,profile_is_active=True).first()

        house, success = House.objects.update_or_create(
            uuid = input.uuid,
            defaults={
                'name' : input.name,
                'address' : input.address,
                'description' : input.description,
                'owner_info':owner_info,
                'is_active': True
            }
        )

        data = SettingsBuilders.get_house_data(id=house.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class DeleteHouseMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        
        house = House.objects.filter(uuid=uuid).first()
        house.is_active = False
        house.save()
        return self(ResponseObject.get_response(id='1'))


# ROOM API
class CreateRoomMutation(graphene.Mutation):
    class Arguments:
        input = RoomInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(RoomObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.house_uuid:
            house = House.objects.filter(uuid=input.house_uuid, is_active=True).first()
            
        room, success = Room.objects.update_or_create(
            name = input.name,
            number = input.number,
            capacity = input.capacity,
            price_per_night = input.price_per_night,
            house_info = house,
            defaults={
                'is_active': True
            }
        )

        data = SettingsBuilders.get_room_data(id=room.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)


class UpdateRoomMutation(graphene.Mutation):
    class Arguments:
        input = RoomInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(RoomObject)

    @classmethod
    def mutate(self, root, info, input):
        if input.house_uuid:
            house_info = House.objects.filter(uuid=input.house_uuid, is_active=True).first()
        
        room, success = Room.objects.update_or_create(
            uuid = input.uuid,
            defaults={
                'name' : input.name,
                'number' : input.number,
                'capacity' : input.capacity,
                'price_per_night' : input.price_per_night,
                'house_info' : house_info,
                'is_active': True
            }
        )

        data = SettingsBuilders.get_room_data(id=room.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class DeleteRoomMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        room = Room.objects.filter(uuid=uuid).first()
        room.is_active = False
        room.save()
        return self(ResponseObject.get_response(id='1'))


# Notification's API
class CreateNotificationMutation(graphene.Mutation):
    class Arguments:
        input = NotificationInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(NotificationObject)

    @classmethod
    def mutate(self, root, info, input):
        
        notification, success = Notification.objects.update_or_create(
            medium = input.medium,
            payload = input.payload,
            status = input.status,
            attempts = input.attempts,
            error_message = input.error_message,
            defaults={
                'is_active': True
            }
        )

        data = SettingsBuilders.get_notification_data(id=notification.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class UpdateNotificationMutation(graphene.Mutation):
    class Arguments:
        input = NotificationInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(NotificationObject)

    @classmethod
    def mutate(self, root, info, input):
        
        notification, success = Notification.objects.update_or_create(
            uuid = input.uuid,
            defaults={
                'medium' : input.medium,
                'payload' : input.payload,
                'status' : input.status,
                'attempts' : input.attempts,
                'error_message' : input.error_message,
                'is_active': True
            }
        )

        data = SettingsBuilders.get_notification_data(id=notification.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class DeleteNotificationMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        notification = Notification.objects.filter(uuid=uuid).first()
        notification.is_active = False
        notification.save()
        return self(ResponseObject.get_response(id='1'))
    
    


class Mutation(graphene.ObjectType):
    
    # House Mutation
    delete_house_mutation = DeleteHouseMutation().Field()
    update_house_mutation = UpdateHouseMutation().Field()
    create_house_mutation = CreateHouseMutation().Field()

    # Room Mutation
    delete_room_mutation = DeleteRoomMutation().Field()
    update_room_mutation = UpdateRoomMutation().Field()
    create_room_mutation = CreateRoomMutation().Field()

    # Notification Mutation
    delete_notification_mutation = DeleteNotificationMutation().Field()
    update_notification_mutation = UpdateNotificationMutation().Field()
    create_notification_mutation = CreateNotificationMutation().Field()
