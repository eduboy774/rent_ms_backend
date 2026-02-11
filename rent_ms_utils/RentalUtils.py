import random
from datetime import datetime
from django.apps import apps


class RentalUtils:

    @staticmethod
    def generate_contract_reference():
        date_str = datetime.now().strftime("%Y%m%d")
        while True:
            random_number = random.randint(1000, 9999)
            reference = f'KASP-{date_str}-{random_number}'
            
            HouseRental = apps.get_model('rent_ms_settings', 'HouseRental')
            if not HouseRental.objects.filter(reference_no=reference).exists():
                return reference

    @staticmethod
    def generate_rental_confirmation_message(
        customer_title,
        customer_name,
        house_name,
        duration,
        amount,
        contract_number
    ):
        return (
            f"Dear {customer_title} {customer_name}, "
            f"your rental contract {contract_number} for {house_name} "
            f"({duration}) has been successfully created. "
            f"The agreed rent amount is {amount} TZS. "
            f"Thank you for choosing our housing services."
        )

    @staticmethod
    def generate_payment_confirmation_message(
        customer_title,
        customer_name,
        amount_paid,
        contract_number
    ):
        return (
            f"Dear {customer_title} {customer_name}, "
            f"your rent payment of {amount_paid} TZS for contract "
            f"{contract_number} Moths has been received successfully. "
            f"Thank you."
        )

    @staticmethod
    def generate_transaction_reference(prefix="RENT"):
        company = "KASP"
        date_str = datetime.now().strftime("%Y%m%d")
        unique_number = random.randint(1000, 9999)
        return f"{company}-{prefix}-{date_str}-{unique_number}"

    
    