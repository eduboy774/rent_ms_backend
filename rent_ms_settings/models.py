from django.db import models
from rent_ms_accounts.models import  UsersProfiles
from django.utils import timezone
import uuid

MEDIUM = (
    ('Sms','Sms'),
    ('Email','Email')
)

STATUS = (
    ('Pending','Pending'),
    ('Sent','Sent'),
    ('Failed','Failed')
)


class House(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    owner_info = models.ForeignKey(UsersProfiles, on_delete=models.CASCADE, related_name='owner_profile', null=True, blank=True)
    name = models.CharField(max_length=9, unique=True,blank=False,null=False)
    address = models.CharField(max_length=9,blank=True,null=True)
    description = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.name,self.id,self.uuid)

    class Meta:
        db_table = "houses"
        ordering = ["-id"]
        verbose_name_plural = "01. Houses"


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True)
    house_info = models.ForeignKey(House, on_delete=models.CASCADE, related_name='house_info', null=True, blank=True)
    name =models.CharField(max_length=100,unique=False,blank=False,null=False)
    number =models.IntegerField(unique=False,blank=True,null=True)
    capacity =models.IntegerField(unique=False,blank=False,null=False)
    price_per_night =models.IntegerField(unique=False,blank=False,null=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.name,self.id,self.uuid)
    
    class Meta:
        db_table ="rooms"
        ordering =["-id"]
        verbose_name_plural ="02. Rooms"

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

