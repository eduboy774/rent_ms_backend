import graphene
from rent_ms_dto.Enum import OrderStatusEnum, PaymentMethodEnum, PaymentStatusEnum, PaymentTypeEnum
from rent_ms_dto.Response import ResponseObject
from rent_ms_dto.UserAccounts import UserProfileObject


# Vilcom Order
class VilcomSingleOrderInput(graphene.InputObjectType):
        uuid = graphene.String()
        customer_uuid = graphene.String()
        food_uuid = graphene.String() 
        status = OrderStatusEnum()
        delivery_address = graphene.String()
        notes = graphene.String()
        quantity = graphene.String()

class VilcomOrderInputObject(graphene.InputObjectType):
      order_list = graphene.List(VilcomSingleOrderInput)

class VilcomOrderObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    customer = graphene.Field(UserProfileObject)
    status = OrderStatusEnum()
    delivery_address = graphene.String()
    notes = graphene.String()
    is_active = graphene.Boolean()

class VilcomOrderResponseObject(graphene.ObjectType):
    data = graphene.List(VilcomOrderObject)
    response = graphene.Field(ResponseObject)

class VilcomOrderFilteringInputObject(graphene.InputObjectType):
      uuid = graphene.String()
      status = graphene.String()
      customer_uuid = graphene.String()


# Vilcom Payment
class VilcomPaymentInputObject(graphene.InputObjectType):
      uuid = graphene.String()
      order_uuid = graphene.String()
      status = PaymentStatusEnum()
      method = PaymentMethodEnum()
      paid_amount = graphene.String()
      payment_type  =PaymentTypeEnum()

class VilcomPaymentObject(graphene.ObjectType):
       id = graphene.String()
       uuid = graphene.String()
       order = graphene.Field(VilcomOrderObject)
       status = PaymentStatusEnum()
       method = PaymentMethodEnum()
       paid_amount = graphene.String()
       paid_at = graphene.String()
       is_active = graphene.String()

class VilcomPaymentResponseObject(graphene.ObjectType):
    data = graphene.List(VilcomPaymentObject)
    response = graphene.Field(ResponseObject)

class VilcomPaymentFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    status = PaymentStatusEnum()
    method = PaymentMethodEnum()


