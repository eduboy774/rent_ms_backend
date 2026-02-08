from rent_ms_dto.Settings import *
from rent_ms_settings.models import *
from rent_ms_builders.UserAccountsBuilders import UserAccountBuilder


class SettingsBuilders:
# Houses
    def get_house_data(id):
        if id is not None:
            house = House.objects.filter(uuid=id).first()
            if house:
                return HouseObject(
                    id = house.id,
                    uuid = house.uuid,
                    name = house.name,
                    description = house.description,
                    owner_info = UserAccountBuilder.get_user_profile_data(house.owner_info.profile_unique_id),
                    is_active = house.is_active,
                )
            else:
                return HouseObject()
        else:
            HouseObject()

# Renter
    def get_renter_data(id):
        if id is not None:
            renter = Renter.objects.filter(uuid=id).first()
            if renter:
                return RenterObject(
                    id = renter.id,
                    uuid = renter.uuid,
                    full_name = renter.full_name,
                    phone_number = renter.phone_number,
                    nida_number = renter.nida_number,
                    is_active = renter.is_active,
                )
            else:
                return RenterObject()
        else:
            return RenterObject()

# Notifications
    def get_notification_data(id):
        if id is not None:
            notification = Notification.objects.filter(uuid=id).first()
            if notification:
                return NotificationObject(
                    id = notification.id,
                    uuid = notification.uuid,
                    medium = notification.medium,
                    payload = notification.payload,
                    status = notification.status,
                    attempts = notification.attempts,
                    error_message = notification.error_message,
                    is_active = notification.is_active,
                )
            else:
                return NotificationObject()
        else:
            NotificationObject()


 # ---------------- House RENTAL ----------------
    def get_house_rental_data(id):
        if id is not None:
            rental = HouseRental.objects.filter(uuid=id).first()
            if rental:
                return HouseRentalObject(
                    id=rental.id,
                    uuid=str(rental.uuid),
                    house=SettingsBuilders.get_house_data(
                        rental.house.uuid if rental.house else None
                    ),
                    owner=UserAccountBuilder.get_user_profile_data(
                        rental.owner.profile_unique_id if rental.owner else None
                    ),
                    renter=SettingsBuilders.get_renter_data(
                        rental.renter.uuid if rental.renter else None
                    ),
                    duration=rental.duration,
                    notice_period_days=rental.notice_period_days,
                    amount=rental.amount,
                    auto_renew=rental.auto_renew,
                    status=rental.status,
                    expired_at=rental.expired_at,
                    terminated_at=rental.terminated_at,
                    created_at=rental.created_at,
                    is_active=rental.is_active,
                )
            else:
                return HouseRentalObject()
        else:
            return HouseRentalObject()