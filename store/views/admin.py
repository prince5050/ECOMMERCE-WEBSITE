from django.contrib import admin
from .models.product import *
from .models.category import *
from .models.customer import *
from .models.tenders import *
from .models.events import *
from .models.partners import *



class AdminProduct(admin.ModelAdmin):
    list_display = ['product_name', 'product_price', 'category', 'upload_date',]
    list_filter = ['product_name', 'category', 'status']
    search_fields = ['product_name', 'category', 'status']
    fieldsets = (
        ('Product Details', {'fields': ['product_name', 'product_price', 'category', 'product_description', 'product_image',
                    'product_specification_boucher', 'status', 'gst',  'discount_type', 'discount_amount_or_per']}),
        ('Product Image Option', {'fields': ['product_option_image_1', 'product_option_image_2', 'product_option_image_3',
                                             'product_option_image_4']}),

    )


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'password']


class AdminTenders(admin.ModelAdmin):
    list_display = ['from_date', 'to_date', 'tenders_number', 'tenders_description', 'tenders_pdf']


class AdminPartners(admin.ModelAdmin):
      list_display = ['update_date', 'partner_name', 'partner_image', 'partner_url','status']





@admin.register(Qutation_request)
class Qutation_request(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'mobile_number', 'Product_name']
    list_filter = ['fullname', 'Product_name']
    search_fields = ['fullname', 'email', 'Product_name']
    fieldsets = (
        ('Customer Details', {'fields': ['fullname', 'email', 'mobile_number']}),
        ('Qutation For Product Details', {'fields': ['product_id', 'Product_name', 'quantity', 'subject', 'message']}),

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
    list_display = ['event_name', 'Start_date', 'end_date']
    list_filter = ['event_name', 'Start_date', 'end_date']
    search_fields = ['event_name', 'Start_date', 'end_date']
    fieldsets = (
        ('Event Details', {'fields': ['event_name', 'event_discription', 'event_picture', 'event_youtube_link_key', 'registration_form_urls']}),
        ('Event Date', {'fields': ['Start_date', 'end_date', 'status']}),

    )

@admin.register(News)
class News(admin.ModelAdmin):
    list_display = ['news_title', 'news_date']
    list_filter = ['news_title', 'news_date']
    search_fields = ['news_title', 'news_date']
    fieldsets = (
        ('News Details', {'fields': ['news_title', 'news_discription', 'news_picture',
                                     'news_youtube_link_key', 'news_date']}),

    )


# Register your models here.
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Tenders, AdminTenders)
admin.site.register(Partners, AdminPartners)

