from django.db import models
import uuid


class RentReport(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    report_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.report_name)

    class Meta:
        db_table = "rent_ms_report"
        ordering = ["-id"]
        verbose_name_plural = "01. Report"






































    
