from django.contrib import admin
from .models.product import *
from .models.category import *
from .models.customer import *
from .models.tenders import *
from .models.events import *
from .models.partners import *
from .models.internship import *



class AdminProduct(admin.ModelAdmin):
    list_display = ['product_name', 'product_price', 'category', 'upload_date']
    list_filter = ['category']
    search_fields = ['product_name', 'category__name', 'status']
    fieldsets = (
        ('Product Details', {'fields': ['product_name', 'product_price', 'HSN_CODE', 'category', 'product_description', 'product_image',
                    'product_specification_boucher', 'status', 'gst']}),
        ('Product Image Option', {'fields': ['product_option_image_1', 'product_option_image_2', 'product_option_image_3',
                                             'product_option_image_4']}),

    )

@admin.register(Internship_Application)
class AdminInternship_Application(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'submit_date']
    list_filter = ['first_name', 'last_name', 'gender']
    search_fields = ['first_name', 'last_name', 'gender']
    fieldsets = (
        ('Personal Details', {'fields': ['first_name', 'last_name', 'gender', 'email', 'Phone', 'Address', 'Zipcode',
                                         'country', 'state', 'submit_date']}),
        ('Educational Qualifications', {'fields': ['highest_education', 'name_of_study', 'education_date_from', 'education_date_to']}),
        ('WORK EXPERCIENCE', {'fields': ['Organization', 'designation', 'date_from', 'date_to', 'responsibilities',
                                         'experience', 'resume']}),
    )

@admin.register(Latest_notification)
class AdminLatest_notification(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'status']
    list_filter = []
    search_fields = ['title', 'start_date', 'end_date', 'status']
    fieldsets = (
        ('Application Details', {'fields': ['title', 'description', 'job_description_pdf', 'start_date', 'end_date', 'status', 'upload_date']}),
    )
    readonly_fields = ['upload_date']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

#
# class AdminCustomer(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'phone', 'email', 'password']


class AdminTenders(admin.ModelAdmin):
    list_display = ['tenders_number', 'tenders_description', 'from_date', 'to_date',   'tenders_pdf']
    search_fields = ['tenders_number']

class AdminPartners(admin.ModelAdmin):
      list_display = ['partner_name', 'partner_image', 'update_date', 'status']
      search_fields = ['partner_name', 'status']


@admin.register(Qutation_request)
class Qutation_request(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'mobile_number', 'Product_name']
    list_filter = ['fullname', 'Product_name']
    search_fields = ['fullname', 'email', 'Product_name']
    fieldsets = (
        ('Customer Details', {'fields': ['fullname', 'email', 'mobile_number']}),
        ('Qutation For Product Details', {'fields': ['product_id', 'Product_name', 'quantity', 'other_product_name1',
                                                     'other_product_qty1', 'other_product_name2', 'other_product_qty2', 'subject', 'message']}),

    )

@admin.register(Contact_request)
class Contact_request(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'mobile_number']
    list_filter = ['fullname', 'email']
    search_fields = ['fullname', 'email', 'mobile_number']
    fieldsets = (
        ('Sender Details', {'fields': ['fullname', 'email', 'mobile_number']}),
        ('Message', {'fields': ['subject', 'message']}),

    )


@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display = ['event_name', 'Event_year', 'Start_date', 'end_date']
    list_filter = ['Event_year']
    search_fields = ['Event_year__Event_year']
    fieldsets = (
        ('Event Details', {'fields': ['Event_year', 'event_name', 'event_discription', 'event_picture', 'event_youtube_link_key', 'registration_form_urls']}),
        ('Event Date', {'fields': ['Start_date', 'end_date', 'status']}),

    )

@admin.register(Event_year)
class Event_year(admin.ModelAdmin):
    list_display = ['Event_year', 'status']
    list_filter = ['Event_year']
    search_fields = ['Event_year']

@admin.register(News)
class News(admin.ModelAdmin):
    list_display = ['news_title', 'news_date']
    search_fields = ['news_title', 'news_date', 'status']
    fieldsets = (
        ('News Details', {'fields': ['news_title', 'news_discription', 'news_picture',
                                     'news_youtube_link_key', 'news_date', 'status']}),

    )

@admin.register(Our_video)
class Our_video(admin.ModelAdmin):
    list_display = ['video_title', 'video_date']
    search_fields = ['video_title', 'video_date', 'status']
    fieldsets = (
        ('AMTZ Video', {'fields': ['video_title', 'video_date', 'video_youtube_link_key', 'video_Thumbnail_link', 'status']}),

    )

# Register your models here.
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
# admin.site.register(Customer, AdminCustomer)
admin.site.register(Tenders, AdminTenders)
admin.site.register(Partners, AdminPartners)

