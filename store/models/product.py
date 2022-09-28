from django.db import models
from datetime import date

# from store.views import Product
from .category import Category


class Product(models.Model):
    status_list = (
        ('1', 'Active'),
        ('2', 'Deactive'),
        ('3', 'Delete')
    )
    discount_type_value = (
        ('0', 'N/A'),
        ('Rs', 'Flat Discount'),
        ('%', 'Percentage Discount')
    )
    gst_type = (
        ('0', 'N/A'),
        ('12', '12%'),
        ('18', '18%')
    )
    product_name = models.CharField(max_length=100, null=True)
    product_price = models.IntegerField(null=True, blank=True)
    HSN_CODE = models.CharField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    product_image = models.ImageField(upload_to='uploads/products/', null=True)
    product_option_image_1 = models.ImageField(upload_to='uploads/products-Option-image/', null=True, blank=True)
    product_option_image_2 = models.ImageField(upload_to='uploads/products-Option-image/', null=True, blank=True)
    product_option_image_3 = models.ImageField(upload_to='uploads/products-Option-image/', null=True, blank=True)
    product_option_image_4 = models.ImageField(upload_to='uploads/products-Option-image/', null=True, blank=True)
    product_specification_boucher = models.FileField(upload_to='uploads/products/specification', max_length=500, null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_list, default='1')
    gst = models.CharField(max_length=50, choices=gst_type, default='0')
    discount_type = models.CharField(max_length=50, choices=discount_type_value, default='0')
    discount_amount_or_per = models.IntegerField(default=0)
    product_description = models.TextField(null=True)
    upload_date = models.DateField(auto_now=date.today, null=True, blank=True)

    def __str__(self):
        return self.product_name



    @staticmethod
    def get_all_products():
        return Product.objects.filter(status='1')
    
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id, status='1')
        else:
            return Product.get_all_products();

class Qutation_request(models.Model):
    product_id = models.IntegerField()
    Product_name = models.CharField(max_length=250, blank=True, null=True)
    other_product_name1 = models.CharField(max_length=250, blank=True, null=True)
    other_product_name2 = models.CharField(max_length=250, blank=True, null=True)
    other_product_qty1 = models.CharField(max_length=80, blank=True, null=True)
    other_product_qty2 = models.CharField(max_length=80, blank=True, null=True)
    fullname = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    message = models.TextField(default='')
    quantity = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.product_name

class Contact_request(models.Model):
    fullname = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    message = models.TextField(default='')

    def __str__(self):
        return self.fullname
