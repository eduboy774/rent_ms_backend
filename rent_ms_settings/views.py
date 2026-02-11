import graphene
from rent_ms_builders.SettingsBuilders import SettingsBuilders
from rent_ms_dto.Response import ResponseObject
from rent_ms_dto.Settings import *
from rent_ms_settings.models import *
from django.utils import timezone
from django.contrib.postgres.fields import DateRangeField
from django.db import transaction
from psycopg2.extras import DateRange
from rent_ms_sms.models import RentMsSms
from rent_ms_sms.views import SendSms
from rent_ms_utils.RentalUtils import RentalUtils
from django.utils import timezone

from dotenv import dotenv_values

config = dotenv_values(".env")
callbackUrl = config['VILCOM_CALL_BACK_URL']
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


# Renter API
class CreateRenterMutation(graphene.Mutation):
    class Arguments:
        input = RenterInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(RenterObject)

    @classmethod
    def mutate(self, root, info, input):
            
        renter, success = Renter.objects.update_or_create(
            full_name = input.full_name,
            phone_number = input.phone_number,
            nida_number = input.nida_number,
            defaults={
                'is_active': True
            }
        )

        data = SettingsBuilders.get_renter_data(id=renter.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)


class UpdateRenterMutation(graphene.Mutation):
    class Arguments:
        input = RenterInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(RenterObject)

    @classmethod
    def mutate(self, root, info, input):
        
        renter, success = Renter.objects.update_or_create(
            uuid = input.uuid,
            defaults={
                'full_name' : input.full_name,
                'phone_number' : input.phone_number,
                'nida_number' : input.nida_number,
                'is_active': True
            }
        )

        data = SettingsBuilders.get_renter_data(id=renter.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class DeleteRenterMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        room = Renter.objects.filter(uuid=uuid).first()
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
    

class CreateHouseRentalMutation(graphene.Mutation):
    class Arguments:
        input = HouseRentalInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(HouseRentalObject)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, input):

        house = House.objects.filter(
            uuid=input.house_uuid,
            is_active=True
        ).first()

        
        if not house:
            return cls(
                response=ResponseObject.get_response(id='13')
            )

        renter = Renter.objects.filter(
            uuid=input.renter_uuid,
            is_active=True
        ).first()

        if not renter:
            return cls(
                response=ResponseObject.get_response(id='14')
            )
        
        amount = float(input.amount)
        duration_months = int(input.duration)

        existing_rental = HouseRental.objects.filter(
            house=house,
            renter=renter,
            owner=house.owner_info,
            is_active=True
        ).exists()

        if existing_rental:
            return cls(
                response=ResponseObject.get_response(id='15')  # create a new response ID
            )

        rental = HouseRental.objects.create(
            house=house,
            owner=house.owner_info,
            renter=renter,
            duration=input.duration or '3',
            amount=input.amount,
            total_amount= amount * duration_months,
            auto_renew=input.auto_renew or False,
            notice_period_days=input.notice_period_days or 30,
            status=input.status or 'PENDING',
            is_active=True
        )
        

        if rental:
                
                message_to_send = RentalUtils.generate_rental_confirmation_message(
                    rental.renter.renter_title,
                    rental.renter.full_name,
                    rental.house.name,
                    rental.duration,
                    rental.total_amount,
                    rental.reference_no
                    )

                phone_number = rental.renter.phone_number
                third_party_ref = RentalUtils.generate_transaction_reference()

                    # preparing sms and send
                bulk_request = {
                            "senderId": "Vilcom",
                            "envelopes": [
                                {
                                    "message":message_to_send ,
                                    "number":phone_number ,
                                    "thirdPartyRef":third_party_ref
                                },
                            ],
                            "callbackUrl": callbackUrl
                        }

                try:
                            bulk_response = SendSms.send_bulk_sms(bulk_request)
                            print(
                                bulk_response.get('status'),
                                bulk_response.get('code'),
                                bulk_response.get('message')
                            )
                except Exception as e:
                        print(e)
                        print("Failed to send bulk SMS")

                RentMsSms.objects.create(
                status = bulk_response.get('status'),
                code = bulk_response.get('code'),
                message =bulk_response.get('message'),
                message_to_user = message_to_send ,
                user_phone_number = phone_number,
                third_party_ref = third_party_ref
                )


        data = SettingsBuilders.get_house_rental_data(id=rental.uuid)
        return cls(response=ResponseObject.get_response(id='1'), data=data)
    

class UpdateHouseRentalMutation(graphene.Mutation):
    class Arguments:
        input = HouseRentalInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(HouseRentalObject)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, input):

        rental = HouseRental.objects.filter(
            uuid=input.uuid,
            is_active=True
        ).first()

        if not rental:
            return cls(response=ResponseObject.get_response(id='13'))

        if input.duration:
            rental.duration = input.duration

        if input.amount is not None:
            rental.amount = input.amount

        if input.auto_renew is not None:
            rental.auto_renew = input.auto_renew

        if input.notice_period_days is not None:
            rental.notice_period_days = input.notice_period_days

        if input.status:
            rental.status = input.status

        rental.save()

        return cls(
            response=ResponseObject.get_response(id='1'),
            data=rental
        )

    

class DeleteHouseRentalMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(cls, root, info, uuid):

        rental = HouseRental.objects.filter(uuid=uuid).first()
        if not rental:
            return cls(
                response=ResponseObject.get_response(id='13')
            )

        rental.is_active = False
        rental.save()

        return cls(
            response=ResponseObject.get_response(id='1')
        )
 
class ActivateContractMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(cls, root, info, uuid):

        rental = HouseRental.objects.filter(uuid=uuid).first()
        if not rental:
            return cls(
                response=ResponseObject.get_response(id='13')
            )

        rental.status = ContractStatusInum.ACTIVE.value
        rental.activated_at = timezone.now()

        rental.save()

        return cls(
            response=ResponseObject.get_response(id='1')
        )
    
class TerminateContractMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(cls, root, info, uuid):

        rental = HouseRental.objects.filter(uuid=uuid).first()
        if not rental:
            return cls(
                response=ResponseObject.get_response(id='13')
            )

        rental.status = ContractStatusInum.TERMINATED.value
        rental.terminated_at = timezone.now()

        rental.save()

        return cls(
            response=ResponseObject.get_response(id='1')
        )    


class Mutation(graphene.ObjectType):
    
    # House Mutation
    delete_house_mutation = DeleteHouseMutation().Field()
    update_house_mutation = UpdateHouseMutation().Field()
    create_house_mutation = CreateHouseMutation().Field()

    # Renter Mutation
    delete_renter_mutation = DeleteRenterMutation().Field()
    update_renter_mutation = UpdateRenterMutation().Field()
    create_renter_mutation = CreateRenterMutation().Field()

    # Notification Mutation
    delete_notification_mutation = DeleteNotificationMutation().Field()
    update_notification_mutation = UpdateNotificationMutation().Field()
    create_notification_mutation = CreateNotificationMutation().Field()


    # House Rental Mutation
    create_house_rental_mutation = CreateHouseRentalMutation().Field()
    update_house_rental_mutation = UpdateHouseRentalMutation().Field()
    delete_house_rental_mutation = DeleteHouseRentalMutation().Field()
    terminate_contract_mutation=  TerminateContractMutation().Field()
    activate_contract_mutation =  ActivateContractMutation().Field()