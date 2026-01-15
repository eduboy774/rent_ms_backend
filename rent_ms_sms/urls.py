from django.contrib import admin
from django.urls import include, path
from rent_ms_sms.views import update_sms_status_from_huduma, rent_ms_sms_callback

urlpatterns = [
    path('update-sms-status-from-huduma/', update_sms_status_from_huduma, name='update_sms_status_from_huduma'),
    path('rent-ms-sms-call-back/', rent_ms_sms_callback, name='rent_ms_sms_callback'),

]
