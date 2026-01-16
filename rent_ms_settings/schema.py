from graphene import ObjectType
import graphene
from rent_ms_builders.SettingsBuilders import SettingsBuilders
from rent_ms_dto.Settings import *
from rent_ms_settings.models import *


class Query(ObjectType): 
    get_houses = graphene.Field(HouseResponseObject, filtering=HouseFilteringInputObject())
    
    @staticmethod
    def resolve_get_houses(self, info,filtering=None,**kwargs):

        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        houses = House.objects.filter(is_active=True).values('uuid')

        if filtering.uuid is not None:
            houses = houses.filter(uuid=filtering.uuid).values('uuid')
        if filtering.name is not None:
            houses = houses.filter(name=filtering.name).values('name')

        house_list = list(map(lambda x: SettingsBuilders.get_house_data(str(x['uuid'])),houses))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = house_list)

    get_rooms = graphene.Field(RoomResponseObject, filtering=RoomFilteringInputObject())
    
    @staticmethod
    def resolve_get_rooms(self, info,filtering=None,**kwargs):
        
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        room = Room.objects.filter(is_active=True).values('uuid')
        
        if filtering.uuid is not None:
            room = room.filter(uuid=filtering.uuid).values('uuid')
        if filtering.name and filtering.number is not None:
            room = room.filter(name=filtering.name).values('name')
            room = room.filter(number=filtering.number).values('number')
            
        room_list = list(map(lambda x: SettingsBuilders.get_room_data(str(x['uuid'])), room))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = room_list)

    get_notification = graphene.Field(NotificationResponseObject, filtering=NotificationFilteringInputObject())
    
    @staticmethod
    def resolve_get_notification(self, info,filtering=None,**kwargs):
        
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        notification = Notification.objects.filter(is_active=True).values('uuid')
        
        if filtering.uuid is not None:
            notification = notification.filter(uuid=filtering.uuid).values('uuid')
        if filtering.medium and filtering.payload is not None:
            notification = notification.filter(medium=filtering.medium).values('medium')
            notification = notification.filter(payload=filtering.payload).values('payload')
            notification_list = list(map(lambda x: SettingsBuilders.get_notification_data(str(x['uuid'])), notification))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = notification_list)
    
    
    
