from django.contrib.auth.backends import BaseBackend
from provider.oauth2.models import AccessToken 
from provider.utils import now

class BearerTokenAuthentication(BaseBackend):
    def authenticate_header(self, request):
        return 'Bearer'

    def authenticate(headers):
        try:
            bearer_token=headers['Authorization'].split(' ')[1]
            token=AccessToken.objects.filter(token=bearer_token,expires__gt=now(), client__client_id='efe6c087a6525968d454').first()

            return True, token.user
        except AccessToken.DoesNotExist:
            return False, None
        #TODO: remove this when in production
        except Exception as e:
            return False, None