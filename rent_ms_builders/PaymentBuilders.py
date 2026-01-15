from rent_ms_dto.Payment import *
from rent_ms_payment.models import *
from rent_ms_builders.UserAccountsBuilders import UserAccountBuilder


class PaymentBuilders:
    def get_vilcom_order_data(id):
        if id is not None:
            vilcom_order = VilcomOrder.objects.filter(uuid=id).first()
            if vilcom_order:
                return VilcomOrderObject(
                    id = vilcom_order.id,
                    uuid = vilcom_order.uuid,
                    status = vilcom_order.status,
                    delivery_address = vilcom_order.delivery_address,
                    notes = vilcom_order.notes,
                    customer = UserAccountBuilder.get_user_profile_data(vilcom_order.customer.profile_unique_id),
                    is_active = vilcom_order.is_active,
                )
            else:
                return VilcomOrderObject()
        else:
            VilcomOrderObject()

    def get_vilcom_payment_data(id):
        if id is not None:
            vm_is_payment = VilcomPayment.objects.filter(uuid=id).first()
            if vm_is_payment:
                return VilcomPaymentObject(
                    id = vm_is_payment.id,
                    uuid = vm_is_payment.uuid,
                    status = vm_is_payment.status,
                    method = vm_is_payment.method,
                    paid_amount = vm_is_payment.paid_amount,
                    paid_at = vm_is_payment.paid_at,
                    order =PaymentBuilders.get_vilcom_order_data(vm_is_payment.order.uuid),
                    is_active = vm_is_payment.is_active,
                )
            else:
                return VilcomPaymentObject()
        else:
            VilcomPaymentObject()
 
   
       

   
   