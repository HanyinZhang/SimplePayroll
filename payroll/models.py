from django.db import models


# Create your models here.
class TimeSheet(models.Model):
    class Meta:
        unique_together = ('date', 'employee_id')

    date = models.DateField()
    hours = models.DecimalField(decimal_places=1, max_digits=3)
    employee_id = models.CharField(max_length=16)
    job_group = models.CharField(max_length=32)
    pay_period = models.DateField()
    pay_rate = models.DecimalField(decimal_places=2, max_digits=10)


class TimeReport(models.Model):
    report_id = models.CharField(max_length=16, primary_key=True)
    identifier = models.CharField(max_length=32)
    upload_time = models.DateTimeField()
