import graphene
from rent_ms_builders.PaymentBuilders import PaymentBuilders
from rent_ms_dto.Enum import PaymentMethodInum, PaymentStatusInum, PaymentTypeInum
from rent_ms_dto.Payment import *
from rent_ms_dto.Response import ResponseObject
from rent_ms_dto.Settings import *
from rent_ms_payment.models import VilcomOrder, VilcomOrderItem, VilcomPayment
from rent_ms_settings.models import *
from django.utils import timezone
from rent_ms_sms.models import RentMsSms
from rent_ms_sms.views import SendSms
from rent_ms_utils.RentMsUtils import RentMsUtils
from dotenv import dotenv_values


config = dotenv_values(".env")
callbackUrl = config['VILCOM_CALL_BACK_URL']


class CreateVilcomOrderMutation(graphene.Mutation):
    class Arguments:
        input = VilcomOrderInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.List(VilcomOrderObject)

    @classmethod
    def mutate(self, root, info, input):
        payment_created_at_time = timezone.now()
        orders = []
        for order in input.order_list:
            if order.customer_uuid:
                user = UsersProfiles.objects.filter(
                    profile_unique_id=order.customer_uuid
                ).first()

                vilcom_order = VilcomOrder.objects.create(
                    status=order.status.value,
                    delivery_address=order.delivery_address,
                    notes=order.notes,
                    customer=user,
                    is_active = True
                )

                if order.food_uuid:
                    food = VilcomFood.objects.filter(
                        uuid=order.food_uuid, is_active=True
                    ).first()

                    VilcomOrderItem.objects.create(
                        food=food,
                        price=food.food_price,
                        order=vilcom_order,
                        quantity=order.quantity,
                        is_active = True
                    )
                amount_to_pay = food.food_price * int(order.quantity)
                message_to_send = VilcomUtils.generate_order_message(
                    user.profile_title,
                    user.profile_user.first_name,
                    food.food_name,
                    amount_to_pay,
                    vilcom_order.reference_no
                    )
                
                phone_number = user.profile_phone
                third_party_ref = VilcomUtils.generate_third_party_ref('ORD')

                
                    # preparing sms and send
                bulk_request = {
                            "senderId": "SHULENI",
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

            VilcomPayment.objects.create(
                order = vilcom_order,
                status = PaymentStatusInum.Pending._value_ ,
                method = PaymentMethodInum.Cash._value_ ,
                payment_type = PaymentTypeInum.Full._value_ ,
                paid_amount = amount_to_pay,
                paid_at = payment_created_at_time
            )
 
            orders.append(PaymentBuilders.get_vilcom_order_data(id=vilcom_order.uuid))
        return self(response=ResponseObject.get_response(id='1'), data=orders)


class UpdateVilcomOrderMutation(graphene.Mutation):
    class Arguments:
        input = VilcomOrderInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.List(VilcomOrderObject)

    @classmethod
    def mutate(self, root, info, input):
        orders = []
        for order in input.order_list:
            if order.customer_uuid:
             user = UsersProfiles.objects.filter(profile_unique_id=order.customer_uuid).first()
             vilcom_order, success = VilcomOrder.objects.update_or_create(
                    uuid = order.uuid,
                    defaults={
                        'status' : order.status,
                        'delivery_address' : order.delivery_address,
                        'notes':order.notes,
                        'customer':user,
                        'is_active': True
                    }
                )

        data = PaymentBuilders.get_vilcom_order_data(id=vilcom_order.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class ActivateOrDeactivateVilcomOrderMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        
        vilcom_order = VilcomOrder.objects.filter(uuid=uuid).first()
        if vilcom_order.is_active == True :
           vilcom_order.is_active = False
           vilcom_order.save()
           return self(ResponseObject.get_response(id='10'))
        elif vilcom_order.is_active == False :
             vilcom_order.is_active = True
             vilcom_order.save()
             return self(ResponseObject.get_response(id='9'))     
        

class CreateVilcomPaymentMutation(graphene.Mutation):
    class Arguments:
        input = VilcomPaymentInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VilcomPaymentObject)

    @classmethod
    def mutate(self, root, info, input):

        paid_at_time = timezone.now()

        
        if input.order_uuid:
           vilcom_order = VilcomOrder.objects.filter(uuid=input.order_uuid,is_active=True).first()
           vilcom_order_items = VilcomOrderItem.objects.filter(order=vilcom_order,is_active=True).first()

           if input.paid_amount is None:
              paid_amount =  vilcom_order_items.price * vilcom_order_items.quantity
           else:
              paid_amount =  input.paid_amount * vilcom_order_items.quantity

           rent_ms_payment, success = VilcomPayment.objects.update_or_create(
                status = input.status.value,
                method = input.method.value,
                paid_amount = paid_amount,
                paid_at = paid_at_time,
                order = vilcom_order,
                defaults={
                    'is_active': True
                }
            )
           
        data = PaymentBuilders.get_vilcom_payment_data(id=rent_ms_payment.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class UpdateVilcomPaymentMutation(graphene.Mutation):
    class Arguments:
        input = VilcomPaymentInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(VilcomPaymentObject)

    @classmethod
    def mutate(self, root, info, input):

        paid_at_time = timezone.now()
        
        if input.order_uuid:
           vilcom_order = VilcomOrder.objects.filter(uuid=input.order_uuid,is_active=True).first()
           vilcom_order_items = VilcomOrderItem.objects.filter(order=vilcom_order,is_active=True).first()

           if input.paid_amount is None:
              paid_amount =  vilcom_order_items.price * vilcom_order_items.quantity
           else:
              paid_amount =  input.paid_amount * vilcom_order_items.quantity

           rent_ms_payment, success = VilcomPayment.objects.update_or_create(
                uuid = input.uuid,
                defaults={
                    'status' : input.status.value,
                    'method' : input.method.value,
                    'paid_amount':paid_amount,
                    'paid_at':paid_at_time,
                    'order':vilcom_order,
                    'is_active': True
                }
            )
        
    
        message_to_send = VilcomUtils.generate_payment_message(
                    vilcom_order.customer.profile_title,
                    vilcom_order.customer.profile_user.first_name,
                    paid_amount,
                    vilcom_order.reference_no
                    )
                
        phone_number =  vilcom_order.customer.profile_phone
        third_party_ref = VilcomUtils.generate_third_party_ref('PAY')

                
                    # preparing sms and send
        bulk_request = {
                            "senderId": "SHULENI",
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
           
               

        data = PaymentBuilders.get_vilcom_payment_data(id=rent_ms_payment.uuid)
        return self(ResponseObject.get_response(id='1'), data=data)

class ActivateOrDeactivateVilcomPaymentMutation(graphene.Mutation):
    class Arguments:
        uuid = graphene.String()
    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(self, root, info, uuid):
        
        rent_ms_payment = VilcomPayment.objects.filter(uuid=uuid).first()
        if rent_ms_payment.is_active == True :
           rent_ms_payment.is_active = False
           rent_ms_payment.save()
           return self(ResponseObject.get_response(id='10'))
        elif rent_ms_payment.is_active == False :
             rent_ms_payment.is_active = True
             rent_ms_payment.save()
             return self(ResponseObject.get_response(id='9'))
    

class Mutation(graphene.ObjectType):
    
    #order
    create_vilcom_order_mutation = CreateVilcomOrderMutation.Field()
    update_vilcom_order_mutation = UpdateVilcomOrderMutation.Field()
    activate_or_deactivate_vilcom_location_mutation = ActivateOrDeactivateVilcomOrderMutation.Field()

    # payment
    create_vilcom_payment_mutation = CreateVilcomPaymentMutation.Field()
    update_vilcom_payment_mutation = UpdateVilcomPaymentMutation.Field()
    activate_or_deactivate_vilcom_payment_mutation = ActivateOrDeactivateVilcomPaymentMutation.Field()



    




  

    