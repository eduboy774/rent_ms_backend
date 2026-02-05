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

RENTAL_STATUS = (
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )

CONSTRACT_STATUS = (
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('TERMINATED', 'Terminated'),
    )

BILLING_FREQUENCY = (
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    )



class House(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    owner_info = models.ForeignKey(UsersProfiles, on_delete=models.CASCADE, related_name='owner_profile', null=True, blank=True)
    name = models.CharField(max_length=255, unique=True,blank=False,null=False)
    address = models.CharField(max_length=255,blank=True,null=True)
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
    name =models.CharField(max_length=255,unique=False,blank=False,null=False)
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


class RoomRental(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='room_rentals')
    renter = models.ForeignKey(UsersProfiles,on_delete=models.CASCADE,related_name='renter_profile')
    period = DateRangeField()
    status = models.CharField(max_length=20, choices=RENTAL_STATUS, default='BOOKED')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "room_rentals"
        ordering = ["-id"]
        verbose_name_plural = "04. Room Rentals"

    def __str__(self):
        return f"RoomRental {self.uuid}"


class HouseRental(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    house = models.ForeignKey(House,on_delete=models.CASCADE,related_name='house_rentals')
    renter = models.ForeignKey(UsersProfiles,on_delete=models.CASCADE,related_name='house_renter_profile')
    period = DateRangeField()
    status = models.CharField(max_length=20, choices=RENTAL_STATUS, default='BOOKED')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "house_rentals"
        ordering = ["-id"]
        verbose_name_plural = "05. House Rentals"

    def __str__(self):
        return f"HouseRental {self.uuid}"
    

class Contract(models.Model):

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    house = models.ForeignKey(House,on_delete=models.CASCADE,related_name='contracts')
    room = models.ForeignKey(Room,on_delete=models.SET_NULL,null=True,blank=True,related_name='contracts')
    owner = models.ForeignKey(UsersProfiles,on_delete=models.CASCADE,related_name='owned_contracts')
    tenant = models.ForeignKey(UsersProfiles,on_delete=models.CASCADE,related_name='tenant_contracts')
    period = DateRangeField()
    term_months = models.IntegerField()
    monthly_rent = models.IntegerField()
    deposit_amount = models.IntegerField()
    billing_frequency = models.CharField(max_length=20,choices=BILLING_FREQUENCY,default='MONTHLY')
    auto_renew = models.BooleanField(default=False)
    notice_period_days = models.IntegerField(default=30)
    status = models.CharField(max_length=20,choices=CONSTRACT_STATUS,default='PENDING')
    expired_at = models.DateTimeField(null=True, blank=True)
    terminated_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "contracts"
        ordering = ["-id"]
        verbose_name_plural = "06. Contracts"

    def __str__(self):
        return f"Contract {self.uuid}"

