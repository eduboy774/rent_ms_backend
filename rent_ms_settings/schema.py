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

    get_renters = graphene.Field(RenterResponseObject, filtering=RenterFilteringInputObject())
    
    @staticmethod
    def resolve_get_renters(self, info,filtering=None,**kwargs):
        
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        renter = Renter.objects.filter(is_active=True).values('uuid')
        
        if filtering.uuid is not None:
            renter = renter.filter(uuid=filtering.uuid).values('uuid')
        if filtering.full_name is not None:
            renter = renter.filter(full_name=filtering.full_name).values('full_name')
            
        renter_list = list(map(lambda x: SettingsBuilders.get_renter_data(str(x['uuid'])), renter))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = renter_list)

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
    

    get_house_rentals = graphene.Field(HouseRentalResponseObject,filtering=HouseRentalFilteringInputObject())

    @staticmethod
    def resolve_get_house_rentals(self, info, filtering=None, **kwargs):

        if filtering is None:
            return info.return_type.graphene_type(
                response=ResponseObject.get_response(id="2"),
                data=[]
            )

        rentals = HouseRental.objects.filter(is_active=True).values("uuid")

        if filtering.uuid is not None:
            rentals = rentals.filter(uuid=filtering.uuid).values("uuid")

        if filtering.house_uuid is not None:
            rentals = rentals.filter(house__uuid=filtering.house_uuid).values("uuid")

        if filtering.renter_uuid is not None:
            rentals = rentals.filter(
                renter__profile_unique_id=filtering.renter_uuid
            ).values("uuid")

        if filtering.status is not None:
            rentals = rentals.filter(status=filtering.status).values("uuid")

        rental_list = list(
            map(
                lambda x: SettingsBuilders.get_room_rental_data(str(x["uuid"])),
                rentals
            )
        )

        return info.return_type.graphene_type(
            response=ResponseObject.get_response(id="1"),
            data=rental_list
        )
    
    
    
