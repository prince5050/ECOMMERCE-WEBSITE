from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from ourCenter.models import Center as CentersModels
from ourCenter.models import *
from store.models.events import Event_year
from store.models.product import *


# Create your views here.
from store.views.home import Cart_Count


def our_center(request):
        Cart_Count(request)
        cart_count = settings.CART_COUNT
        event_year = Event_year.objects.filter(status='1')
        center_list = CentersModels.objects.filter(status=1).order_by('-id').reverse
        return render(request, 'ourCenter.html', {'centers': center_list, 'cart_count': cart_count, 'event_year': event_year})

def whocc(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'whocc.html', {'cart_count': cart_count, 'event_year': event_year})
def centerDetails(request, name):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    product_id = request.GET["key"]
    center_list = CentersModels.objects.get(pk=product_id)
    return render(request, 'centerDetails.html', {'centers_details': center_list, 'cart_count': cart_count, 'event_year': event_year})

def service_contact(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        subject = request.POST['subject']
        message = request.POST['message']
        ser_obj = OurService.objects.filter(id=id)[0]
        ser_name = ser_obj.service_title
        recipient_email = ser_obj.contact_email
        Service_Contact_request.objects.create(fullname=name, email=email,  mobile_number=mobile,
                                       subject=subject, message=message, service_name=ser_name)

        send_mail_service(ser_name, name, email, mobile, subject, message, recipient_email)
        messages.success(request, "Query Request successfully send")
        return redirect('service_details', id=id)

    else:
        messages.error(request, "Something Went Wrong try again")
        return redirect('service_details', id=id)

def send_mail_service(ser_name, name, email, mobile, user_subject, message, recipient_email):
    subject = f'Query Request From {ser_name} Service of  Amtz Website'
    message = f'Hello,\n     AMTZ Team \n     This mail is come from your Amtz website \n' \
              f'     {name} want to Contact related to {user_subject}\n \n' \
              f'     Sender Name : {name}\n     Email : {email}\n     Sender Mobile Number : {mobile}\n\n' \
              f'     Subject : {user_subject}\n' \
              f'     Message : \n     {message}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    send_mail(subject, message, email_from, recipient_list)