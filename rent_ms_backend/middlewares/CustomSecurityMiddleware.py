import json
from django.http import JsonResponse
from dotenv import dotenv_values
config = dotenv_values(".env")


class CustomSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

            # For token authentication

            # # For token authentication
            # if "api" in request.path.split('/'):
            #     return response

            if "admin" in request.path.split('/'):
                return response

                                    
            # TODO This line allows the federation to Introspect schema make sure you comment it when your going to live invironments
            if "SubgraphIntrospectQuery" in str(request.body):
                return response
            

            # For token authentication
            # headers = request.headers
            # headers_authorization = headers['Authorization'].split(' ')

            # if True:
            return response

            # return JsonResponse(data={'message': 'Operation Denied'}, safe=False)

        except Exception as e:
            return JsonResponse(data={'message': 'Operation Denied'}, safe=False)


