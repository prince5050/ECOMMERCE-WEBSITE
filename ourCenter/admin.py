from django.contrib import admin
from .models import *


# Register your models here.

class AdminCenter(admin.ModelAdmin):
    list_display = ['center_title', 'center_description', 'center_image', 'center_video_key', 'center_brochure', 'status']


admin.site.register(Center, AdminCenter)


@admin.register(OurHub)
class AdminOurHub(admin.ModelAdmin):
    list_display = ['hub_title', 'hub_description', 'hub_image', 'hub_link', 'hub_video_key', 'image_title', 'image_alt', 'status']

@admin.register(OurService)
class AdminOurService(admin.ModelAdmin):
    list_display = ['service_title', 'service_description', 'status']
    list_filter = ['service_title']
    search_fields = ['service_title']
    fieldsets = (
        ('Service Details', {'fields': ['service_title', 'service_description', 'service_use1', 'service_use2', 'service_use3',
                                        'service_use4', 'service_use5', 'service_pdf',
                                       'service_image', 'service_poster', 'service_link', 'service_video_key', 'contact_email',
                                        'meta_title', 'meta_discription','image_title', 'image_alt', 'status']}),
)
@admin.register(Service_Contact_request)
class AdminService_Contact_request(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'mobile_number', 'service_name']
    list_filter = []
    search_fields = ['email', 'mobile_number', 'service_name']
    fieldsets = (
        ('Service Details', {'fields': ['fullname', 'email', 'mobile_number' 'subject', 'message', 'service_name']}),
)

