from django.core.management.base import BaseCommand
from django.utils import timezone
from rent_ms_accounts.models import UsersProfiles


class Command(BaseCommand):
    help = 'Deactivates users who have been active for more than 7 days'

    def handle(self, *args, **options):
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        # Define types of profiles that need to be deactivated
        profiles_to_deactivate = [
            'SCANNING_OFFICERS', 
            'SCANNING_QC_OFFICERS', 
            'SURVEY_OFFICER',
            'REGISTRY_OFFICER',
            'DATA_ENTRY_OFFICER',
            'DATA_ENTRY_QC_OFFICER',
            'APPROVAL_OFFICER',
        ]
        
        # Filter users to deactivate based on profile type and last login time
        UsersProfiles.objects.filter(
            profile_is_active=True,
            profile_user__last_login__lt=seven_days_ago,
            profile_type__in=profiles_to_deactivate
        ).update(profile_is_active=False, profile_user__is_active=False)
        
        self.stdout.write(self.style.SUCCESS('Users deactivated successfully'))