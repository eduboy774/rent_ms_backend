from graphene import ObjectType
import graphene
from rent_ms_settings.models import House, Renter, HouseRental
from rent_ms_accounts.models import UsersProfiles
from rent_ms_builders.SettingsBuilders import SettingsBuilders
from rent_ms_builders.UserAccountsBuilders import UserAccountBuilder
from rent_ms_dto.Settings import DashboardSummaryObject, DashboardSummaryResponseObject
from rent_ms_dto.Response import ResponseObject


class Query(ObjectType):
    get_dashboard_summary = graphene.Field(DashboardSummaryResponseObject)

    @staticmethod
    def resolve_get_dashboard_summary(self, info, **kwargs):
        try:
            # Users
            user_uuids = list(
                UsersProfiles.objects.filter(profile_is_active=True).values_list('profile_unique_id', flat=True)
            )
            users_data = []
            for uid in user_uuids:
                try:
                    user_data = UserAccountBuilder.get_user_profile_data(str(uid))
                    if user_data:
                        users_data.append(user_data)
                except Exception as e:
                    print('Error fetching user profile:', e)

            # Houses
            house_uuids = list(House.objects.filter(is_active=True).values_list('uuid', flat=True))
            houses_data = []
            for uid in house_uuids:
                try:
                    house_data = SettingsBuilders.get_house_data(str(uid))
                    if house_data:
                        houses_data.append(house_data)
                except Exception as e:
                    print('Error fetching house data:', e)

            # Renters
            renter_uuids = list(Renter.objects.filter(is_active=True).values_list('uuid', flat=True))
            renters_data = []
            for uid in renter_uuids:
                try:
                    renter_data = SettingsBuilders.get_renter_data(str(uid))
                    if renter_data:
                        renters_data.append(renter_data)
                except Exception as e:
                    print('Error fetching renter data:', e)

            # All rentals
            all_rental_uuids = list(HouseRental.objects.filter(is_active=True).values('uuid', 'status'))

            active_rentals, pending_rentals, expired_rentals = [], [], []
            for r in all_rental_uuids:
                try:
                    obj = SettingsBuilders.get_house_rental_data(str(r['uuid']))
                    if obj:
                        if r['status'] == 'ACTIVE':
                            active_rentals.append(obj)
                        elif r['status'] == 'PENDING':
                            pending_rentals.append(obj)
                        elif r['status'] == 'EXPIRED':
                            expired_rentals.append(obj)
                except Exception as e:
                    print('Error fetching rental data:', e)

            summary = DashboardSummaryObject(
                total_users=len(users_data),
                total_houses=len(houses_data),
                total_renters=len(renters_data),
                total_rentals=len(all_rental_uuids),
                active_rentals_count=len(active_rentals),
                pending_rentals_count=len(pending_rentals),
                expired_rentals_count=len(expired_rentals),
                users=users_data,
                houses=houses_data,
                renters=renters_data,
                active_rentals=active_rentals,
                pending_rentals=pending_rentals,
                expired_rentals=expired_rentals,
            )

            return info.return_type.graphene_type(
                response=ResponseObject.get_response(id="1"),
                data=summary,
            )
        except Exception as e:
            print('getDashboardSummary error:', e)
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="6"))
