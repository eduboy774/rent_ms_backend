from django.db import models
from django.utils import timezone
import uuid

SMS_DELIVERY_STATUS = (
 ('ENROUTE','ENROUTE'),
 ('DELIVERED','DELIVERED'),
 ('ACCEPTED','ACCEPTED')
)

class RentMsSms(models.Model):
      id = models.AutoField(primary_key=True)
      uuid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True)
      status =models.CharField(choices=SMS_DELIVERY_STATUS,max_length=255,blank=True,null=True)
      code =models.CharField(max_length=255,blank=True,null=True)
      third_party_ref = models.CharField(max_length=255,blank=True,null=True,unique=True)
      message =models.CharField(max_length=255,blank=True,null=True)
      message_to_user =models.CharField(max_length=255,blank=True,null=True)
      user_phone_number =models.CharField(max_length=255,blank=True,null=True)
      smscId = models.CharField(max_length=255,blank=True,null=True)
      created_at = models.DateTimeField(default=timezone.now)
      is_active =models.BooleanField(default=True)

      def __str__(self):
        return "{}".format(self.status,self.id,self.uuid)
    
      class Meta:
          db_table ="rent_ms_sms"
          ordering =["-id"]
          verbose_name_plural ="01. Rent Ms Sms"














