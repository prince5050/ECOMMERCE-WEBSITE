from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(RoomManager)
class RoomManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_no')
    list_filter = []
    search_fields = ['name', 'email']
    fieldsets = (
        ('Room Manager', {'fields': ('name', 'email', 'phone_no', 'gender', 'profile_pic')}),

     )

@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ('manager', 'room_no', 'price')
    list_filter = []
    search_fields = ['manager__name', 'room_no', 'price']
    fieldsets = (
        ('Room Manager', {'fields': ('manager', 'room_no', 'room_type', 'room_discription', 'price',
                                     'no_of_days_advance', 'start_date', 'room_image', 'is_available', 'Booked_by_admin')}),

     )

@admin.register(Room_Picture)
class Room_PictureAdmin(admin.ModelAdmin):
    list_display = ('room_no', 'room_image_discription', 'room_picture')
    list_filter = []
    search_fields = ['room_no__room_no', ]
    fieldsets = (
        ('Room Manager', {'fields': ('room_no', 'room_image_discription', 'room_picture')}),

     )
@admin.register(Room_invoice)
class Room_invoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_no', 'created_at']
    search_fields = ['invoice_no', 'created_at']
    fieldsets = (
        (None, {'fields': ['invoice_no', 'created_at']}),

    )
    readonly_fields = ['created_at']
@admin.register(Room_Order)
class Room_OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_number', 'room_no',  'status')
    list_filter = []
    search_fields = ['room_no__room_no', 'order_number', 'status']
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Order Details', {'fields': ('order_number', 'room_no', 'check_in', 'check_out', 'price', 'status', 'created_at')}),
        ('Customer',
         {'fields': ('name', 'mobile', 'email', 'adult_no')}),

    )
    readonly_fields = ['created_at']

@admin.register(Book_By_admin)
class Book_By_adminAdmin(admin.ModelAdmin):
    list_display = ('Guest_name', 'Guest_mobile', 'room_no', 'check_in', 'check_out', 'status', 'created_at')
    list_filter = []
    search_fields = ['room_no__room_no', 'Guest_name', 'Guest_mobile' 'created_at']
    fieldsets = (
        ('Guest',
         {'fields': ('Guest_name', 'Guest_mobile', 'Guest_email')}),
        ('Guest Booking Details', {'fields': ('room_no', 'adult_no', 'check_in', 'check_out', 'Total_price', 'Booking_remark', 'Booked_by', 'cancelled_remark', 'created_at', 'status')}),
 )
    readonly_fields = ['created_at']


@admin.register(Booking_room)
class Booking_roomAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_number', 'Invoice_number', 'room_no', 'check_in', 'check_out', 'Payment_status')
    list_filter = []
    search_fields = ['user__email', 'order_number__order_number', 'room_no__room_no',  'Invoice_number', 'Payment_status']
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Booking Details', {'fields': ('order_number', 'room_no', 'check_in', 'check_out', 'Invoice_number', 'invoice_document',)}),
        ('Payment Details',
         {'fields': ('txn_id', 'amount_initiated', 'Date_of_payment', 'payment_mode', 'Payment_status', 'log',
                     'was_success', 'created_at')}),

    )
    readonly_fields = ['created_at']
