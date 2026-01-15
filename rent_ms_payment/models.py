from django.db import models
from rent_ms_accounts.models import  UsersProfiles
import uuid
from rent_ms_utils.RentMsUtils import RentMsUtils
from django.utils import timezone

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Preparing', 'Preparing'),
    ('Out_For_Delivery', 'Out For Delivery'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

PAYMENT_STATUS = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Failed', 'Failed'),
    ('Refunded', 'Refunded'),
)

PAYMENT_METHOD = (
    ('Cash', 'Cash'),
    ('Card', 'Card'),
    ('MobileMoney', 'Mobile Money'),
    ('Online', 'Online'),
)


PAYMENT_TYPE = (
    ('Full', 'Full'),
    ('Partial', 'Partial'),
)

class VilcomOrder(models.Model):
      id = models.AutoField(primary_key=True)
      uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
      customer = models.ForeignKey(UsersProfiles,related_name='customer_info', on_delete=models.CASCADE)
      status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
      delivery_address = models.TextField()
      notes = models.TextField(blank=True, null=True)
      reference_no = models.CharField(max_length=20, unique=True,blank=False,null=False, default=RentMsUtils.generate_reference_number)
      created_at = models.DateTimeField(default=timezone.now)
      is_active = models.BooleanField(default=True)

      def __str__(self):
        return "{}".format(self.status,self.id,self.uuid)

      class Meta:
        db_table = "vilcom_orders"
        ordering = ["-id"]
        verbose_name_plural = "01. Vilcom Oders"


class VilcomOrderItem(models.Model):
        id = models.AutoField(primary_key=True)
        uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
        order = models.ForeignKey(VilcomOrder, related_name='vilcom_items', on_delete=models.CASCADE)
        # food = models.ForeignKey(VilcomFood,related_name='order_food',on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField()
        price = models.DecimalField(max_digits=8, decimal_places=2)
        created_at = models.DateTimeField(default=timezone.now)
        is_active =models.BooleanField(default=True)

        def get_total(self):
            return self.quantity * self.price
        
        def __str__(self):
            return "{}".format(self.price,self.id,self.uuid)
        
        class Meta:
            db_table = "vilcom_orders_items"
            ordering = ["-id"]
            verbose_name_plural = "02. Vilcom Oders Items"

class VilcomPayment(models.Model):
        id = models.AutoField(primary_key=True)
        uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
        order = models.OneToOneField(VilcomOrder,related_name='order_payment', on_delete=models.CASCADE)
        status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='Pending')
        method = models.CharField(max_length=20, choices=PAYMENT_METHOD,default='Cash')
        payment_type = models.CharField(max_length=20,choices=PAYMENT_TYPE,default='Full')
        transaction_id = models.CharField(max_length=100, blank=True, null=True)
        paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
        paid_at = models.DateTimeField(max_length=255, blank=True, null=True)
        created_at = models.DateTimeField(default=timezone.now)
        is_active =models.BooleanField(default=True)

        def __str__(self):
            return "{}".format(self.method,self.id,self.uuid)

        class Meta:
            db_table = "rent_ms_payment"
            ordering = ["-id"]
            verbose_name_plural = "03. Vilcom Payment"
