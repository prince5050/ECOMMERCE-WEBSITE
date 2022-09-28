from django.db import models
from datetime import date

from django.db.models.fields import TextField


class Partners(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    update_date = models.DateField(default=date.today)
    partner_name = models.CharField(max_length=500, null=True)
    partner_image = models.ImageField(upload_to='uploads/partners/', null=True)
    partner_url= models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default=1)


    def __str__(self):
        return self.partner_name
