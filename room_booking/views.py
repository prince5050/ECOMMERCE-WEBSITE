from room_booking.models import *
from ecommerce import views
from django.conf import settings
import datetime
from django.core.files import File
from num2words import num2words
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django_billdesk import ResponseMessage, GetMessage
# Create your views here.
from store.models.events import Event_year
from store.views.home import Cart_Count


def room_list(request):
    return render(request, 'Room/room_list.html')

def room_search(request):
    info_message = []
    admin_book_message = []
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    if request.method == "POST":
        try:
            start_date = request.POST.get('check_in')
            end_date = request.POST.get('check_out')
            mobile = request.POST.get('mobile')
            adult_no = request.POST.get('adult_no')
            request.session['start_date'] = start_date
            request.session['mobile'] = mobile
            request.session['adult_no'] = adult_no
            request.session['end_date'] = end_date
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date < datetime.date.today() or end_date < datetime.date.today():
                return render(request, 'Room/room_search.html', {'error': 'Please Enter Correct Booking Date', 'cart_count': cart_count, 'event_year': event_year})
            if end_date < start_date:
                return render(request, 'Room/room_search.html', {'error': 'Please Enter Correct Booking Date', 'cart_count': cart_count, 'event_year': event_year})
            if start_date == end_date:
                return render(request, 'Room/room_search.html', {'error': 'Same Day Check-in and Check-out not allowed', 'cart_count': cart_count, 'event_year': event_year})
            no_of_days = (end_date - start_date).days

        # Automatic Available Room when checkout less than Booking start date_______________________
            room = Rooms.objects.all()
            for rom in room:
                try:
                    filter_params = dict(check_in__lte=end_date, check_out__gte=start_date)
                    room_book_obj = Booking_room.objects.filter(**filter_params, Payment_status='2', room_no=rom.room_no).exists()
                    room_book = Booking_room.objects.filter(**filter_params, Payment_status='2', room_no=rom.room_no)

                    if room_book_obj == True:
                        if room_book is not None:
                            for room in room_book:
                                # if room.check_out <= start_date and room.check_in < start_date:
                                #     print('b1')
                                #     room_obj = Rooms.objects.filter(room_no=room.room_no)
                                #     for r in room_obj:
                                #             r.is_available = True
                                #             r.save()

                                if room.check_in > start_date and room.check_in > end_date:
                                    room_obj = Rooms.objects.filter(room_no=room.room_no)
                                    for r in room_obj:
                                            r.is_available = True
                                            r.save()

                                if room.check_in < start_date and room.check_out >= end_date:

                                    room_obj = Rooms.objects.filter(room_no=room.room_no)
                                    info_message = Booking_room.objects.filter(**filter_params, Payment_status='2',
                                                                               room_no=rom.room_no)
                                    for r in room_obj:
                                            r.is_available = False
                                            r.save()

                                #  Add extra conditions

                                if room.check_in > start_date and room.check_out <= end_date:

                                    room_obj = Rooms.objects.filter(room_no=room.room_no)
                                    info_message = Booking_room.objects.filter(**filter_params, Payment_status='2',
                                                                               room_no=rom.room_no)
                                    for r in room_obj:
                                            r.is_available = False
                                            r.save()
                                if room.check_in > start_date and room.check_out > end_date and room.check_in < end_date:

                                    room_obj = Rooms.objects.filter(room_no=room.room_no)
                                    info_message = Booking_room.objects.filter(**filter_params, Payment_status='2',
                                                                               room_no=rom.room_no)
                                    for r in room_obj:
                                        r.is_available = False
                                        r.save()
                                if room.check_in < start_date and room.check_out > start_date and room.check_out < end_date:

                                    room_obj = Rooms.objects.filter(room_no=room.room_no)
                                    info_message = Booking_room.objects.filter(**filter_params, Payment_status='2',
                                                                               room_no=rom.room_no)
                                    for r in room_obj:
                                        r.is_available = False
                                        r.save()
                                if room.check_in == start_date:

                                    room_obj = Rooms.objects.filter(room_no=room.room_no)
                                    info_message = Booking_room.objects.filter(**filter_params, Payment_status='2',
                                                                               room_no=rom.room_no)
                                    for r in room_obj:
                                        r.is_available = False
                                        r.save()

                                if room.check_in == end_date:

                                    room_obj = Rooms.objects.filter(room_no=room.room_no)
                                    info_message = Booking_room.objects.filter(**filter_params, Payment_status='2',
                                                                               room_no=rom.room_no)
                                    for r in room_obj:
                                        r.is_available = True
                                        r.save()

                            # room_obj = Rooms.objects.filter(room_no=room.room_no)
                            # for r in room_obj:
                            #         r.is_available = False
                            #         r.save()
                    else:
                        #Rooms.objects.filter(room_no=rom.room_no).update(is_avaliable=True)
                            room_obj = Rooms.objects.all()
                            for r in room_obj:
                                r.is_available = True
                                r.save()



                except:

                    room_book_obj = None
        # If Admin checkout Greater than Booking start date_______________________
            room = Rooms.objects.all()
            for rom in room:
                filter_params = dict(check_in__lte=end_date, check_out__gte=start_date)
                admin_room_book_obj = Book_By_admin.objects.filter(**filter_params, status='1',
                                                            room_no=rom.room_no).exists()
                admin_book_obj = Book_By_admin.objects.filter(**filter_params, status='1', room_no=rom.room_no)


                #admin_book_obj = Book_By_admin.objects.filter(room_no_id=rom.room_no, status='1', check_in__gte=datetime.date.today())
                if admin_room_book_obj == True:
                        for admin_book in admin_book_obj:
                            if admin_book.check_out <= start_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=False)


                            if admin_book.check_in < start_date and admin_book.check_out == end_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=True)
                                admin_book_message = Book_By_admin.objects.filter(**filter_params, room_no_id=rom.room_no, status='1', check_in__gte=datetime.date.today())
                                # check_in__gte = datetime.date.today()



                            if admin_book.check_in < start_date and admin_book.check_out <= end_date and admin_book.check_out > start_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=True)
                                admin_book_message = Book_By_admin.objects.filter(**filter_params, room_no_id=rom.room_no, status='1', check_in__gte=datetime.date.today())
                                # check_in__gte = datetime.date.today()


                            if admin_book.check_in > start_date and admin_book.check_out > end_date and admin_book.check_in < end_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=True)
                                admin_book_message = Book_By_admin.objects.filter(**filter_params, room_no_id=rom.room_no, status='1', check_in__gte=datetime.date.today())
                                # check_in__gte = datetime.date.today()


                            if admin_book.check_in > start_date and admin_book.check_in > end_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=False)


                                #Extra Field
                            if admin_book.check_in > start_date and admin_book.check_out == end_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=True)
                                admin_book_message = Book_By_admin.objects.filter(**filter_params, room_no_id=rom.room_no, status='1', check_in__gte=datetime.date.today())
                                # check_in__gte = datetime.date.today()

                            if admin_book.check_in > start_date and admin_book.check_in == end_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=False)

                            if admin_book.check_in > start_date and admin_book.check_out < end_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=True)
                                admin_book_message = Book_By_admin.objects.filter(**filter_params, room_no_id=rom.room_no, status='1', check_in__gte=datetime.date.today())


                                # end

                            if admin_book.check_in < start_date and admin_book.check_out > end_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=True)
                                admin_book_message = Book_By_admin.objects.filter(**filter_params, room_no_id=rom.room_no, status='1', check_in__gte=datetime.date.today())

                            if admin_book.check_in == start_date:
                                Rooms.objects.filter(room_no=admin_book.room_no).update(Booked_by_admin=True)
                                admin_book_message = Book_By_admin.objects.filter(**filter_params, room_no_id=rom.room_no, status='1', check_in__gte=datetime.date.today())
                               
                else:
                    #Rooms.objects.filter(room_no=rom.room_no).update(Booked_by_admin=False)
                    for r in room:
                        r.Booked_by_admin = False
                        r.save()

        # Search the empty Room --------------------------------------
            room_obj = Rooms.objects.filter(is_available=True, Booked_by_admin=False).order_by('room_no')


            request.session['no_of_days'] = no_of_days
            return render(request, 'Room/room_list.html', {'room_obj': room_obj, 'cart_count': cart_count, 'event_year': event_year, 'message': info_message, 'admin_msg': admin_book_message})
        except:
            return render(request, 'Room/room_search.html', {'cart_count': cart_count, 'event_year': event_year})
    else:
        return render(request, 'Room/room_search.html', {'cart_count': cart_count, 'event_year': event_year})
@login_required(login_url='/login/')
def book_now(request, id):
    try:
        event_year = Event_year.objects.filter(status='1')
        cart_count = settings.CART_COUNT
        if request.session.get("no_of_days", 1):
            user_id = request.user.id
            no_of_days = request.session['no_of_days']
            start_date = request.session['start_date']
            end_date = request.session['end_date']
            name = request.user.first_name + '' + request.user.last_name
            email = request.user.email
            mobile = request.session['mobile']
            adult_no = request.session['adult_no']
            request.session['room_no'] = id
            data = Rooms.objects.get(room_no=id)
            bill = data.price*int(no_of_days)
            request.session['bill'] = bill
            order_id = increment_order_number(request)
            room_obj = Room_Picture.objects.filter(room_no_id=id)
            order_obj = Room_Order.objects.create(user_id=user_id, room_no_id=id, order_number=order_id, check_in=start_date,
                                                 check_out=end_date, price=bill, name=name, email=email, mobile=mobile,
                                                 adult_no=adult_no)
            order_obj.save()
            roomManager=data.manager.name
            msg = GetMessage().message1(order_id, bill, user_id, email, name, mobile)
            return render(request, "Room/room_details.html", {"no_of_days": no_of_days, "room_no": id,
                                                              "data": data, "bill": bill, "roomManager": roomManager,
                                                              "start": start_date, "end": end_date, "msg": msg, 'room_obj': room_obj,
                                                              'cart_count': cart_count, 'event_year': event_year, 'url': settings.BILL_URL})

        else:
            return redirect("room_search")
    except:
            return redirect("room_search")

def increment_order_number(request):
    id = request.user.id
    new_order_no = str(id)+(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
    return new_order_no

@csrf_exempt
def room_handleResp(request):
    if request.method == 'POST':
        response = request.POST
        values = ResponseMessage().respMsg(response)
        if not values is False and values['MID'] == settings.MID:
            order_obj = Room_Order.objects.filter(order_number=values['OrderID'])[0]
            tstat, amnt, txnid, dnt, mode = values['TStat'], values['AMNT'], values['TaxnNo'], values['DnT'], values[
                'TMode']
            if tstat == '0300' and order_obj.price == float(amnt):
                if order_obj.status != '2':
                    id = order_obj.user_id
                    invoice_number = increment_invoice_number()
                    invoice_obj = Booking_room.objects.create(user_id=id, order_number_id=values['OrderID'], Invoice_number=invoice_number,
                                                              txn_id=txnid, Date_of_payment=datetime.datetime.now(), Payment_status='2',
                                                              was_success=True, payment_mode=mode, amount_initiated=amnt,  log=str([response]),
                                                              check_in=order_obj.check_in, check_out=order_obj.check_out, room_no=order_obj.room_no)
                    invoice_obj.save()
                    order_obj.status = '2'
                    order_obj.save()
                    inc_invoice_obj = Room_invoice.objects.create(invoice_no=invoice_number)
                    inc_invoice_obj.save()
                    room_obj = Rooms.objects.filter(room_no=order_obj.room_no).first()
                    room_obj.is_available = False
                    room_obj.save()
                    generate_pdf(request, id, values['OrderID'])
                    # usr_details = User.objects.filter(id=id)[0]
                typ = 'success'
                msgs = ['Success', 'Payment Succesful']
                data = {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt), 'mode': mode}
                return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt), 'mode': mode})
            elif tstat == '0300' and order_obj.amount_initiated != amnt:
                id = order_obj.user_id
                invoice_obj = Booking_room.objects.create(user_id=id, order_number_id=values['OrderID'],
                                                          txn_id=txnid, Date_of_payment=datetime.datetime.now(),
                                                          Payment_status='3',
                                                          was_success=False, payment_mode=mode, amount_initiated=amnt,
                                                          log=str([response]), room_no=order_obj.room_no)
                invoice_obj.save()
                order_obj.status = '3'
                order_obj.save()
                # usr_details = User.objects.filter(id=id)[0]
                msgs = ['Failed', 'Payment declined! Looked liked someone tried tampering your payment']
                typ = 'danger'
                return render(request, 'Buy/afterPayment.html',
                              {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt), 'mode': mode})
            elif tstat == '0002':
                id = order_obj.user_id
                invoice_obj = Booking_room.objects.create(user_id=id, order_number_id=values['OrderID'],
                                                          txn_id=txnid, Date_of_payment=datetime.datetime.now(),
                                                          Payment_status='3',
                                                          was_success=False, payment_mode=mode, amount_initiated=amnt,
                                                          log=str([response]), room_no=order_obj.room_no)
                invoice_obj.save()
                order_obj.status = '3'
                order_obj.save()
                # usr_details = User.objects.filter(id=id)[0]
                msgs = ['Failed',
                        'Billdesk is waiting for the trasaction status from your bank. Will update you as soon as we have any response',
                        ]
                typ = 'info'
                return render(request, 'Buy/afterPayment.html',
                              {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt), 'mode': mode})
            elif tstat != '0300':
                if tstat == '0399':
                    id = order_obj.user_id
                    invoice_obj = Booking_room.objects.create(user_id=id, order_number_id=values['OrderID'],
                                                              txn_id=txnid, Date_of_payment=datetime.datetime.now(),
                                                              Payment_status='3',
                                                              was_success=False, payment_mode=mode,
                                                              amount_initiated=amnt, room_no=order_obj.room_no,
                                                              log=str([response]))
                    invoice_obj.save()
                    order_obj.status = '3'
                    order_obj.save()
                    detail = 'Invalid Authentication at Bank'
                    msgs = ['Failed', detail]
                    typ = 'info'
                    return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt), 'mode': mode})
                elif tstat == 'NA':
                    id = order_obj.user_id
                    invoice_obj = Booking_room.objects.create(user_id=id, order_number_id=values['OrderID'],
                                                              txn_id=txnid, Date_of_payment=datetime.datetime.now(),
                                                              Payment_status='3',
                                                              was_success=False, payment_mode=mode,
                                                              amount_initiated=amnt, room_no=order_obj.room_no,
                                                              log=str([response]))
                    invoice_obj.save()
                    order_obj.status = '3'
                    order_obj.save()
                    detail = 'Invalid Input in the Request Message'
                    msgs = ['Failed', detail]
                    typ = 'info'
                    return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt), 'mode': mode})
                elif tstat == '0001':
                    id = order_obj.user_id
                    invoice_obj = Booking_room.objects.create(user_id=id, order_number_id=values['OrderID'],
                                                              txn_id=txnid, Date_of_payment=datetime.datetime.now(),
                                                              Payment_status='3',
                                                              was_success=False, payment_mode=mode,
                                                              amount_initiated=amnt, room_no=order_obj.room_no,
                                                              log=str([response]))
                    invoice_obj.save()
                    order_obj.status = '3'
                    order_obj.save()
                    detail = 'error at billdesk'
                    msgs = ['Failed', detail]
                    typ = 'info'
                    return render(request, 'Buy/afterPayment.html',
                                  {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt), 'mode': mode})
                else:
                    id = order_obj.user_id
                    invoice_obj = Booking_room.objects.create(user_id=id, order_number_id=values['OrderID'],
                                                              txn_id=txnid, Date_of_payment=datetime.datetime.now(),
                                                              Payment_status='3',
                                                              was_success=False, payment_mode=mode,
                                                              amount_initiated=amnt, room_no=order_obj.room_no,
                                                              log=str([response]))
                    invoice_obj.save()
                    order_obj.status = '3'
                    order_obj.save()
                    detail = 'Payment Failed'
                    msgs = ['Failed', detail]
                    typ = 'danger'
                    return render(request, 'Buy/afterPayment.html',
                                    {'error': msgs, 'typ': typ, 'txnid': txnid, 'date': dnt, 'amnt': float(amnt), 'mode': mode})
            else:
                return HttpResponse('Bad Request')
        else:
            msgs = ['Failed', 'Payment declined! Looked liked someone tried tampering your payment']
            return render(request, 'Buy/afterPayment.html', {'error': msgs, 'typ': 'danger'})
    else:
        return HttpResponse('Bad Request')





def generate_pdf(request, user_id, order_ID):
    user_obj = User.objects.filter(id=user_id)[0]
    user_mail = user_obj.email
    order = Room_Order.objects.filter(order_number=order_ID, status='2')
    order_obj = Room_Order.objects.filter(order_number=order_ID, status='2')[0]
    booking_obj = Booking_room.objects.filter(order_number=order_ID)[0]
    ord_count = Room_Order.objects.filter(order_number=order_ID, status='2').count()
    if ord_count > 0:
        total_price = order_obj.price
        total_price_word = num2words(total_price)
        template = get_template('Room/room_invoice.html')
        data = {
            'order_id': order_obj.order_number, 'invoice_number': booking_obj.Invoice_number,
            'payment_date': booking_obj.Date_of_payment, 'fullname': order_obj.name,
            'mobile': order_obj.mobile, 'email': order_obj.email, 'check_in': order_obj.check_in, 'check_out': order_obj.check_out,
            'order': order, 'net_price': total_price, 'price_in_word': total_price_word, 'adult_no': order_obj.adult_no,
            'one_night_price': order_obj.room_no.price,

        }
        html = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("Utf-8")), result)
        pdf = result.getvalue()
        filename = 'Booking_Invoice_' + str(data['order_id']) + '.pdf'
        html_message = render_to_string('Room/villla_email_message.html', data)
        mail_subject = 'Villa Booking Invoice - AMTZ'
        template = get_template('Room/room_invoice.html')
        message = html_message
        to_email = [user_mail, 'subbarao.m@amtz.in', 'finance@amtz.in']
        email = EmailMultiAlternatives(
        mail_subject,
        "hello",  # necessary to pass some message here
        settings.EMAIL_HOST_USER, to_email)
        email.attach_alternative(message, "text/html")
        email.attach(filename, pdf, 'application/pdf')
        email.send(fail_silently=False)
        receipt_file = BytesIO(pdf)
        invoice_obj = Booking_room.objects.filter(order_number_id=order_ID).first()
        invoice_obj.invoice_document = File(receipt_file, filename)
        invoice_obj.save()


def increment_invoice_number():
    last_invoice = Room_invoice.objects.all().order_by('id').last()
    if not last_invoice:
         return 'AMTZ/VILLA/1'
    invoice_no = last_invoice.invoice_no
    invoice_int = int(invoice_no.split('AMTZ/VILLA/')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'AMTZ/VILLA/' + str(new_invoice_int)
    return new_invoice_no
@login_required(login_url='/login/')
def Dashboard(request):
    try:
        event_year = Event_year.objects.filter(status='1')
        cart_count = settings.CART_COUNT
        user_id = request.user.id
        book_obj = Booking_room.objects.filter(user_id=user_id).order_by('Date_of_payment').reverse()
        return render(request, 'Room/booking_dashboard.html', {'book_obj': book_obj, 'cart_count': cart_count, 'event_year': event_year})
    except:
        redirect('login')


def Villa_terms_conditions(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'Room/villa-terms-conditions.html', {'cart_count': cart_count, 'event_year': event_year})