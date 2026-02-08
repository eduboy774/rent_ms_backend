from django.db import models
from rent_ms_accounts.models import  UsersProfiles
from django.utils import timezone
import uuid
from django.contrib.postgres.fields import DateRangeField


MEDIUM = (
    ('Sms','Sms'),
    ('Email','Email')
)

STATUS = (
    ('Pending','Pending'),
    ('Sent','Sent'),
    ('Failed','Failed')
)


CONSTRACT_STATUS = (
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('TERMINATED', 'Terminated'),
    )

DURATION = (
        ('3_MONTHS', 'Three Months'),
        ('6_MONTHS', 'Six Months'),
        ('12_MONTHS', 'One Year'),    )



class House(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    owner_info = models.ForeignKey(UsersProfiles, on_delete=models.CASCADE, related_name='owner_profile', null=True, blank=True)
    name = models.CharField(max_length=255, unique=True,blank=False,null=False)
    description = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # todo: add  region,district,ward,  
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.name,self.id,self.uuid)

    class Meta:
        db_table = "houses"
        ordering = ["-id"]
        verbose_name_plural = "01. Houses"


class Renter(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True)
    full_name =models.CharField(max_length=255,unique=False,blank=False,null=False)
    phone_number =models.IntegerField(unique=False,blank=True,null=True)
    nida_number =models.CharField(max_length=255,unique=False,blank=False,null=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.full_name,self.id,self.uuid)
    
    class Meta:
        db_table ="renters"
        ordering =["-id"]
        verbose_name_plural ="02. Renters"

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True)
    medium = models.CharField(choices=MEDIUM,max_length=100,unique=True,blank=False,null=False)
    payload = models.CharField(max_length=100,unique=True,blank=False,null=False)
    status = models.CharField(choices=STATUS,max_length=255,blank=False,null=False, default='Pending')
    attempts = models.CharField(max_length=255,blank=False,null=False)
    error_message = models.CharField(max_length=255,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "{}".format(self.medium,self.payload,self.id,self.uuid)
    
    class Meta:
        db_table ="notifications"
        ordering =["-id"]
        verbose_name_plural ="03. Notifications"

    
class HouseRental(models.Model):

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    house = models.ForeignKey(House,on_delete=models.CASCADE,related_name='house_contracts')
    owner = models.ForeignKey(UsersProfiles,on_delete=models.CASCADE,related_name='owned_contracts')
    renter = models.ForeignKey(Renter,on_delete=models.CASCADE,related_name='renter_contracts')
    duration = models.CharField(max_length=50,choices=DURATION,default='3_MONTHS')
    amount =  models.DecimalField(max_digits=15,decimal_places=2)
    auto_renew = models.BooleanField(default=False)
    notice_period_days = models.IntegerField(default=30)
    status = models.CharField(max_length=50,choices=CONSTRACT_STATUS,default='PENDING')
    expired_at = models.DateTimeField(null=True, blank=True)
    terminated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return "{} - {} - {}".format(self.house.name,self.owner.full_name,self.renter.full_name)

    class Meta:
        db_table = "house_rentals"
        ordering = ["-id"]
        verbose_name_plural = "04. House Rentals"
