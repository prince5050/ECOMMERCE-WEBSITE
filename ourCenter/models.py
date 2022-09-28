from django.db import models


# Create your models here.

class Center(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    center_title = models.CharField(max_length=100, null=True)
    center_description = models.TextField(blank=True, null=True)
    center_image = models.ImageField(upload_to='uploads/center/', null=True, blank=True)
    center_video_key = models.CharField(max_length=500, null=True, blank=True)
    center_brochure = models.FileField(upload_to='uploads/center/', null=True, blank=True)
    meta_title = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    image_title = models.TextField(null=True, blank=True)
    image_alt = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default=1)

    # @staticmethod
    # def get_all_tenders():
    #     return Tenders.objects.all()
    def __str__(self):
        return self.center_title

class OurHub(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    hub_title = models.CharField(max_length=100, null=True, blank=True)
    hub_description = models.TextField(blank=True, null=True)
    hub_image = models.ImageField(upload_to='uploads/Hub/', null=True, blank=True)
    hub_video_key = models.CharField(max_length=500, null=True, blank=True)
    hub_link = models.CharField(max_length=500, null=True, blank=True)
    image_title = models.TextField(null=True, blank=True)
    image_alt = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default=1)

    # @staticmethod
    # def get_all_tenders():
    #     return Tenders.objects.all()
    def __str__(self):
        return self.hub_title

class OurService(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    service_title = models.CharField(max_length=100, null=True, blank=True)
    service_description = models.TextField(blank=True, null=True)
    service_use1 = models.CharField(max_length=100, blank=True, null=True)
    service_use2 = models.CharField(max_length=100, blank=True, null=True)
    service_use3 = models.CharField(max_length=100, blank=True, null=True)
    service_use4 = models.CharField(max_length=100, blank=True, null=True)
    service_use5 = models.CharField(max_length=100, blank=True, null=True)
    service_image = models.ImageField(upload_to='uploads/Services/', null=True, blank=True)
    service_poster = models.ImageField(upload_to='uploads/Services/poster', null=True, blank=True)
    service_pdf = models.FileField(upload_to='uploads/Services/pdf', max_length=500, null=True, blank=True)
    service_video_key = models.CharField(max_length=500, null=True, blank=True)
    service_link = models.CharField(max_length=1000, null=True, blank=True)
    contact_email = models.CharField(max_length=100, null=True, blank=True)
    meta_title = models.TextField(null=True, blank=True)
    meta_discription = models.TextField(null=True, blank=True)
    image_title = models.TextField(null=True, blank=True)
    image_alt = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default=1)

    def __str__(self):
        return self.service_title

class Service_Contact_request(models.Model):
    fullname = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    message = models.TextField()
    service_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.fullname