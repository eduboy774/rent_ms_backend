import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from graphql.pyutils import did_you_mean


class GraphQLAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            if "admin" in request.path.split('/'):
                return response
            
            if settings.DJANGO_HOST =="production":                                       
                # TODO This line allows the federation to Introspect schema make sure you comment it when your going to live invironments
                if "IntrospectionQuery" in str(request.body) or "__schema" in str(request.body) or "alias" in str(request.body):
                    return JsonResponse(data={'message': 'Operation Denied GraphQL Meddleware'}, safe=False)
                
            did_you_mean.__globals__['MAX_LENGTH'] = 0    
                                 
            if "api" in request.path.split('/'):
                
                if request.method =="GET" or "application/json" not in str(request.content_type) :
                    json_data = {"data":{"NotAllowed":{"graphql":"invalid request method or request content type",}}}
                    response = HttpResponse(json.dumps(json_data), content_type="application/json")            


            if "Introspection" in str(request.body) or "__" in str(request.body):
                json_data = {"data":{"NotAllowed":{"introspection":None,}}}
                response = HttpResponse(json.dumps(json_data), c="application/json")


            if "errors" in str(response.content):
                json_data = {"data":{"errors":{"error":"an error occurred",}}}
                response = HttpResponse(json.dumps(json_data), content_type="application/json")

         
            
            # if True:
            return response

            # return JsonResponse(data={'message': 'Operation Denied GraphQL Meddleware'}, safe=False)

        except Exception as e:
            return JsonResponse(data={'message': 'Operation Denied GraphQL Meddleware'}, safe=False)