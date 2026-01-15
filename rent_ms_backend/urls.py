from django.contrib import admin
from django.urls import path, include

# graphene imports
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

admin.autodiscover()
admin.site.site_header = 'Vehicle Management System'


urlpatterns = [
    path('oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    path('api', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('admin/', admin.site.urls),
    
    path('rental/', include('rent_ms_sms.urls')),

]
