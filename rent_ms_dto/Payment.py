import graphene
from rent_ms_dto.Enum import OrderStatusEnum, PaymentMethodEnum, PaymentStatusEnum, PaymentTypeEnum
from rent_ms_dto.Response import ResponseObject
from rent_ms_dto.UserAccounts import UserProfileObject
from rent_ms_dto.Settings import HouseRentalObject


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


# Rental Payment
class RentalPaymentInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    rental_uuid = graphene.String(required=True)
    amount = graphene.Float(required=True)
    payment_date = graphene.Date()
    payment_method = PaymentMethodEnum()
    payment_type = PaymentTypeEnum()
    notes = graphene.String()


class RentalPaymentObject(graphene.ObjectType):
    id = graphene.String()
    uuid = graphene.String()
    rental = graphene.Field(HouseRentalObject)
    amount = graphene.Float()
    payment_date = graphene.Date()
    payment_method = graphene.String()
    payment_type = graphene.String()
    status = graphene.String()
    notes = graphene.String()
    recorded_by = graphene.Field(UserProfileObject)
    created_at = graphene.DateTime()
    is_active = graphene.Boolean()


class RentalPaymentResponseObject(graphene.ObjectType):
    data = graphene.List(RentalPaymentObject)
    response = graphene.Field(ResponseObject)


class RentalPaymentFilteringInputObject(graphene.InputObjectType):
    uuid = graphene.String()
    rental_uuid = graphene.String()
    status = PaymentStatusEnum()
    payment_method = PaymentMethodEnum()
    date_from = graphene.DateTime()
    date_to = graphene.DateTime()


class RentalPaymentSummaryObject(graphene.ObjectType):
    rental_uuid = graphene.String()
    total_amount = graphene.Float()
    total_paid = graphene.Float()
    balance = graphene.Float()
    payment_count = graphene.Int()
    last_payment_date = graphene.DateTime()
    payment_history = graphene.List(RentalPaymentObject)


class RentalPaymentSummaryResponseObject(graphene.ObjectType):
    data = graphene.Field(RentalPaymentSummaryObject)
    response = graphene.Field(ResponseObject)

