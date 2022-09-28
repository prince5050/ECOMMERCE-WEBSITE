from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('sortname', 'country_name', 'phonecode')
    list_filter = []
    search_fields = ['country_name', 'sortname']
    fieldsets = (
        (None, {'fields': ('sortname', 'country_name', 'phonecode')}),

     )

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['country', 'state_name']
    list_filter = []
    search_fields = ['state_name']
    fieldsets = (
        (None, {'fields': ('country', 'state_name')}),

    )
@admin.register(user_role)
class user_roleAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile', 'alternative_mobile',  'role', 'status']
    list_filter = ['user', 'role']
    search_fields = ['user__email', 'role']
    fieldsets = (
        ('User Details', {'fields': ['user', 'mobile', 'alternative_mobile', 'role', 'auth_token', 'status', 'is_verified']}),


)
    # readonly_fields = ['last_login']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'status']
    list_filter = ['user', 'product']
    search_fields = ['user__email', 'product__product_name', 'status']
    fieldsets = (
        (None, {'fields': ['user']}),
        ('Product Details', {'fields': ['product', 'gst_amount', 'gst_with_product_QTY', 'total_price', 'quantity',
                                        'total_product_QTY', 'total_price_without_gst_QTY',
                                        'total_price_with_QTY', 'total_gst_with_QTY',
                                        'payable_price_withoutGST', 'payable_price_withGST', 'add_date', 'order_status', 'status']}),

)
    readonly_fields = ['add_date']

@admin.register(Direct_buy_bag)
class Direct_buy_bagAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'payable_price', 'add_date', 'status']
    list_filter = []
    search_fields = ['user__email', 'product__product_name', 'status']
    fieldsets = (
        (None, {'fields': ['user']}),
        ('Product Details', {'fields': ['product',  'quantity', 'total_price', 'gst_amount',
                                        'payable_price', 'add_date', 'status']}),

)
    readonly_fields = ['add_date']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'mobile', 'pincode', 'status']
    list_filter = ['pincode', 'status']
    search_fields = ['fullname', 'mobile', 'pincode', 'status']
    fieldsets = (
        (None, {'fields': ['user']}),
        ('Customer Shipping Address', {'fields': ['fullname', 'mobile', 'email', 'country', 'state', 'city', 'pincode', 'address1',
                                        'address2', 'landmark', 'created_at', 'status']}),
        ('Customer Shipping Address',
         {'fields': ['billing_fullname', 'billing_mobile', 'billing_email', 'billing_country', 'billing_state', 'billing_city',
                     'billing_pincode', 'billing_address1',
                     'billing_address2', 'billing_landmark']}),

)
    readonly_fields = ['created_at']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',  'order_Id', 'Invoice_number', 'Date_of_payment', 'order_status', 'Payment_status', 'tracking_id']
    list_filter = ['Date_of_payment', 'order_status', 'Payment_status']
    search_fields = ['user__email',  'Date_of_payment', 'order_Id', 'Invoice_number',  'order_status', 'Payment_status', 'tracking_id']
    fieldsets = (
        (None, {'fields': ['user']}),
        ('Order Details', {'fields': ['order_Id', 'Invoice_number', 'email', 'address', 'cart', 'order_status', 'order_date', 'log', 'tracking_id']}),
        ('Payment Details', {
            'fields': ['amount_initiated', 'txn_id', 'Date_of_payment', 'payment_mode', 'Payment_status', 'was_success']}),

    )
    readonly_fields = ['order_date']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'invoice_no', 'order_Id']
    list_filter = ['user']
    search_fields = ['user__email', 'order_Id__order_Id', 'invoice_no']
    fieldsets = (
        (None, {'fields': ['user']}),
        ('Customer Address', {'fields': ['invoice_no', 'order_Id', 'invoice_document', 'created_at']}),

)
    readonly_fields = ['created_at']

@admin.register(Order_Product)
class Order_ProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_Id', 'Product_name', 'Product_amount', 'created_at']
    list_filter = []
    search_fields = ['user__email', 'order_Id__order_Id', 'Product_name', 'Product_amount']
    fieldsets = (
        (None, {'fields': ['order_Id']}),
        ('Customer Address', {'fields': ['Product_name', 'Product_amount',  'Total_price_without_gst', 'Total_gst_amount', 'Product_qty', 'product_image', 'created_at']}),

)
    readonly_fields = ['created_at']
