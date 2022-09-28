from datetime import datetime

from django.db import models

from ecommerce.models import User
# Create your models here.
class RoomManager(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="uploads/room_manager", height_field=None, width_field=None, max_length=None, blank=True)
    phone_no = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    def __str__(self):
        return "Room Manager: "+self.email


class Rooms(models.Model):
    manager = models.ForeignKey(RoomManager, on_delete=models.CASCADE)
    room_no = models.CharField(max_length=10, primary_key=True)
    room_type = models.CharField(max_length=50)
    room_discription = models.TextField()
    is_available = models.BooleanField(default=True)
    Booked_by_admin = models.BooleanField(default=False)
    price = models.FloatField(default=1000.00)
    no_of_days_advance = models.IntegerField()
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    room_image = models.ImageField(upload_to="uploads/room_photos", height_field=None, width_field=None, max_length=None,default='0.jpeg')
    def __str__(self):
        return str(self.room_no)


class Room_Order(models.Model):
    Ord_status = (
        ('1', 'Pending'),
        ('2', 'Success'),
        ('3', 'Failed')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    room_no = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING)
    order_number = models.TextField(primary_key=True)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True, default=3000)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=80, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    adult_no = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=50, choices=Ord_status, default=1)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order_number)

class Book_By_admin(models.Model):
    room_status = (
        ('1', 'Booked'),
        ('2', 'Not Book')
    )
    room_no = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING)
    Guest_name = models.CharField(max_length=200, null=True, blank=True)
    Guest_mobile = models.CharField(max_length=20, null=True, blank=True)
    Guest_email = models.CharField(max_length=80, null=True, blank=True)
    adult_no = models.CharField(max_length=20, null=True, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    Total_price = models.FloatField(null=True, blank=True, default=3000)
    Booking_remark = models.CharField(max_length=700, blank=True, null=True)
    Booked_by = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, choices=room_status, default='1')
    cancelled_remark = models.CharField(max_length=700, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.Guest_name)
class Booking_room(models.Model):
    Pay_status = (
        ('1', 'Pending'),
        ('2', 'Success'),
        ('3', 'Failed')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order_number = models.ForeignKey(Room_Order, on_delete=models.DO_NOTHING, default='')
    room_no = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING, default='')
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    Invoice_number = models.CharField(max_length=200, null=True, blank=True)
    txn_id = models.CharField(max_length=200, blank=True, null=True)
    amount_initiated = models.FloatField(blank=True, null=True)
    Date_of_payment = models.DateTimeField(null=True, blank=True)
    payment_mode = models.CharField(max_length=200, null=True, blank=True)
    Payment_status = models.CharField(max_length=50, choices=Pay_status, default='1')
    log = models.TextField(null=True, blank=True)
    was_success = models.BooleanField(default=False)
    invoice_document = models.FileField(upload_to='uploads/Room-Invoice/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order_number)


class Room_Picture(models.Model):
    room_no = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    room_image_discription = models.TextField(null=True, blank=True)
    room_picture = models.ImageField(upload_to="uploads/room_photos", height_field=None, width_field=None, max_length=None, default='0.jpeg')
    def __str__(self):
        return str(self.room_no)

class Room_invoice(models.Model):
    invoice_no = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'[{self.invoice_no}]'
