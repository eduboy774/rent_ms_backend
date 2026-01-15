import random
from datetime import datetime
from django.apps import apps

class RentMsUtils:
    def generate_reference_number():
            date_str = datetime.now().strftime("%Y%m%d")
            while True:
                random_number = random.randint(1000, 9999)
                reference = f'VIL-{date_str}-{random_number}'
                VilcomOrder = apps.get_model('vm_is_payment', 'VilcomOrder')  # Lazy import
                if not VilcomOrder.objects.filter(reference_no=reference).exists():
                    return reference
                
    def generate_order_message(custome_title,customer_name, food_name, amount_paid, order_number):
        return (
            f"Dear {custome_title} {customer_name} your order {order_number} for {food_name} has been received successfully. Payment of {amount_paid} Tzs has been confirmed. Thank you for choosing Vilcom!"
        )
    

    def generate_payment_message(custome_title,customer_name, amount_paid, order_number):
        return (
            f"Dear {custome_title} {customer_name}, your payment {amount_paid} Tzs for order {order_number} has been received successfully. Thank you for choosing Vilcom!"
        )

    
    def generate_third_party_ref(prefix):
        company="VIL"
        date_str = datetime.now().strftime("%Y%m%d")
        unique_number = random.randint(1000, 9999)
        return f"{company}-{prefix}-{date_str}-{unique_number}"
    