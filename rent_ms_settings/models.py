from django.db import models
from rent_ms_accounts.models import  UsersProfiles
from django.utils import timezone
import uuid

RELATIONSHIP = (
    ('Mother','Mother'),
    ('Father','Father'),
    ('Auncle','Auncle'),
    ('Aunt','Aunt'),
    ('Brother','Brother'),
    ('Sister','Sister')
)

VEHICLE_TYPE = (
    ('Cars','Cars'),
    ('ThreeWheelers','ThreeWheelers'),
    ('Motorcycles','Motorcycles')
)

TRANSMISSION_CATEGORY = (
    ('Automatic','Automatic'),
    ('Manual','Manual')
)

VEHICLE_USAGE_CATEGORY = (
    ('Personal','Personal'),
    ('Commercial','Commercial')
)

VEHICLE_CLASSIFICATION = (
    ('Passengers','Passenger'),
    ('Goods','Goods')
)

class VmIsDrivers(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    driver_info = models.ForeignKey(UsersProfiles, on_delete=models.CASCADE, related_name='driver_profile', null=True, blank=True)
    tin_number = models.CharField(max_length=9, unique=True,blank=False,null=False)
    # street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name='driver_stree', null=False, blank=False) Todo import and make a model of region,distric,council,ward,stree
    driver_licence = models.CharField(default='/profiles/service.png', max_length=600, blank=False,null=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.first_name,self.id,self.uuid)

    class Meta:
        db_table = "vm_is_drivers"
        ordering = ["-id"]
        verbose_name_plural = "01. VmIs Drivers"


class VmIsTrustees(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True)
    driver = models.ForeignKey(VmIsDrivers, on_delete=models.CASCADE, related_name='trustee_driver', null=True, blank=True)
    first_name =models.CharField(max_length=100,unique=False,blank=False,null=False)
    middle_name =models.CharField(max_length=100,unique=False,blank=True,null=True)
    last_name =models.CharField(max_length=100,unique=False,blank=False,null=False)
    relationship = models.CharField(choices=RELATIONSHIP,max_length=255,blank=False,null=False,default='Mother')
    photo = models.CharField(default='/profiles/food.png', max_length=600, blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.first_name,self.last_name,self.id,self.uuid)
    
    class Meta:
        db_table ="vm_is_trustees"
        ordering =["-id"]
        verbose_name_plural ="02. VmIs Trustees"

class VmIsVehicles(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True)
    chassis_number = models.CharField(max_length=100,unique=True,blank=False,null=False)
    registration_number = models.CharField(max_length=100,unique=True,blank=False,null=False)
    vehicle_model = models.CharField(max_length=100,unique=False,blank=False,null=False)
    vehicle_colour = models.CharField(max_length=100,unique=False,blank=False,null=False)
    vehicle_type = models.CharField(choices=VEHICLE_TYPE,max_length=255,blank=False,null=False,default='Cars')
    vehicle_usage_category = models.CharField(choices=VEHICLE_USAGE_CATEGORY,max_length=255,blank=False,null=False,default='Commercial')
    transmission_category = models.CharField(choices=TRANSMISSION_CATEGORY,max_length=255,blank=False,null=False,default='Automatic')
    vehicle_classification = models.CharField(choices=VEHICLE_CLASSIFICATION,max_length=255,blank=False,null=False,default='Passengers')
    vehicle_attachment = models.FileField(upload_to='attachments/')
    created_at = models.DateTimeField(default=timezone.now)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "{}".format(self.chassis_number,self.registration_number,self.id,self.uuid)
    
    class Meta:
        db_table ="vm_is_vehicles"
        ordering =["-id"]
        verbose_name_plural ="03. VmIs Vehicles"

class VmIsContracts(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True)
    contract_start_date = models.DateTimeField(default=timezone.now)
    contract_end_date = models.DateTimeField(default=timezone.now)
    vehicle = models.ForeignKey(VmIsVehicles, on_delete=models.CASCADE, related_name='contract_vehicle', null=True, blank=True)
    # street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name='driver_stree', null=False, blank=False) Todo import and make a model of region,distric,council,ward,stree
    driver = models.ForeignKey(VmIsDrivers, on_delete=models.CASCADE, related_name='vilcom_package', null=True, blank=True)
    contract_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.FloatField()
    total_month = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "{}".format(self.contract_start_date,self.contract_end_date,self.id,self.uuid)
    
    class Meta:
        db_table ="vm_is_contracts"
        ordering =["-id"]
        verbose_name_plural ="04. VmIs Contracts"