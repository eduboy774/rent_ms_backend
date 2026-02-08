
from django.http import JsonResponse
from provider.utils import now
from provider.oauth2.models import AccessToken

class ConcurrentLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == '/oauth2/access_token' and request.method == 'POST':

            if request.POST['grant_type'] == 'password':

                login_user = AccessToken.objects.filter(user__username=str(request.POST['username']), expires__gte=now(), client__client_id='f166f09731e878aa4a5b').first() 
                if login_user:
                    login_user.expires=now()
                    login_user.save()
                
        response = self.get_response(request)
            
        return response

    def _get_response_error(self):
        return JsonResponse({'error': 'Concurrent login detected. Log out and try again.'}, status=423)

    def _get_lockout_error(self):
        return JsonResponse({'error': 'Account locked. Contact Administrators or wait until one hour (60 Minutes)'}, status=423)

    def _get_forbiden_error(self):
        return JsonResponse({'error': 'You need a registered device to be able to login'}, status=423)

