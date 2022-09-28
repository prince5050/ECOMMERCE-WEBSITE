from datetime import date, timezone

from django.db import models
from django.contrib.auth.models import User
from store.models import *

# Create your models here.
class user_role(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    alternative_mobile = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default=1)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

class Cart(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    Ord_status = (
        ('1', 'Pending'),
        ('2', 'Order Placed'),
        ('3', 'Invoice generated')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    gst_amount = models.IntegerField(null=True, blank=True)
    gst_with_product_QTY = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    payable_price_withGST = models.IntegerField(null=True, blank=True)
    payable_price_withoutGST = models.IntegerField(null=True, blank=True)
    quantity = models.CharField(max_length=100, default=1)
    total_product_QTY = models.IntegerField(null=True, blank=True)
    total_price_with_QTY = models.IntegerField(null=True, blank=True)
    total_price_without_gst_QTY = models.IntegerField(null=True, blank=True)
    total_gst_with_QTY = models.IntegerField(null=True, blank=True)
    add_date = models.DateField(auto_now=date.today, null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default=1)
    order_status = models.CharField(max_length=50, choices=Ord_status, default=1)

    def __str__(self):
        return self.product.product_name

class Direct_buy_bag(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.CharField(max_length=100, default=1)
    gst_amount = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    payable_price = models.IntegerField(null=True, blank=True)
    add_date = models.DateField(auto_now=date.today, null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default=1)
    def __str__(self):
        return self.product.product_name

class Country(models.Model):
    country_name = models.CharField(max_length=60, default="")
    sortname = models.CharField(max_length=60, default="")
    phonecode = models.CharField(max_length=60, default="")

    def __str__(self):
        return self.country_name

class State(models.Model):
    state_name = models.CharField(max_length=60, default="")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.state_name

class Address(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    fullname = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=100, default='')
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    address1 = models.TextField()
    address2 = models.TextField()
    landmark = models.TextField()
    billing_fullname = models.CharField(max_length=150, null=True, blank=True)
    billing_mobile = models.CharField(max_length=15, null=True, blank=True)
    billing_email = models.CharField(max_length=80, null=True, blank=True)
    billing_country = models.CharField(max_length=150, null=True, blank=True)
    billing_state = models.CharField(max_length=150, null=True, blank=True)
    billing_city = models.CharField(max_length=100, null=True, blank=True)
    billing_pincode = models.CharField(max_length=20, null=True, blank=True)
    billing_address1 = models.TextField(null=True, blank=True)
    billing_address2 = models.TextField(null=True, blank=True)
    billing_landmark = models.TextField(null=True, blank=True)
    billing_gst_no = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status_list, default=1)

    def __str__(self):
        return self.address2

class Order(models.Model):
    status_list = (
        ('1', 'PENDING'),
        ('2', 'SUCCESS'),
        ('3', 'FAILED'),
        ('4', 'AMOUNT Tampered')
    )
    order = (
        ('1', 'not Packed'),
        ('2', 'packed'),
        ('3', 'ON The Way'),
        ('4', 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    order_Id = models.TextField(primary_key=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    cart = models.CharField(max_length=200, null=True, blank=True)
    txn_id = models.CharField(max_length=200, blank=True, null=True)
    Invoice_number = models.CharField(max_length=200, null=True, blank=True)
    order_date = models.DateTimeField(auto_now=True)
    amount_initiated = models.FloatField(blank=True, null=True)
    Date_of_payment = models.DateTimeField(null=True, blank=True)
    payment_mode = models.CharField(max_length=200, null=True, blank=True)
    order_status = models.CharField(max_length=50, choices=order, default='1')
    Payment_status = models.CharField(max_length=50, choices=status_list, default='1')
    email = models.EmailField(max_length=30, blank=True, null=True)
    log = models.TextField(null=True, blank=True)
    tracking_id = models.CharField(max_length=1000, blank=True, null=True)
    was_success = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order_Id}'

    # def __str__(self):
    #     return self.user.first_name


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    invoice_no = models.CharField(max_length=500, null=True, blank=True)
    order_Id = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    invoice_document = models.FileField(upload_to='uploads/products-Invoice/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.user.id} [{self.invoice_no}]'


class Order_Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_Id = models.ForeignKey(Order, on_delete=models.CASCADE, default="")
    Product_name = models.CharField(max_length=300, null=True, blank=True)
    Product_amount = models.CharField(max_length=100, null=True, blank=True)
    Total_gst_amount = models.CharField(max_length=100, null=True, blank=True)
    Total_price_without_gst = models.CharField(max_length=100, null=True, blank=True)
    Product_qty = models.CharField(max_length=100, null=True, blank=True)
    product_image = models.FileField(upload_to='uploads/product_order/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.order_Id} '