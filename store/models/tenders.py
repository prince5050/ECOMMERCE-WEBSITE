from django.db import models
from datetime import date


class Tenders(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    from_date = models.DateField(default=date.today)
    to_date = models.DateField(default=date.today)
    tenders_number = models.CharField( max_length=100, blank=True, null=True)
    tenders_description = models.TextField(blank=True)
    tenders_pdf = models.FileField(upload_to='uploads/tenders/', max_length=500)
    status = models.CharField(max_length=50, choices=status_list, default=1)
    # @staticmethod
    # def get_all_tenders():
    #     return Tenders.objects.all()
    def __str__(self):
        return self.tenders_description
