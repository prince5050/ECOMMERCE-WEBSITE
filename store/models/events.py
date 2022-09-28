from django.db import models
from datetime import date
class Event_year(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    Event_year = models.CharField(primary_key=True, max_length=100)
    status = models.CharField(max_length=50, choices=status_list, default='1')
    def __str__(self):
        return self.Event_year

class Event(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    Event_year = models.ForeignKey(Event_year, on_delete=models.CASCADE, default='')
    event_name = models.CharField(max_length=500)
    event_picture = models.FileField(upload_to='uploads/events/', null=True, blank=True)
    event_discription = models.TextField(blank=True, null=True)
    event_youtube_link_key = models.CharField(max_length=100, blank=True, null=True)
    registration_form_urls = models.CharField(max_length=250, blank=True, null=True)
    Start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default='1')

    def __str__(self):
        return self.event_name

class News(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )

    news_title = models.CharField(max_length=500)
    news_picture = models.FileField(upload_to='uploads/events/', null=True, blank=True)
    news_discription = models.TextField(blank=True, null=True)
    news_youtube_link_key = models.CharField(max_length=100, blank=True, null=True)
    news_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default='1')

    def __str__(self):
        return self.news_title

class Our_video(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )

    video_title = models.CharField(max_length=500, null=True, blank=True)
    video_youtube_link_key = models.CharField(max_length=500, blank=True, null=True)
    video_Thumbnail_link = models.CharField(max_length=500, blank=True, null=True)
    video_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default='1')

    def __str__(self):
        return self.video_title