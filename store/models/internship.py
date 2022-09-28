from django.db import models
from datetime import date

from django.db.models.fields import TextField

class Internship_Application(models.Model):
    submit_date = models.DateField(default=date.today)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    Phone = models.CharField(max_length=100, blank=True, null=True)
    Address = models.CharField(max_length=500, blank=True, null=True)
    Zipcode = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    highest_education = models.CharField(max_length=300, blank=True, null=True)
    name_of_study = models.CharField(max_length=100, blank=True, null=True)
    education_date_from = models.CharField(max_length=100, blank=True, null=True)
    education_date_to = models.CharField(max_length=100, blank=True, null=True)
    Organization = models.CharField(max_length=150, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    date_from = models.CharField(max_length=100, blank=True, null=True)
    date_to = models.CharField(max_length=100, blank=True, null=True)
    responsibilities = models.CharField(max_length=200, blank=True, null=True)
    experience = models.CharField(max_length=150, blank=True, null=True)
    resume = models.FileField(upload_to='uploads/Internship_Application_cv/')

    def __str__(self):
        return self.first_name


class Latest_notification(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    job_description_pdf = models.FileField(upload_to='uploads/Latest_notification/')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, choices=status_list, default='1')
    upload_date = models.DateField(auto_now=date.today)

    def __str__(self):
        return self.title