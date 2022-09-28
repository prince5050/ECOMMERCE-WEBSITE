from datetime import datetime
from django.core.cache import cache
from django.contrib import messages
from django.core.files import File
from num2words import num2words
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from ecommerce.models import *
from room_booking.models import Booking_room
from store.models import *
from django.contrib.auth import login
from django.contrib.auth.models import User

from store.models.events import Event_year
from store.views.home import Cart_Count
import uuid
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django_billdesk import ResponseMessage, GetMessage
from django.contrib.auth import logout
import random
import string
from django.contrib.auth import update_session_auth_hash
import requests

# Create your views here.
def signup(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:

            if User.objects.filter(email=email).first() and user_role.objects.filter(role='user'):
                return render(request, 'auth/signup.html', {'error': 'Email is already taken. Try with another'})
            else:
                user_obj = User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name,
                                                        password=password)
                user_obj.save()
                auth_token = str(uuid.uuid4())
                role = 'user'
                user_role_obj = user_role.objects.create(user=user_obj, auth_token=auth_token, role=role)
                user_role_obj.save()
                set_url = request._current_scheme_host
                send_mail_after_registration(first_name, last_name, set_url, auth_token, email)
                return render(request, 'auth/login.html',
                                  {'message': 'Verification mail is send to Your register email id', 'cart_count': cart_count,
                                   'event_year': event_year})

        else:

            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('signup')
    else:
        return render(request, 'auth/signup.html', {'cart_count': cart_count, 'event_year': event_year})


def verify(request, auth_token):
    user_obj = user_role.objects.filter(auth_token=auth_token).first()

    if user_obj:
        if user_obj.is_verified:
            return render(request, 'confirmation/verify.html',
                          {'message': 'Your account is already verified . you can Sign In'})

        else:
            user_obj.is_verified = True
            user_obj.save()
            return render(request, 'confirmation/verify.html',
                          {'message': 'verification Successful . you can Sign In'})
    else:
        return render(request, 'confirmation/error.html')


def custom_login(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    if request.method == 'GET':
        Next = request.GET.get('next')
        cache.set('next', Next)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                user_role_obj = user_role.objects.filter(user=user).first()
                if user_role_obj.is_verified:
                    if user_role_obj.role == 'user':
                        next_url = cache.get('next')
                        if next_url:
                            cache.delete('next')
                            return HttpResponseRedirect(next_url)
                        else:
                            return redirect('/user-dashboard/')
                    else:
                        return render(request, 'auth/login.html', {'cart_count': cart_count, 'event_year': event_year})
                else:
                    return render(request, 'auth/login.html', {'error': 'Account not verify. Please Verify account '
                                                                        'Varification mail send to your registration email',
                                                               'cart_count': cart_count, 'event_year': event_year})
            else:
                return render(request, 'auth/login.html',
                              {'error': 'Invalid Password. Try with correct Password', 'cart_count': cart_count,
                               'event_year': event_year})

        except:
            return render(request, 'auth/login.html',
                          {'error': 'Invalid Email. Try with correct Email', 'cart_count': cart_count,
                           'event_year': event_year})
    else:
        return render(request, 'auth/login.html', {'cart_count': cart_count, 'event_year': event_year})


def send_mail_after_registration(first_name, last_name, set_url, auth_token, email):
    subject = 'Confirmation: your AMTZ account has been created'
    message = f'Hello {first_name} {last_name},\nThank you for completing your registration.\n \n' \
              f'We would like to confirm that your account has been created successfully. To access your account, click the link below.\n\n' \
              f'Confirm your registration here : {set_url}/verify/{auth_token} \n \n' \
              f'If you experience any issues logging into your account, reach out to us at info@amtz.in .\n\n'\
              f'Best,\n'\
              f'AMTZ team'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


@login_required(login_url='/login/')
def cart(request):
    request.session['buy_type'] = 'Add_to_cart'

    try:
        Cart_Count(request)
        cart_count = settings.CART_COUNT
        event_year = Event_year.objects.filter(status='1')
        user_id = request.user.id
        net_price = 0
        total_gst = 0
        price_without_gst = 0
        total_qty = 0
        product_details = Cart.objects.filter(user_id=user_id, status='1').order_by('add_date').reverse()

        for product in product_details:
            net_price = net_price + int(product.payable_price_withGST)
            total_gst = total_gst + int(product.gst_with_product_QTY)
            price_without_gst = price_without_gst + int(product.payable_price_withoutGST)
            total_qty = total_qty + int(product.quantity)

        for p in product_details:
            p.total_price_with_QTY = net_price
            p.total_gst_with_QTY = total_gst
            p.total_price_without_gst_QTY = price_without_gst
            p.total_product_QTY = total_qty
            p.save()
        product_value = Cart.objects.filter(user_id=user_id, status='1').order_by('add_date').reverse()
        return render(request, 'cart/cart.html',
                      {'product_details': product_value, 'cart_count': cart_count, 'event_year': event_year,
                       'net_price': net_price, 'total_gst': total_gst, 'total_qty': total_qty,
                       'price_without_gst': price_without_gst})
    except:
        return redirect('login')


@login_required(login_url='/login/')
def Add_cart(request, id):
    try:
        Cart_Count(request)
        cart_count = settings.CART_COUNT
        event_year = Event_year.objects.filter(status='1')
        product_details = Product.objects.filter(id=id)
        for cat in product_details:
            category = cat.category
        product_category = Product.objects.filter(category=category)[0:8]
        user_id = request.user.id
        if Cart.objects.filter(user_id=user_id, product_id=id, status='1'):

            return render(request, 'cart/add_to_cart.html',
                          {'cart_count': cart_count, 'product_details': product_details,
                           'categories': product_category, 'event_year': event_year,
                           })
        # 'msg': 'you add one more Quantity of'
        else:
            for i in product_details:
                old_price = i.product_price
                price = int(old_price)
                gst = i.gst
                gst_amount = float((price * int(gst)) / 100)
                total_price = price + gst_amount
                payable_price = total_price
                cart_obj = Cart.objects.create(user_id=user_id, product_id=id, gst_amount=gst_amount,
                                               total_price=total_price,
                                               payable_price_withGST=payable_price, total_price_with_QTY=total_price,
                                               total_gst_with_QTY=gst_amount, payable_price_withoutGST=old_price,
                                               total_price_without_gst_QTY=old_price, gst_with_product_QTY=gst_amount,
                                               total_product_QTY=1
                                               )
                cart_obj.save()
                Cart_Count(request)
                cart_count = settings.CART_COUNT
            return render(request, 'cart/add_to_cart.html',
                          {'cart_count': cart_count, 'product_details': product_details,
                           'categories': product_category, 'event_year': event_year})

    except:
        return redirect('product_page')


@login_required(login_url='/login/')
def delete_product(request, product_id):
    cart_obj = Cart.objects.filter(product_id=product_id, status='1')
    for cart in cart_obj:
        cart.status = '2'
    cart.save()
    Cart_Count(request)
    return redirect('cart')


@login_required(login_url='/login/')
def quantity_change(request):
    net_price = 0
    total_gst = 0
    price_without_gst = 0
    total_qty = 0
    quantity = request.POST.get('quantity')
    product_id = request.POST.get('id')
    user_id = request.user.id
    cart_obj = Cart.objects.filter(user_id=user_id, product_id=product_id, status='1')
    product_value = Cart.objects.filter(user_id=user_id, status='1').order_by('add_date').reverse()
    for cart in cart_obj:
        cart.quantity = quantity
        payable_price_withGST = int(cart.total_price) * int(quantity)
        cart.payable_price_withGST = payable_price_withGST
        payable_price_withoutGST = int(cart.product.product_price) * int(quantity)
        cart.payable_price_withoutGST = payable_price_withoutGST
        payable_gst = int(cart.gst_amount) * int(quantity)
        cart.gst_with_product_QTY = payable_gst

        cart.save()

    for product in product_value:
        net_price = net_price + int(product.payable_price_withGST)
        total_gst = total_gst + int(product.gst_with_product_QTY)
        price_without_gst = price_without_gst + int(product.payable_price_withoutGST)
        total_qty = total_qty + int(product.quantity)

    for p in cart_obj:
        p.total_price_with_QTY = net_price
        p.total_gst_with_QTY = total_gst
        p.total_price_without_gst_QTY = price_without_gst
        p.total_product_QTY = total_qty
        p.save()
    # for pro in product_value:
    #     pro.
    return JsonResponse(data={
        'price_without_gst': price_without_gst,
        'total_gst': total_gst,
        'net_price': net_price,
        'qty': total_qty

    })


@login_required(login_url='/login/')
def delivery_address(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    user_id = request.user.id
    address_obj = Address.objects.filter(user_id=user_id, status='1')
    country_obj = Country.objects.all()

    return render(request, 'Buy/delivery_address.html', {'cart_count': cart_count,
                                                         'address': address_obj, 'country': country_obj,
                                                         'event_year': event_year})


# for load state in address page
def load_state(request):
    country_id = request.GET.get('country')
    states = State.objects.filter(country_id=country_id).order_by('state_name')
    return render(request, 'address_dropdown/state_dropdown_list.html', {'states': states})


def state_change(request):
    country_id = request.POST.get('country_id')
    state_id = request.POST.get('state_id')
    s_id = int(state_id)
    c_id = int(country_id)
    country_obj = Country.objects.filter(id=c_id)[0]
    state_obj = State.objects.filter(id=s_id)[0]
    country_name = country_obj.country_name
    state_name = state_obj.state_name
    return JsonResponse(data={
        'country': country_name,
        'state': state_name,
    })


@login_required(login_url='/login/')
def delivery_form(request):
    try:
        full_name = request.POST.get('full_name')
        mobile = request.POST.get('mobile')
        country = request.POST.get('country')
        state = request.POST.get('State')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        landmark = request.POST.get('landmark')
        billing_full_name = request.POST.get('billing_full_name')
        billing_mobile = request.POST.get('billing_mobile')
        billing_country = request.POST.get('billing_country')
        billing_state = request.POST.get('billing_State')
        billing_pincode = request.POST.get('billing_pincode')
        billing_city = request.POST.get('billing_city')
        billing_address1 = request.POST.get('billing_address1')
        billing_address2 = request.POST.get('billing_address2')
        billing_landmark = request.POST.get('billing_landmark')
        billing_gst_no = request.POST.get('billing_gst_no')

        user_id = request.user.id
        email = request.user.email
        address_obj = Address.objects.create(user_id=user_id, fullname=full_name, mobile=mobile, email=email,
                                             country_id=country, state_id=state, pincode=pincode, city=city,
                                             address1=address1, address2=address2, landmark=landmark,
                                             billing_gst_no=billing_gst_no,
                                             billing_fullname=billing_full_name, billing_mobile=billing_mobile,
                                             billing_country=billing_country,
                                             billing_state=billing_state, billing_pincode=billing_pincode,
                                             billing_city=billing_city,
                                             billing_address1=billing_address1, billing_address2=billing_address2,
                                             billing_landmark=billing_landmark
                                             )
        address_obj.save()
        messages.success(request, 'Address Add Successfully')
        return redirect('delivery_address')

    except:
        messages.error(request, 'Something went wrong')
        return redirect('delivery_address')


def edit_address(request, address_id):
    try:
        Cart_Count(request)
        cart_count = settings.CART_COUNT
        event_year = Event_year.objects.filter(status='1')
        user_id = request.user.id
        address_obj = Address.objects.filter(user_id=user_id, id=address_id, status='1')
        country_obj = Country.objects.all()

        return render(request, 'Buy/edit_address.html',
                      {'address': address_obj, 'country': country_obj, 'cart_count': cart_count,
                       'event_year': event_year})
    except:
        return redirect('delivery_address')


@login_required(login_url='/login/')
def edit_address_form(request):
    try:
        if request.method == 'POST':
            address_id = request.POST.get('address_id')
            full_name = request.POST.get('full_name')
            mobile = request.POST.get('mobile')
            country = request.POST.get('country')
            state = request.POST.get('State')
            pincode = request.POST.get('pincode')
            city = request.POST.get('city')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            landmark = request.POST.get('landmark')
            billing_full_name = request.POST.get('billing_full_name')
            billing_mobile = request.POST.get('billing_mobile')
            billing_country = request.POST.get('billing_country')
            billing_state = request.POST.get('billing_State')
            billing_pincode = request.POST.get('billing_pincode')
            billing_city = request.POST.get('billing_city')
            billing_address1 = request.POST.get('billing_address1')
            billing_address2 = request.POST.get('billing_address2')
            billing_landmark = request.POST.get('billing_landmark')
            billing_gst_no = request.POST.get('billing_gst_no')

            user_id = request.user.id
            email = request.user.email
            Address.objects.filter(id=address_id).update(user_id=user_id, fullname=full_name, mobile=mobile,
                                                         email=email,
                                                         country_id=country, state_id=state, pincode=pincode, city=city,
                                                         address1=address1, address2=address2, landmark=landmark,
                                                         billing_gst_no=billing_gst_no,
                                                         billing_fullname=billing_full_name,
                                                         billing_mobile=billing_mobile, billing_country=billing_country,
                                                         billing_state=billing_state, billing_pincode=billing_pincode,
                                                         billing_city=billing_city,
                                                         billing_address1=billing_address1,
                                                         billing_address2=billing_address2,
                                                         billing_landmark=billing_landmark
                                                         )

            # return redirect('checkout', product_id=product_id, address_id=address_id)
            messages.success(request, 'Address Updated Successfully')
            return redirect('delivery_address')
    except:
        messages.error(request, 'Something went Wrong')
        return redirect('delivery_address')


@login_required(login_url='/login/')
def delete_address(request, address_id):
    user_id = request.user.id
    address_obj = Address.objects.filter(user_id=user_id, id=address_id, status='1')
    for address in address_obj:
        address.status = '2'
        address.save()

    return redirect('delivery_address')


@login_required(login_url='/login/')
def checkout(request, address_id):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    buy_type = request.session.get('buy_type')
    try:
        if buy_type == 'buy_now':
            product_id = int(float(request.session.get('product_id')))
            quantity = int(float(request.session.get('quantity')))
            price = int(float(request.session.get('net_price')))
            total_gst = int(float(request.session.get('total_gst')))
            net_price = int(float(request.session.get('payable_price')))
            user_id = request.user.id
            email_id = request.user.email
            fname = request.user.first_name
            buy_bag = Direct_buy_bag.objects.filter(user_id=user_id, product_id=product_id, status='1')

            if not buy_bag:
                buy_obj = Direct_buy_bag.objects.create(user_id=user_id, product_id=product_id, quantity=quantity,
                                                        gst_amount=total_gst, total_price=price, payable_price=net_price)
                buy_obj.save()

            else:
                Direct_buy_bag.objects.filter(user_id=user_id, product_id=product_id).update(quantity=quantity,
                                                        gst_amount=total_gst, total_price=price,
                                                        payable_price=net_price)

            add_obj = Address.objects.filter(user_id=user_id, id=address_id, status='1')
            order_mod = 'direct_buy'
            mnumber = None
            for add in add_obj:
                mnumber = add.mobile
            order_id = increment_order_number(request)

            order = Order.objects.filter(user_id=user_id, address_id=address_id, Payment_status='1').first()
            if order is None:
                msg = GetMessage().message(order_id, net_price, product_id, email_id, fname, mnumber, order_mod)
                order_object = Order.objects.create(user_id=user_id, address_id=address_id,
                                                    amount_initiated=net_price, cart='', order_Id=order_id)
                order_object.save()
                order = Order.objects.filter(user_id=user_id, address_id=address_id, Payment_status='1')
                return render(request, 'Buy/checkout.html',
                              {'event_year': event_year, 'cart_count': cart_count, 'order_obj': order,
                               'net_price': net_price,
                               'total_gst': total_gst, 'price_without_gst': price,
                               'total_qty': quantity, 'url': settings.BILL_URL, 'msg': msg})


            else:
                order_id = increment_order_number(request)
                msg = GetMessage().message(order_id, net_price, product_id, email_id, fname, mnumber, order_mod)
                Order.objects.filter(user_id=user_id, address_id=address_id, Payment_status='1').update(
                    address_id=address_id, amount_initiated=net_price, cart='', order_Id=order_id)
                order_obj = Order.objects.filter(user_id=user_id, address_id=address_id, Payment_status='1')
                return render(request, 'Buy/checkout.html',
                              {'event_year': event_year, 'cart_count': cart_count, 'order_obj': order_obj,
                               'net_price': net_price,
                               'total_gst': total_gst, 'price_without_gst': price,
                               'total_qty': quantity, 'url': settings.BILL_URL, 'msg': msg})

            #Add to cart buy product start from here ___________________

        else:
            cart_id = ''
            user_id = request.user.id
            email_id = request.user.email
            fname = request.user.first_name
            add_obj = Address.objects.filter(user_id=user_id, id=address_id, status='1')
            for add in add_obj:
                mnumber = add.mobile
            order_id = increment_order_number(request)
            order_mod = 'Indirect_buy'
            cart_obj = Cart.objects.filter(user_id=user_id, status='1')
            for c in cart_obj:
                cart_id = cart_id + str(c.id) + ','
            cart1 = Cart.objects.filter(user_id=user_id, status='1')
            for c in cart1:
                net_price = c.total_price_with_QTY
                total_gst = c.total_gst_with_QTY
                price_without_gst = c.total_price_without_gst_QTY
                total_qty = c.total_product_QTY

            order = Order.objects.filter(user_id=user_id, address_id=address_id, Payment_status='1').first()
            if order is None:
                msg = GetMessage().message(order_id, net_price, user_id, email_id, fname, mnumber, order_mod)
                order_object = Order.objects.create(user_id=user_id, address_id=address_id, cart=cart_id,
                                                    amount_initiated=net_price, order_Id=order_id)
                order_object.save()
                order = Order.objects.filter(user_id=user_id, address_id=address_id, Payment_status='1')
                return render(request, 'Buy/checkout.html',
                              {'event_year': event_year, 'cart_count': cart_count, 'order_obj': order,
                               'net_price': net_price,
                               'total_gst': total_gst, 'price_without_gst': price_without_gst,
                               'total_qty': total_qty, 'url': settings.BILL_URL, 'msg': msg})


            else:
                order_id = increment_order_number(request)
                msg = GetMessage().message(order_id, net_price, user_id, email_id, fname, mnumber, order_mod)
                Order.objects.filter(user_id=user_id, address_id=address_id, Payment_status='1').update(
                    address_id=address_id, cart=cart_id, amount_initiated=net_price, order_Id=order_id)
                order_obj = Order.objects.filter(user_id=user_id, address_id=address_id, Payment_status='1')
                cart_obj = Cart.objects.filter(user_id=user_id, status='1')
                return render(request, 'Buy/checkout.html',
                              {'event_year': event_year, 'cart_count': cart_count, 'order_obj': order_obj,
                               'net_price': net_price,
                               'total_gst': total_gst, 'price_without_gst': price_without_gst,
                               'total_qty': total_qty, 'url': settings.BILL_URL, 'msg': msg})
    except:
        return redirect('cart')


@csrf_exempt
def handleResponse(request):
    if request.method == 'POST':
        response = request.POST
        values = ResponseMessage().respMsg(response)
        if values['order_mode'] == 'direct_buy':

            if not values is False and values['MID'] == settings.MID:
                order_obj = Order.objects.filter(order_Id=values['OrderID'])[0]
                tstat, amnt, txnid, dnt, mode = values['TStat'], values['AMNT'], values['TaxnNo'], values['DnT'], values[
                    'TMode']
                if tstat == '0300' and order_obj.amount_initiated == float(amnt):
                    if order_obj.Payment_status != '2':
                        id = order_obj.user_id
                        cart_obj = Direct_buy_bag.objects.filter(user_id=id, product_id=values['pro_id'], status='1')
                        for cart in cart_obj:
                            cart.status = '2'
                            cart.save()
                        invoice_number = increment_invoice_number()
                        invoice_obj = Invoice.objects.create(user_id=id, order_Id_id=values['OrderID'],
                                                             invoice_no=invoice_number)
                        invoice_obj.save()
                        order_obj.Invoice_number = invoice_number
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '2'
                        order_obj.was_success = True
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        direct_buy_generate_pdf(request, id, values['OrderID'], values['pro_id'])
                    # usr_details = User.objects.filter(id=id)[0]
                    typ = 'success'
                    msgs = ['Success', 'Payment Succesful']
                    return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                   'mode': mode})
                elif tstat == '0300' and order_obj.amount_initiated != amnt:
                    # id = order_obj.user_id
                    order_obj.amount_initiated = amnt
                    order_obj.txn_id = txnid
                    order_obj.Date_of_payment = datetime.now()
                    order_obj.Payment_status = '4'
                    order_obj.was_success = False
                    order_obj.log = str([response])
                    order_obj.save()
                    # usr_details = User.objects.filter(id=id)[0]
                    msgs = ['Failed', 'Payment declined! Looked liked someone tried tampering your payment']
                    typ = 'danger'
                    return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                   'mode': mode})
                elif tstat == '0002':
                    # id = order_obj.user_id
                    order_obj.amount_initiated = amnt
                    order_obj.txn_id = txnid
                    order_obj.Date_of_payment = datetime.now()
                    order_obj.Payment_status = '3'
                    order_obj.was_success = False
                    order_obj.log = str([response])
                    order_obj.save()
                    # usr_details = User.objects.filter(id=id)[0]
                    msgs = ['Failed',
                            'Billdesk is waiting for the trasaction status from your bank. Will update you as soon as we have any response',
                            ]
                    typ = 'info'
                    return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                   'mode': mode})
                elif tstat != '0300':
                    if tstat == '0399':
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '3'
                        order_obj.was_success = False
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        detail = 'Invalid Authentication at Bank'
                        msgs = ['Failed', detail]
                        typ = 'info'
                        return render(request, 'Buy/afterPayment.html',
                                      {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                       'mode': mode})
                    elif tstat == 'NA':
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '3'
                        order_obj.was_success = False
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        detail = 'Invalid Input in the Request Message'
                        msgs = ['Failed', detail]
                        typ = 'info'
                        return render(request, 'Buy/afterPayment.html',
                                      {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                       'mode': mode})
                    elif tstat == '0001':
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '3'
                        order_obj.was_success = False
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        detail = 'error at billdesk'
                        msgs = ['Failed', detail]
                        typ = 'info'
                        return render(request, 'buy/afterPayment.html',
                                      {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                       'mode': mode})
                    else:
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '3'
                        order_obj.was_success = False
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        detail = 'Payment Failed'
                        msgs = ['Failed', detail]
                        typ = 'danger'
                        return render(request, 'Buy/afterPayment.html',
                                      {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                       'mode': mode})
                else:
                    return HttpResponse('Bad Request')
            else:
                msgs = ['Failed', 'Payment declined! Looked liked someone tried tampering your payment']
                return render(request, 'Buy/afterPayment.html', {'error': msgs, 'typ': 'danger'})

        else:
            if not values is False and values['MID'] == settings.MID:
                order_obj = Order.objects.filter(order_Id=values['OrderID'])[0]
                tstat, amnt, txnid, dnt, mode = values['TStat'], values['AMNT'], values['TaxnNo'], values['DnT'], \
                                                values[
                                                    'TMode']

                if tstat == '0300' and order_obj.amount_initiated == float(amnt):
                    if order_obj.Payment_status != '2':
                        id = order_obj.user_id
                        cart_obj = Cart.objects.filter(user_id=id, order_status='1', status='1')
                        for cart in cart_obj:
                            cart.order_status = '2'
                            cart.save()
                        invoice_number = increment_invoice_number()
                        invoice_obj = Invoice.objects.create(user_id=id, order_Id_id=values['OrderID'],
                                                             invoice_no=invoice_number)
                        invoice_obj.save()
                        order_obj.Invoice_number = invoice_number
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '2'
                        order_obj.was_success = True
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        generate_pdf(request, id, values['OrderID'])
                    # usr_details = User.objects.filter(id=id)[0]
                    typ = 'success'
                    msgs = ['Success', 'Payment Succesful']
                    return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                   'mode': mode})
                elif tstat == '0300' and order_obj.amount_initiated != amnt:
                    # id = order_obj.user_id
                    order_obj.amount_initiated = amnt
                    order_obj.txn_id = txnid
                    order_obj.Date_of_payment = datetime.now()
                    order_obj.Payment_status = '4'
                    order_obj.was_success = False
                    order_obj.log = str([response])
                    order_obj.save()
                    # usr_details = User.objects.filter(id=id)[0]
                    msgs = ['Failed', 'Payment declined! Looked liked someone tried tampering your payment']
                    typ = 'danger'
                    return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                   'mode': mode})
                elif tstat == '0002':
                    # id = order_obj.user_id
                    order_obj.amount_initiated = amnt
                    order_obj.txn_id = txnid
                    order_obj.Date_of_payment = datetime.now()
                    order_obj.Payment_status = '3'
                    order_obj.was_success = False
                    order_obj.log = str([response])
                    order_obj.save()
                    # usr_details = User.objects.filter(id=id)[0]
                    msgs = ['Failed',
                            'Billdesk is waiting for the trasaction status from your bank. Will update you as soon as we have any response',
                            ]
                    typ = 'info'
                    return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                   'mode': mode})
                elif tstat != '0300':
                    if tstat == '0399':
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '3'
                        order_obj.was_success = False
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        detail = 'Invalid Authentication at Bank'
                        msgs = ['Failed', detail]
                        typ = 'info'
                        return render(request, 'Buy/afterPayment.html',
                                      {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                       'mode': mode})
                    elif tstat == 'NA':
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '3'
                        order_obj.was_success = False
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        detail = 'Invalid Input in the Request Message'
                        msgs = ['Failed', detail]
                        typ = 'info'
                        return render(request, 'Buy/afterPayment.html',
                                      {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                       'mode': mode})
                    elif tstat == '0001':
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '3'
                        order_obj.was_success = False
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        detail = 'error at billdesk'
                        msgs = ['Failed', detail]
                        typ = 'info'
                        return render(request, 'buy/afterPayment.html',
                                      {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                       'mode': mode})
                    else:
                        order_obj.amount_initiated = amnt
                        order_obj.txn_id = txnid
                        order_obj.Date_of_payment = datetime.now()
                        order_obj.Payment_status = '3'
                        order_obj.was_success = False
                        order_obj.payment_mode = mode
                        order_obj.log = str([response])
                        order_obj.save()
                        detail = 'Payment Failed'
                        msgs = ['Failed', detail]
                        typ = 'danger'
                        return render(request, 'Buy/afterPayment.html',
                                      {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt),
                                       'mode': mode})
                else:
                    return HttpResponse('Bad Request')
            else:
                msgs = ['Failed', 'Payment declined! Looked liked someone tried tampering your payment']
                return render(request, 'Buy/afterPayment.html', {'error': msgs, 'typ': 'danger'})

    else:
        return HttpResponse('Bad Request')


def generate_pdf(request, user_id, order_ID):
    total_price = 0
    total_gst = 0
    total_price_word = 0
    total_price_without_gst = 0
    total_gst_word = ''
    total_QTY = 0
    user_obj = User.objects.filter(id=user_id)[0]
    user_mail = user_obj.email
    first_name = user_obj.first_name
    last_name = user_obj.last_name
    order_obj = Order.objects.filter(order_Id=order_ID)[0]
    cart_obj = Cart.objects.filter(user_id=user_id, order_status='2')
    cart_count = Cart.objects.filter(user_id=user_id, order_status='2').count()
    if cart_count > 0:

        for cart in cart_obj:
            total_price = cart.total_price_with_QTY
            total_price_without_gst = cart.total_price_without_gst_QTY
            total_gst = cart.total_gst_with_QTY
            total_QTY = cart.total_product_QTY
            total_price_word = num2words(total_price, lang='en_IN')
            total_gst_word = num2words(total_gst)
        for c in cart_obj:
            gst = int(c.gst_with_product_QTY)
            price = int(c.payable_price_withoutGST)
            total = gst + price
            ord_product = Order_Product.objects.create(user_id=user_id, order_Id_id=order_ID,
                                                       Product_name=c.product.product_name, Product_amount=total,
                                                       Total_price_without_gst=total_price_without_gst,
                                                       Total_gst_amount=total_gst, Product_qty=c.quantity,
                                                       product_image=c.product.product_image)
            ord_product.save()

        template = get_template('Buy/invoice.html')
        data = {
            'order_id': order_obj.order_Id, 'invoice_number': order_obj.Invoice_number,
            'payment_date': order_obj.Date_of_payment, 'address1': order_obj.address.address1,
            'address2': order_obj.address.address2,
            'landmark': order_obj.address.landmark, 'city': order_obj.address.city,
            'pincode': order_obj.address.pincode,
            'state': order_obj.address.state, 'country': order_obj.address.country,
            'fullname': order_obj.address.fullname,
            'mobile': order_obj.address.mobile, 'email': order_obj.address.email, 'lastname': last_name,
            'firstname': first_name,
            'billing_address1': order_obj.address.billing_address1,
            'billing_address2': order_obj.address.billing_address2,
            'billing_landmark': order_obj.address.billing_landmark, 'billing_city': order_obj.address.billing_city,
            'billing_pincode': order_obj.address.billing_pincode,
            'billing_state': order_obj.address.billing_state, 'billing_country': order_obj.address.billing_country,
            'billing_fullname': order_obj.address.billing_fullname,
            'billing_mobile': order_obj.address.billing_mobile, 'billing_gst_no': order_obj.address.billing_gst_no,
            'order': order_obj, 'net_price': total_price, 'price_in_word': total_price_word,
            'price_without_gst': total_price_without_gst,
            'cart_obj': cart_obj, 'total_gst': total_gst, 'total_gst_word': total_gst_word, 'total_QTY': total_QTY,
            'name': user_obj.first_name,

        }
        html = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("Utf-8")), result)  # , link_callback=fetch_resources)
        pdf = result.getvalue()
        filename = 'Invoice_' + str(data['order_id']) + '.pdf'
        html_message = render_to_string('Buy/email-message.html', data)
        mail_subject = 'Order Invoice - AMTZ'
        template = get_template('Buy/invoice.html')
        message = html_message
        to_email = [user_mail, 'sales@amtz.in', 'finance@amtz.in']
        email = EmailMultiAlternatives(
            mail_subject,
            "hello",  # necessary to pass some message here
            settings.EMAIL_HOST_USER, to_email)
        email.attach_alternative(message, "text/html")
        email.attach(filename, pdf, 'application/pdf')
        email.send(fail_silently=False)
        receipt_file = BytesIO(pdf)
        invoice_obj = Invoice.objects.filter(order_Id_id=order_ID).first()
        invoice_obj.invoice_document = File(receipt_file, filename)
        invoice_obj.save()
        for cart in cart_obj:
            cart.order_status = '3'
            cart.status = '3'
            cart.save()


# Direct Buy Pdf generation ________
def direct_buy_generate_pdf(request, user_id, order_ID, pro_id):

    total_price = 0
    total_gst = 0
    total_price_word = 0
    total_price_without_gst = 0
    total_gst_word = ''
    total_QTY = 0
    user_obj = User.objects.filter(id=user_id)[0]
    user_mail = user_obj.email
    first_name = user_obj.first_name
    last_name = user_obj.last_name
    order_obj = Order.objects.filter(order_Id=order_ID)[0]
    cart_obj = Direct_buy_bag.objects.filter(user_id=user_id, product_id=pro_id, status='2')
    cart_count = Direct_buy_bag.objects.filter(user_id=user_id, product_id=pro_id, status='2').count()
    if cart_count > 0:

        for cart in cart_obj:
            total_price = cart.payable_price
            total_price_without_gst = cart.total_price
            total_gst = cart.gst_amount
            total_QTY = cart.quantity
            total_price_word = num2words(total_price, lang='en_IN')
            total_gst_word = num2words(total_gst)
        for c in cart_obj:
            gst = int(c.gst_amount)
            price = int(c.total_price)
            total = gst + price
            ord_product = Order_Product.objects.create(user_id=user_id, order_Id_id=order_ID,
                                                       Product_name=c.product.product_name, Product_amount=total,
                                                       Total_price_without_gst=total_price_without_gst,
                                                       Total_gst_amount=total_gst, Product_qty=c.quantity,
                                                       product_image=c.product.product_image)
            ord_product.save()

        template = get_template('Buy/invoice.html')
        data = {
            'order_id': order_obj.order_Id, 'invoice_number': order_obj.Invoice_number,
            'payment_date': order_obj.Date_of_payment, 'address1': order_obj.address.address1,
            'address2': order_obj.address.address2,
            'landmark': order_obj.address.landmark, 'city': order_obj.address.city,
            'pincode': order_obj.address.pincode,
            'state': order_obj.address.state, 'country': order_obj.address.country,
            'fullname': order_obj.address.fullname,
            'mobile': order_obj.address.mobile, 'email': order_obj.address.email, 'lastname': last_name,
            'firstname': first_name,
            'billing_address1': order_obj.address.billing_address1,
            'billing_address2': order_obj.address.billing_address2,
            'billing_landmark': order_obj.address.billing_landmark, 'billing_city': order_obj.address.billing_city,
            'billing_pincode': order_obj.address.billing_pincode,
            'billing_state': order_obj.address.billing_state, 'billing_country': order_obj.address.billing_country,
            'billing_fullname': order_obj.address.billing_fullname,
            'billing_mobile': order_obj.address.billing_mobile, 'billing_gst_no': order_obj.address.billing_gst_no,
            'order': order_obj, 'net_price': total_price, 'price_in_word': total_price_word,
            'price_without_gst': total_price_without_gst,
            'cart_obj': cart_obj, 'total_gst': total_gst, 'total_gst_word': total_gst_word, 'total_QTY': total_QTY,
            'name': user_obj.first_name, 'invoice_type': 'direct_buy'

        }
        html = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("Utf-8")), result)  # , link_callback=fetch_resources)
        pdf = result.getvalue()
        filename = 'Invoice_' + str(data['order_id']) + '.pdf'
        html_message = render_to_string('Buy/email-message.html', data)
        mail_subject = 'Order Invoice - AMTZ'
        template = get_template('Buy/invoice.html')
        message = html_message
        to_email = [user_mail, 'sales@amtz.in', 'finance@amtz.in']
        email = EmailMultiAlternatives(
            mail_subject,
            "hello",  # necessary to pass some message here
            settings.EMAIL_HOST_USER, to_email)
        email.attach_alternative(message, "text/html")
        email.attach(filename, pdf, 'application/pdf')
        email.send(fail_silently=False)
        receipt_file = BytesIO(pdf)
        invoice_obj = Invoice.objects.filter(order_Id_id=order_ID).first()
        invoice_obj.invoice_document = File(receipt_file, filename)
        invoice_obj.save()
        for cart in cart_obj:
            cart.status = '3'
            cart.save()
def increment_order_number(request):
    id = request.user.id
    new_order_no = (datetime.now().strftime('%Y%m%d%H%M%S%f')) + str(id)
    return new_order_no


def increment_invoice_number():
    last_invoice = Invoice.objects.all().order_by('id').last()
    if not last_invoice:
        return 1
    invoice_no = last_invoice.invoice_no
    # invoice_int = int(invoice_no.split('AMTZ')[-1])
    new_invoice_int = int(invoice_no) + 1
    new_invoice_no = new_invoice_int
    return new_invoice_no


@login_required(login_url='/login/')
def my_order(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    user_id = request.user.id
    order_obj = Order.objects.filter(user_id=user_id, Payment_status='2').order_by('Date_of_payment').reverse()
    return render(request, 'myorder/order.html',
                  {'order_obj': order_obj, 'cart_count': cart_count, 'event_year': event_year})


@login_required(login_url='/login/')
def order_details(request, order_id):
    try:
        event_year = Event_year.objects.filter(status='1')
        Cart_Count(request)
        cart_count = settings.CART_COUNT
        order = Order_Product.objects.filter(order_Id=order_id)
        invoice = Invoice.objects.filter(order_Id_id=order_id).first()
        for ord in order:
            transaction_id = ord.order_Id.txn_id
            price = ord.Total_price_without_gst
            gst = ord.Total_gst_amount
            total_price = ord.order_Id.amount_initiated
        return render(request, 'myorder/order_details.html', {'order': order, 'txn_id': transaction_id, 'price': price,
                                                              'gst': gst, 'total_price': total_price,
                                                              'order_id': order_id,
                                                              'invoice': invoice.invoice_document,
                                                              'cart_count': cart_count, 'event_year': event_year})
    except:
        return redirect('order')


@login_required(login_url='/login/')
def logout_request(request):
    logout(request)
    return render(request, 'home.html')


# forgot Password ===================================================================
def forgot_password(request):
    try:
        Cart_Count(request)
        cart_count = settings.CART_COUNT
        event_year = Event_year.objects.filter(status='1')
        if request.method == "POST":
            email = request.POST.get('email')
            user_obj = User.objects.filter(email=email)
            count = user_obj.count()
            if count > 0:
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                u = User.objects.get(email=email)
                u.set_password(password)
                first_name = u.first_name
                last_name = u.last_name
                u.save()
                set_url = request._current_scheme_host
                merge_data = {
                    'password': password,
                    'first_name': first_name,
                    'last_name': last_name,
                    'set_url': set_url,

                }
                send_forgot_emails(request, merge_data, email)
                return render(request, 'auth/forgot_password.html',
                              {'message': 'System Generated password is send on your registered E-mail',
                               'cart_count': cart_count, 'event_year': event_year})
            else:
                return render(request, 'auth/forgot_password.html',
                              {'error': 'Invalid E-mail,Try again', 'cart_count': cart_count, 'event_year': event_year})

        return render(request, 'auth/forgot_password.html', {'cart_count': cart_count, 'event_year': event_year})
    except:
        return redirect('login')

def send_forgot_emails(request, merge_data, email):

    html_body = render_to_string("auth/forgot_email.html", merge_data)

    message = EmailMultiAlternatives(
       subject='Confirmation to Reset your password',
       body="",
       from_email=settings.EMAIL_HOST_USER,
       to=[email]
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)

@login_required(login_url='/login/')
def change_password(request):
    try:
        Cart_Count(request)
        cart_count = settings.CART_COUNT
        event_year = Event_year.objects.filter(status='1')
        if request.user.is_authenticated:
            if request.method == 'POST':
                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                # validation
                error_message = None
                if not new_password == confirm_password:
                    return render(request, 'auth/change_password.html',
                                  {'error': "Password doesn't match enter correct Password", 'cart_count': cart_count,
                                   'event_year': event_year})
                else:
                    user = User.objects.get(email=request.user.email)
                    if user.check_password(old_password):
                        user = request.user
                        user.set_password(confirm_password)
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, "Password Updated Successfully")
                        # return redirect('login')
                        return render(request, 'auth/change_password.html',
                                          {'cart_count': cart_count, 'event_year': event_year})

                    else:
                        return render(request, 'auth/change_password.html',
                                      {'error': "Old Password does't match", 'cart_count': cart_count,
                                       'event_year': event_year})
            else:
                return render(request, 'auth/change_password.html',
                              {'cart_count': cart_count, 'event_year': event_year})
    except:
        return redirect('login')

    else:
        return render(request, 'auth/login.html', {'cart_count': cart_count, 'event_year': event_year})


@login_required(login_url='/login/')
def profile(request):
    try:
        Cart_Count(request)
        cart_count = settings.CART_COUNT
        event_year = Event_year.objects.filter(status='1')
        id = request.user.id
        profile_obj = User.objects.filter(id=id)
        user_obj = user_role.objects.filter(user_id=id)[0]
        return render(request, 'auth/profile.html', {'profiles': profile_obj, 'mobile': user_obj.mobile,
                                                     'alternative_mobile': user_obj.alternative_mobile,
                                                     'cart_count': cart_count, 'event_year': event_year})
    except:
        return render(request, 'auth/login.html')


def update_profile(request):
    try:
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        other_number = request.POST.get('other_number')

        User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name, email=email)

        user_obj = user_role.objects.filter(user_id=user_id).first()
        user_obj.mobile = phone_number
        user_obj.alternative_mobile = other_number
        user_obj.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect('profile')
    except:
        return redirect('login')


@login_required(login_url='/login/')
def user_dashboard(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    order_id = None
    payment_date = None
    villa_amount = None
    room_oder_id = None
    room_no = None
    adult_no = None
    check_in = None
    check_out = None
    room_invoice = None
    Payment_status = None
    amount = None
    user_id = request.user.id
    order_obj = Order.objects.filter(user_id=user_id, Payment_status='2').count()
    book_obj = Booking_room.objects.filter(user_id=user_id, Payment_status='2').count()
    product_in_cart = Cart.objects.filter(user_id=user_id, status='1').count()
    order = Order.objects.filter(user_id=user_id, Payment_status='2').order_by('Date_of_payment').reverse().first()
    if order:
        order_id = order.order_Id
        payment_date = order.Date_of_payment
        amount = order.amount_initiated
    book = Booking_room.objects.filter(user_id=user_id).order_by('Date_of_payment').reverse().first()
    if book:
        room_oder_id = book.order_number
        room_no = book.room_no
        adult_no = book.order_number.adult_no
        check_in = book.order_number.check_in
        check_out = book.order_number.check_out
        villa_amount = book.order_number.price
        Payment_status = book.Payment_status
        try:
            room_invoice = book.invoice_document.url
        except:
            room_invoice = None

    return render(request, 'myorder/userdashboard.html', {'order_product': order_obj, 'room_booked': book_obj,
                                                          'product': product_in_cart, 'order_id': order_id,
                                                          'payment_date': payment_date,
                                                          'amount': amount, 'room_oder_id': room_oder_id,
                                                          'room_no': room_no, 'villa_amount': villa_amount,
                                                          'adult_no': adult_no, 'check_in': check_in,
                                                          'check_out': check_out,
                                                          'Payment_status': Payment_status,
                                                          'room_invoice': room_invoice, 'cart_count': cart_count,
                                                          'event_year': event_year
                                                          })

def reset_password(request):
        try:
            Cart_Count(request)
            cart_count = settings.CART_COUNT
            event_year = Event_year.objects.filter(status='1')
            if request.method == 'POST':
                    old_password = request.POST.get('old_password')
                    new_password = request.POST.get('new_password')
                    confirm_password = request.POST.get('confirm_password')
                    email = request.POST.get('email')

                    # validation
                    error_message = None
                    if not new_password == confirm_password:
                        return render(request, 'auth/reset_password.html',
                                      {'error': "Password doesn't match enter correct Password",
                                       'cart_count': cart_count,
                                       'event_year': event_year})
                    else:
                        try:
                            user = User.objects.get(email=email)
                            if user.check_password(old_password):
                                user.set_password(confirm_password)
                                user.save()
                                messages.success(request, "Password Updated Successfully")
                                return render(request, 'auth/login.html',
                                                  {'cart_count': cart_count, 'event_year': event_year})

                            else:
                                return render(request, 'auth/reset_password.html',
                                              {'error': "System Generated Password doesn't match", 'cart_count': cart_count,
                                               'event_year': event_year})
                        except:
                            return render(request, 'auth/reset_password.html',
                                          {'error': "email doesn't Exit Please try with Correct email", 'cart_count': cart_count,
                                           'event_year': event_year})
            else:
                return render(request, 'auth/reset_password.html',
                                  {'cart_count': cart_count, 'event_year': event_year})
        except:
            return redirect('login')


# def refund_form(request):
#     Cart_Count(request)
#     cart_count = settings.CART_COUNT
#     event_year = Event_year.objects.filter(status='1')
#     return render(request, 'refund/refund_form.html', {'cart_count': cart_count, 'event_year': event_year})

def buy_now(request):
    product_id = request.POST.get('id')
    net_price = request.POST.get('net_price')
    total_gst = request.POST.get('gst')
    payable_price = request.POST.get('payable_price')
    quantity = 1
    request.session['product_id'] = product_id
    request.session['quantity'] = quantity
    request.session['net_price'] = net_price
    request.session['total_gst'] = total_gst
    request.session['payable_price'] = payable_price
    request.session['buy_type'] = 'buy_now'
    return JsonResponse(data={
        'net_price': net_price,
        'total_gst': total_gst,
        'payable_price': payable_price,

    })


def quantity_change_buy(request):
    quantity = request.POST.get('quantity')
    product_id = request.POST.get('id')
    pro_obj = Product.objects.get(id=product_id)
    net_price = pro_obj.product_price * int(quantity)
    total_gst = int(pro_obj.gst) * int(net_price)/100
    payable_price = int(net_price) + int(total_gst)

    request.session['product_id'] = product_id
    request.session['quantity'] = quantity
    request.session['net_price'] = net_price
    request.session['total_gst'] = total_gst
    request.session['payable_price'] = payable_price
    request.session['buy_type'] = 'buy_now'

    return JsonResponse(data={
        'net_price': net_price,
        'total_gst': total_gst,
        'payable_price': payable_price,

    })
