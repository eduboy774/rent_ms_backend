from graphene import ObjectType
import graphene
from rent_ms_builders.SettingsBuilders import SettingsBuilders
from rent_ms_dto.Settings import *
from rent_ms_dto.Payment import RentalPaymentResponseObject, RentalPaymentFilteringInputObject, RentalPaymentSummaryResponseObject
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
                lambda x: SettingsBuilders.get_house_rental_data(str(x["uuid"])),
                rentals
            )
        )

        return info.return_type.graphene_type(
            response=ResponseObject.get_response(id="1"),
            data=rental_list
        )

    get_regions = graphene.Field(RegionsResponseObject, filtering=RegionFilteringInputObject())

    @staticmethod
    def resolve_get_regions(self, info, filtering=None, **kwargs):
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data=[])

        regions = Region.objects.all().values('regional_unique_id')

        if filtering.uuid is not None:
            regions = regions.filter(regional_unique_id=filtering.uuid)
        if filtering.name is not None:
            regions = regions.filter(reginal_name__icontains=filtering.name)

        region_list = list(map(lambda x: SettingsBuilders.get_region_data(str(x['regional_unique_id'])), regions))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data=region_list)

    get_districts = graphene.Field(DistrictResponseObject, filtering=DistrictFilteringInputObject())

    @staticmethod
    def resolve_get_districts(self, info, filtering=None, **kwargs):
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data=[])

        districts = District.objects.all().values('district_unique_id')

        if filtering.uuid is not None:
            districts = districts.filter(district_unique_id=filtering.uuid)
        if filtering.name is not None:
            districts = districts.filter(district_name__icontains=filtering.name)
        if filtering.region_uuid is not None:
            districts = districts.filter(district_parent_region__regional_unique_id=filtering.region_uuid)

        district_list = list(map(lambda x: SettingsBuilders.get_district_data(str(x['district_unique_id'])), districts))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data=district_list)

    get_rental_payments = graphene.Field(RentalPaymentResponseObject, filtering=RentalPaymentFilteringInputObject())

    @staticmethod
    def resolve_get_rental_payments(self, info, filtering=None, **kwargs):
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data=[])

        payments = RentalPayment.objects.filter(is_active=True).values('uuid')

        if filtering.uuid is not None:
            payments = payments.filter(uuid=filtering.uuid).values('uuid')

        if filtering.rental_uuid is not None:
            payments = payments.filter(rental__uuid=filtering.rental_uuid).values('uuid')

        if filtering.status is not None:
            payments = payments.filter(status=filtering.status.name).values('uuid')

        if filtering.payment_method is not None:
            payments = payments.filter(payment_method=filtering.payment_method.name).values('uuid')

        if filtering.date_from is not None:
            payments = payments.filter(payment_date__gte=filtering.date_from).values('uuid')

        if filtering.date_to is not None:
            payments = payments.filter(payment_date__lte=filtering.date_to).values('uuid')

        payment_list = list(
            map(
                lambda x: SettingsBuilders.get_rental_payment_data(str(x["uuid"])),
                payments
            )
        )

        return info.return_type.graphene_type(
            response=ResponseObject.get_response(id="1"),
            data=payment_list
        )

    get_rental_payment_summary = graphene.Field(RentalPaymentSummaryResponseObject, rental_uuid=graphene.String(required=True))

    @staticmethod
    def resolve_get_rental_payment_summary(self, info, rental_uuid=None, **kwargs):
        if rental_uuid is None:
            return info.return_type.graphene_type(
                response=ResponseObject.get_response(id="2"),
                data=None
            )

        rental = HouseRental.objects.filter(uuid=rental_uuid, is_active=True).first()
        if not rental:
            return info.return_type.graphene_type(
                response=ResponseObject.get_response(id="13"),
                data=None
            )

        payments = RentalPayment.objects.filter(
            rental=rental,
            is_active=True,
            status='Completed'
        ).order_by('-created_at')

        total_paid = payments.aggregate(total=models.Sum('amount'))['total'] or 0
        balance = max(float(rental.total_amount) - float(total_paid), 0)
        payment_count = payments.count()
        last_payment = payments.first()

        payment_history = list(
            map(
                lambda x: SettingsBuilders.get_rental_payment_data(str(x.uuid)),
                payments
            )
        )

        from rent_ms_dto.Payment import RentalPaymentSummaryObject
        summary_data = RentalPaymentSummaryObject(
            rental_uuid=str(rental.uuid),
            total_amount=float(rental.total_amount),
            total_paid=float(total_paid),
            balance=balance,
            payment_count=payment_count,
            last_payment_date=last_payment.payment_date if last_payment else None,
            payment_history=payment_history
        )

        return info.return_type.graphene_type(
            response=ResponseObject.get_response(id="1"),
            data=summary_data
        )

