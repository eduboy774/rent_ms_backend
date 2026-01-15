from graphene import ObjectType
import graphene
from rent_ms_builders.PaymentBuilders import PaymentBuilders
from rent_ms_dto.Payment import VilcomOrderFilteringInputObject, VilcomOrderResponseObject, VilcomPaymentFilteringInputObject, VilcomPaymentResponseObject
from rent_ms_dto.Response import ResponseObject
from rent_ms_payment.models import VilcomOrder, VilcomPayment


class Query(ObjectType): 
    get_vilcom_payments = graphene.Field(VilcomPaymentResponseObject,filtering=VilcomPaymentFilteringInputObject())
    get_vilcom_orders = graphene.Field(VilcomOrderResponseObject,filtering=VilcomOrderFilteringInputObject())
    

    @staticmethod
    def resolve_get_vilcom_payments(self, info,filtering=None,**kwargs):

        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        rent_ms_payment = VilcomPayment.objects.filter(is_active=True).values('uuid')

        if filtering.uuid is not None:
            rent_ms_payment = rent_ms_payment.filter(uuid=filtering.uuid).values('uuid')
        if filtering.package_name is not None:
            rent_ms_payment = rent_ms_payment.filter(name=filtering.package_name).values('package_name')

        payment_list = list(map(lambda x: PaymentBuilders.get_vilcom_payment_data(str(x['uuid'])),rent_ms_payment))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = payment_list)
    
    

    def resolve_get_vilcom_orders(self, info,filtering=None,**kwargs):

        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="2"), data = [])
        
        vilcom_order = VilcomOrder.objects.filter(is_active=True).values('uuid')

        if filtering.uuid is not None:
            vilcom_order = vilcom_order.filter(uuid=filtering.uuid).values('uuid')
        if filtering.status is not None:
            vilcom_order = vilcom_order.filter(name=filtering.status).values('status')

        order_list = list(map(lambda x: PaymentBuilders.get_vilcom_order_data(str(x['uuid'])),vilcom_order))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"), data = order_list)
    
    
   
    
    

    
