from datetime import datetime, timedelta
from django.contrib import messages
from django.shortcuts import render, redirect
from store.models.product import *
from store.models.events import *
from store.models.internship import *
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from ourCenter.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from ecommerce.models import *
import requests
# Create your views here
#.
#
def product_category(request, name):
    products = None
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        all_product = Product.get_all_products()
        product = Product.get_all_products_by_categoryid(categoryID)
        product_count = product.count()
        # paginator = Paginator(product, 9)
        # page_number = request.GET.get('page')
        # products = paginator.get_page(page_number)
        event_year = Event_year.objects.filter(status='1')

        data = {'products': product, 'categories': categories, 'category_name': name, 'product_count': product_count, 'cart_count': cart_count,
               'all_product': all_product, 'event_year': event_year}
        return render(request, 'shop/product_category.html', data)

class Products(View):
    def post(self, request):
        product = request.POST.get('products')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product] = quantity+1
            else:
                cart[product] = 1

        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('shop/products.html')

    def get(self, request):
        products = None
        Cart_Count(request)
        cart_count = settings.CART_COUNT
        # request.session.clear.get('cart').clear()
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        all_product = Product.get_all_products()
        if categoryID:
            product = Product.get_all_products_by_categoryid(categoryID)
            product_count = product.count()
            # paginator = Paginator(product, 9)
            # page_number = request.GET.get('page')
            # products = paginator.get_page(page_number)
            event_year = Event_year.objects.filter(status='1')

            data = {'products': product, 'categories': categories, 'product_count': product_count, 'cart_count': cart_count, 'event_year': event_year, 'all_product': all_product}
            return render(request, 'shop/product_category.html', data)
        else:
            product = Product.get_all_products()[0:9]
            product_count = product.count()
            # paginator = Paginator(product, 9)
            # page_number = request.GET.get('page')
            # products = paginator.get_page(page_number)
            event_year = Event_year.objects.filter(status='1')
            data = {'products': product, 'categories': categories, 'product_count': product_count, 'cart_count': cart_count, 'all_product': all_product, 'event_year': event_year}
            return render(request, 'shop/products.html', data)

def product_search(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    all_product = Product.get_all_products()
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        if product_name != '':
            product_obj = Product.objects.filter(Q(product_name__startswith=product_name) | Q(product_name__icontains=product_name), status='1')
            product_count = product_obj.count()
            if product_count >0:
                categories = Category.get_all_categories()
                event_year = Event_year.objects.filter(status='1')
                data = {'products': product_obj, 'categories': categories, 'cart_count': cart_count, 'all_product': all_product, 'event_year': event_year}
                return render(request, 'shop/product_category.html', data)
            else:
                messages.error(request, 'No Matching Product Found')
                return redirect('product_page')

        else:
            messages.error(request, 'No Matching Product Found')
            return redirect('product_page')
    else:
        product = Product.get_all_products()[0:9]
        product_count = product.count()
        categories = Category.get_all_categories()
        event_year = Event_year.objects.filter(status='1')
        data = {'products': product, 'categories': categories, 'product_count': product_count, 'cart_count': cart_count, 'all_product': all_product, 'event_year': event_year}
        return render(request, 'shop/products.html', data)

def product_with_price(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    product_obj = Product.objects.filter(~Q(product_price=None))[0:9]
    product_count = product_obj.count()
    all_product = Product.get_all_products()
    if product_count > 0:
        categories = Category.get_all_categories()
        event_year = Event_year.objects.filter(status='1')
        data = {'products': product_obj, 'categories': categories, 'cart_count': cart_count, 'all_product': all_product,
                        'event_year': event_year}
        return render(request, 'shop/product_price_avaliable.html', data)
    else:
        product = Product.get_all_products()[0:9]
        product_count = product.count()
        categories = Category.get_all_categories()
        event_year = Event_year.objects.filter(status='1')
        data = {'products': product, 'categories': categories, 'product_count': product_count, 'cart_count': cart_count, 'all_product': all_product,
                'event_year': event_year}
        messages.error(request, 'No Matching Product Found')
        return render(request, 'shop/products.html', data)


def product_without_price(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    product_obj = Product.objects.filter(product_price=None)[0:9]
    product_count = product_obj.count()
    all_product = Product.get_all_products()
    if product_count > 0:
        categories = Category.get_all_categories()
        event_year = Event_year.objects.filter(status='1')
        data = {'products': product_obj, 'categories': categories, 'cart_count': cart_count, 'all_product': all_product,
                        'event_year': event_year}
        return render(request, 'shop/product_without_price.html', data)
    else:
        product = Product.get_all_products()[0:9]
        product_count = product.count()
        categories = Category.get_all_categories()
        event_year = Event_year.objects.filter(status='1')
        data = {'products': product, 'categories': categories, 'product_count': product_count, 'cart_count': cart_count, 'all_product': all_product,
                'event_year': event_year}
        messages.error(request, 'No Matching Product Found')
        return render(request, 'shop/products.html', data)



def price_high_to_low(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    product_obj = Product.objects.filter(~Q(product_price=None)).order_by('-product_price')[0:9]
    product_count = product_obj.count()
    all_product = Product.get_all_products()
    if product_count > 0:
        categories = Category.get_all_categories()
        event_year = Event_year.objects.filter(status='1')
        data = {'products': product_obj, 'categories': categories, 'cart_count': cart_count, 'all_product': all_product,
                'event_year': event_year}
        return render(request, 'shop/product_price_high_to_low.html', data)
    else:
        product = Product.get_all_products()[0:9]
        product_count = product.count()
        categories = Category.get_all_categories()
        event_year = Event_year.objects.filter(status='1')
        data = {'products': product, 'categories': categories, 'product_count': product_count, 'cart_count': cart_count, 'all_product': all_product,
                'event_year': event_year}
        messages.error(request, 'No Matching Product Found')
        return render(request, 'shop/products.html', data)


def price_low_to_high(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    all_product = Product.get_all_products()
    product_obj = Product.objects.filter(~Q(product_price=None)).order_by('product_price')[0:9]
    product_count = product_obj.count()
    if product_count > 0:
        categories = Category.get_all_categories()
        event_year = Event_year.objects.filter(status='1')
        data = {'products': product_obj, 'categories': categories, 'cart_count': cart_count, 'all_product': all_product,
                'event_year': event_year}
        return render(request, 'shop/product_price_low_to_high.html', data)
    else:
        product = Product.get_all_products()[0:9]
        product_count = product.count()
        categories = Category.get_all_categories()
        event_year = Event_year.objects.filter(status='1')
        data = {'products': product, 'categories': categories, 'product_count': product_count, 'cart_count': cart_count, 'all_product': all_product,
                'event_year': event_year}
        messages.error(request, 'No Matching Product Found')
        return render(request, 'shop/products.html', data)

def load_more(request):
    offset = int(request.POST['offset'])
    limit = 6
    posts = Product.objects.filter(status='1')[offset:limit+offset]
    html_code = ''
    for list_data in posts:
       html_code += '<div class="col-lg-4 col-md-6 col-sm-12 col-12 post-box text-center">'
       html_code += '<a href="/products/'+str(replace_name(list_data.product_name))+'/' + str(list_data.pk) + '">'
       html_code += '<div class=" card single-service h-90" style="height: 353px;" >'
       html_code += '<div class="card-header p-0" style="height:200px;">'
       if list_data.product_image:
           html_code += ' <img class="img-product" style="padding:0%;" src="' + list_data.product_image.url + '" alt="'+list_data.product_name+'"title="'+list_data.product_name+'" />'
       html_code += '</div>'
       html_code += '<div class="card-body text-left"style="height: 112px;"> <h6>' + list_data.product_name + '</h6>'
       html_code += '<div class="text-left">'
       if list_data.discount_type == 'Rs':
           html_code += '<h6 style="font-size:14px;">Price : <strike>₹ ' + str(list_data.product_price) + '.00</strike>'
           html_code += '< span >₹ ' + str(list_data.product_price - list_data.discount_amount_or_per) + '</span >< span class ="badge badge-success " style="font-size:12px;" >'+ str(list_data.discount_amount_or_per) + ' ' + list_data.discount_type + 'Off </span>'
           if list_data.gst != '0':
               html_code += '< small > +GST' + str(list_data.gst) + '% < / small >'
           html_code += '</h6>'
       elif list_data.discount_type == '%':
           html_code += ' <h6>Price : <strike>₹' + list_data.product_price + '.00</strike>'
           html_code += '<span>₹' + str(percentage_cal(list_data.product_price, list_data.discount_amount_or_per)) + ' < / span >'
           html_code += '<span class="badge badge-success " style="font-size:12px;">' + str(list_data.discount_amount_or_per) + ' ' + list_data.discount_type + ' Off </span>'
           if list_data.gst != '0':
               html_code += '<small>+GST ' + str(list_data.gst) + '</small>'
           html_code += '</h6>'
       else:
           html_code += '<h6>Price : <span>'
           if list_data.product_price != None:
               html_code += '₹ ' + str(list_data.product_price) + '.00'
           else:
               html_code += '<span class="badge badge-success"> Ask for Price'
           html_code += '</span>'
           if list_data.gst != '0':
               html_code += '<span>+GST ' + str(list_data.gst) + '%</span>'
           html_code += '</h6>'
       html_code += '</div></div>'
       html_code += '<div class="card-footer m-0 p-0" ><div class ="row" style="margin-left:.5px;margin-right:.5px" > '
       html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-primary" style = "border-radius:0; cursor:pointer;" onclick = "showModal(\'' + str(list_data.product_name) + '\',\'' + str(list_data.pk) + '\')" data-toggle="modal" data-target=".bd-example-modal-lg" ><a style="color:white;font-weight: 500;" > Enquiry </a></button>'

       if list_data.product_price != None:
           html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" data-target=".bd-example-modal-lg"><a style="color:black; font-weight: 500;" href = "/Add-cart/' + str(list_data.pk) + '" > Add to Cart </a></button>'

       else:
           html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" disabled>Add to Cart</button>'
       html_code += '</div></div></div></a></div>'



    total_data = posts.count()
    # posts_json = serializers.serialize('json', posts)
    return JsonResponse(data={
        'posts': html_code,
        'totalResult': total_data
    })

def load_more_product_with_price(request):
    offset = int(request.POST['offset'])
    limit = 6
    posts = Product.objects.filter(~Q(product_price=None))[offset:limit + offset]
    html_code = ''
    for list_data in posts:
        html_code += '<div class="col-lg-4 col-md-6 col-sm-12 col-12 post-box text-center">'
        html_code += '<a href="/products/' + str(replace_name(list_data.product_name)) + '/' + str(list_data.pk) + '">'
        html_code += '<div class=" card single-service h-90" style="height: 353px;" >'
        html_code += '<div class="card-header p-0" style="height:200px;">'
        if list_data.product_image:
            html_code += ' <img class="img-product" style="padding:0%;" src="' + list_data.product_image.url + '" alt="' + list_data.product_name + '"title="' + list_data.product_name + '" />'
        html_code += '</div>'
        html_code += '<div class="card-body text-left"style="height: 112px;"> <h6>' + list_data.product_name + '</h6>'
        html_code += '<div class="text-left">'
        if list_data.discount_type == 'Rs':
            html_code += '<h6 style="font-size:14px;">Price : <strike>₹ ' + str(
                list_data.product_price) + '.00</strike>'
            html_code += '< span >₹ ' + str(
                list_data.product_price - list_data.discount_amount_or_per) + '</span >< span class ="badge badge-success " style="font-size:12px;" >' + str(
                list_data.discount_amount_or_per) + ' ' + list_data.discount_type + 'Off </span>'
            if list_data.gst != '0':
                html_code += '< small > +GST' + str(list_data.gst) + '% < / small >'
            html_code += '</h6>'
        elif list_data.discount_type == '%':
            html_code += ' <h6>Price : <strike>₹' + list_data.product_price + '.00</strike>'
            html_code += '<span>₹' + str(
                percentage_cal(list_data.product_price, list_data.discount_amount_or_per)) + ' < / span >'
            html_code += '<span class="badge badge-success " style="font-size:12px;">' + str(
                list_data.discount_amount_or_per) + ' ' + list_data.discount_type + ' Off </span>'
            if list_data.gst != '0':
                html_code += '<small>+GST ' + str(list_data.gst) + '</small>'
            html_code += '</h6>'
        else:
            html_code += '<h6>Price : <span>'
            if list_data.product_price != None:
                html_code += '₹ ' + str(list_data.product_price) + '.00'
            else:
                html_code += '<span class="badge badge-success"> Ask for Price'
            html_code += '</span>'
            if list_data.gst != '0':
                html_code += '<span>+GST ' + str(list_data.gst) + '%</span>'
            html_code += '</h6>'
        html_code += '</div></div>'
        html_code += '<div class="card-footer m-0 p-0" ><div class ="row" style="margin-left:.5px;margin-right:.5px" > '
        html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-primary" style = "border-radius:0; cursor:pointer;" onclick = "showModal(\'' + str(
            list_data.product_name) + '\',\'' + str(
            list_data.pk) + '\')" data-toggle="modal" data-target=".bd-example-modal-lg" ><a style="color:white;font-weight: 500;" > Enquiry </a></button>'

        if list_data.product_price != None:
            html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" data-target=".bd-example-modal-lg"><a style="color:black; font-weight: 500;" href = "/Add-cart/' + str(
                list_data.pk) + '" > Add to Cart </a></button>'

        else:
            html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" disabled>Add to Cart</button>'
        html_code += '</div></div></div></a></div>'

    total_data = posts.count()
    # posts_json = serializers.serialize('json', posts)
    return JsonResponse(data={
        'posts': html_code,
        'totalResult': total_data
    })

def load_more_product_without_price(request):
    offset = int(request.POST['offset'])
    limit = 6
    posts = Product.objects.filter(product_price=None)[offset:limit + offset]
    html_code = ''
    for list_data in posts:
        html_code += '<div class="col-lg-4 col-md-6 col-sm-12 col-12 post-box text-center">'
        html_code += '<a href="/products/' + str(replace_name(list_data.product_name)) + '/' + str(list_data.pk) + '">'
        html_code += '<div class=" card single-service h-90" style="height: 353px;" >'
        html_code += '<div class="card-header p-0" style="height:200px;">'
        if list_data.product_image:
            html_code += ' <img class="img-product" style="padding:0%;" src="' + list_data.product_image.url + '" alt="' + list_data.product_name + '"title="' + list_data.product_name + '" />'
        html_code += '</div>'
        html_code += '<div class="card-body text-left"style="height: 112px;"> <h6>' + list_data.product_name + '</h6>'
        html_code += '<div class="text-left">'
        if list_data.discount_type == 'Rs':
            html_code += '<h6 style="font-size:14px;">Price : <strike>₹ ' + str(
                list_data.product_price) + '.00</strike>'
            html_code += '< span >₹ ' + str(
                list_data.product_price - list_data.discount_amount_or_per) + '</span >< span class ="badge badge-success " style="font-size:12px;" >' + str(
                list_data.discount_amount_or_per) + ' ' + list_data.discount_type + 'Off </span>'
            if list_data.gst != '0':
                html_code += '< small > +GST' + str(list_data.gst) + '% < / small >'
            html_code += '</h6>'
        elif list_data.discount_type == '%':
            html_code += ' <h6>Price : <strike>₹' + list_data.product_price + '.00</strike>'
            html_code += '<span>₹' + str(
                percentage_cal(list_data.product_price, list_data.discount_amount_or_per)) + ' < / span >'
            html_code += '<span class="badge badge-success " style="font-size:12px;">' + str(
                list_data.discount_amount_or_per) + ' ' + list_data.discount_type + ' Off </span>'
            if list_data.gst != '0':
                html_code += '<small>+GST ' + str(list_data.gst) + '</small>'
            html_code += '</h6>'
        else:
            html_code += '<h6>Price : <span>'
            if list_data.product_price != None:
                html_code += '₹ ' + str(list_data.product_price) + '.00'
            else:
                html_code += '<span class="badge badge-success"> Ask for Price'
            html_code += '</span>'
            if list_data.gst != '0':
                html_code += '<span>+GST ' + str(list_data.gst) + '%</span>'
            html_code += '</h6>'
        html_code += '</div></div>'
        html_code += '<div class="card-footer m-0 p-0" ><div class ="row" style="margin-left:.5px;margin-right:.5px" > '
        html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-primary" style = "border-radius:0; cursor:pointer;" onclick = "showModal(\'' + str(
            list_data.product_name) + '\',\'' + str(
            list_data.pk) + '\')" data-toggle="modal" data-target=".bd-example-modal-lg" ><a style="color:white;font-weight: 500;" > Enquiry </a></button>'

        if list_data.product_price != None:
            html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" data-target=".bd-example-modal-lg"><a style="color:black; font-weight: 500;" href = "/Add-cart/' + str(
                list_data.pk) + '" > Add to Cart </a></button>'

        else:
            html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" disabled>Add to Cart</button>'
        html_code += '</div></div></div></a></div>'

    total_data = posts.count()
    # posts_json = serializers.serialize('json', posts)
    return JsonResponse(data={
        'posts': html_code,
        'totalResult': total_data
    })

def load_more_product_price_high_to_low(request):
    offset = int(request.POST['offset'])
    limit = 6
    posts = Product.objects.filter(~Q(product_price=None)).order_by('-product_price')[offset:limit + offset]
    html_code = ''
    for list_data in posts:
        html_code += '<div class="col-lg-4 col-md-6 col-sm-12 col-12 post-box text-center">'
        html_code += '<a href="/products/' + str(replace_name(list_data.product_name)) + '/' + str(list_data.pk) + '">'
        html_code += '<div class=" card single-service h-90" style="height: 353px;" >'
        html_code += '<div class="card-header p-0" style="height:200px;">'
        if list_data.product_image:
            html_code += ' <img class="img-product" style="padding:0%;" src="' + list_data.product_image.url + '" alt="' + list_data.product_name + '"title="' + list_data.product_name + '" />'
        html_code += '</div>'
        html_code += '<div class="card-body text-left"style="height: 112px;"> <h6>' + list_data.product_name + '</h6>'
        html_code += '<div class="text-left">'
        if list_data.discount_type == 'Rs':
            html_code += '<h6 style="font-size:14px;">Price : <strike>₹ ' + str(
                list_data.product_price) + '.00</strike>'
            html_code += '< span >₹ ' + str(
                list_data.product_price - list_data.discount_amount_or_per) + '</span >< span class ="badge badge-success " style="font-size:12px;" >' + str(
                list_data.discount_amount_or_per) + ' ' + list_data.discount_type + 'Off </span>'
            if list_data.gst != '0':
                html_code += '< small > +GST' + str(list_data.gst) + '% < / small >'
            html_code += '</h6>'
        elif list_data.discount_type == '%':
            html_code += ' <h6>Price : <strike>₹' + list_data.product_price + '.00</strike>'
            html_code += '<span>₹' + str(
                percentage_cal(list_data.product_price, list_data.discount_amount_or_per)) + ' < / span >'
            html_code += '<span class="badge badge-success " style="font-size:12px;">' + str(
                list_data.discount_amount_or_per) + ' ' + list_data.discount_type + ' Off </span>'
            if list_data.gst != '0':
                html_code += '<small>+GST ' + str(list_data.gst) + '</small>'
            html_code += '</h6>'
        else:
            html_code += '<h6>Price : <span>'
            if list_data.product_price != None:
                html_code += '₹ ' + str(list_data.product_price) + '.00'
            else:
                html_code += '<span class="badge badge-success"> Ask for Price'
            html_code += '</span>'
            if list_data.gst != '0':
                html_code += '<span>+GST ' + str(list_data.gst) + '%</span>'
            html_code += '</h6>'
        html_code += '</div></div>'
        html_code += '<div class="card-footer m-0 p-0" ><div class ="row" style="margin-left:.5px;margin-right:.5px" > '
        html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-primary" style = "border-radius:0; cursor:pointer;" onclick = "showModal(\'' + str(
            list_data.product_name) + '\',\'' + str(
            list_data.pk) + '\')" data-toggle="modal" data-target=".bd-example-modal-lg" ><a style="color:white;font-weight: 500;" > Enquiry </a></button>'

        if list_data.product_price != None:
            html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" data-target=".bd-example-modal-lg"><a style="color:black; font-weight: 500;" href = "/Add-cart/' + str(
                list_data.pk) + '" > Add to Cart </a></button>'

        else:
            html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" disabled>Add to Cart</button>'
        html_code += '</div></div></div></a></div>'

    total_data = posts.count()
    # posts_json = serializers.serialize('json', posts)
    return JsonResponse(data={
        'posts': html_code,
        'totalResult': total_data
    })

def load_more_product_price_low_to_high(request):
    offset = int(request.POST['offset'])
    limit = 6
    posts = Product.objects.filter(~Q(product_price=None)).order_by('product_price')[offset:limit + offset]
    html_code = ''
    for list_data in posts:
        html_code += '<div class="col-lg-4 col-md-6 col-sm-12 col-12 post-box text-center">'
        html_code += '<a href="/products/' + str(replace_name(list_data.product_name)) + '/' + str(list_data.pk) + '">'
        html_code += '<div class=" card single-service h-90" style="height: 353px;" >'
        html_code += '<div class="card-header p-0" style="height:200px;">'
        if list_data.product_image:
            html_code += ' <img class="img-product" style="padding:0%;" src="' + list_data.product_image.url + '" alt="' + list_data.product_name + '"title="' + list_data.product_name + '" />'
        html_code += '</div>'
        html_code += '<div class="card-body text-left"style="height: 112px;"> <h6>' + list_data.product_name + '</h6>'
        html_code += '<div class="text-left">'
        if list_data.discount_type == 'Rs':
            html_code += '<h6 style="font-size:14px;">Price : <strike>₹ ' + str(
                list_data.product_price) + '.00</strike>'
            html_code += '< span >₹ ' + str(
                list_data.product_price - list_data.discount_amount_or_per) + '</span >< span class ="badge badge-success " style="font-size:12px;" >' + str(
                list_data.discount_amount_or_per) + ' ' + list_data.discount_type + 'Off </span>'
            if list_data.gst != '0':
                html_code += '< small > +GST' + str(list_data.gst) + '% < / small >'
            html_code += '</h6>'
        elif list_data.discount_type == '%':
            html_code += ' <h6>Price : <strike>₹' + list_data.product_price + '.00</strike>'
            html_code += '<span>₹' + str(
                percentage_cal(list_data.product_price, list_data.discount_amount_or_per)) + ' < / span >'
            html_code += '<span class="badge badge-success " style="font-size:12px;">' + str(
                list_data.discount_amount_or_per) + ' ' + list_data.discount_type + ' Off </span>'
            if list_data.gst != '0':
                html_code += '<small>+GST ' + str(list_data.gst) + '</small>'
            html_code += '</h6>'
        else:
            html_code += '<h6>Price : <span>'
            if list_data.product_price != None:
                html_code += '₹ ' + str(list_data.product_price) + '.00'
            else:
                html_code += '<span class="badge badge-success"> Ask for Price'
            html_code += '</span>'
            if list_data.gst != '0':
                html_code += '<span>+GST ' + str(list_data.gst) + '%</span>'
            html_code += '</h6>'
        html_code += '</div></div>'
        html_code += '<div class="card-footer m-0 p-0" ><div class ="row" style="margin-left:.5px;margin-right:.5px" > '
        html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-primary" style = "border-radius:0; cursor:pointer;" onclick = "showModal(\'' + str(
            list_data.product_name) + '\',\'' + str(
            list_data.pk) + '\')" data-toggle="modal" data-target=".bd-example-modal-lg" ><a style="color:white;font-weight: 500;" > Enquiry </a></button>'

        if list_data.product_price != None:
            html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" data-target=".bd-example-modal-lg"><a style="color:black; font-weight: 500;" href = "/Add-cart/' + str(
                list_data.pk) + '" > Add to Cart </a></button>'

        else:
            html_code += '<button  type ="button" class="col-lg-6 col-md-6 col-sm-6 col-6 btn btn-warning"  style = "border-radius:0" disabled>Add to Cart</button>'
        html_code += '</div></div></div></a></div>'

    total_data = posts.count()
    # posts_json = serializers.serialize('json', posts)
    return JsonResponse(data={
        'posts': html_code,
        'totalResult': total_data
    })


def product_details(request, id, product_name):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    all_product = Product.get_all_products()
    try:

        product_list = Product.objects.get(pk=id)
        category_obj = product_list.category
        category = Product.objects.filter(~Q(pk=id), category=category_obj)[0:8]
        event_year = Event_year.objects.filter(status='1')
        data = {'product_details': product_list, 'categories':  category, 'cart_count': cart_count, 'all_product': all_product, 'event_year': event_year}
        return render(request, 'shop/product_details.html', data)
    except Exception as e:
        return render(request, 'home.html')
def Cart_Count(request):
    user_id = request.user.id
    cart_item_count = Cart.objects.filter(user_id=user_id, status='1')
    settings.CART_COUNT = cart_item_count.count()

def index(request):
    Cart_Count(request)
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'home.html', {'cart_count': cart_count, 'event_year': event_year})


def contact(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'contact.html', {'cart_count': cart_count, 'event_year': event_year})


# def tenders(request):
#     return render(request, 'tenders.html')


def request_quote(request):
    return render(request, 'shop/requestQuote.html')


def sendmail(request, message=None):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        subject = request.POST['subject']
        message = request.POST['message']
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            Contact_request.objects.create(fullname=name, email=email,  mobile_number=mobile,
                                           subject=subject, message=message)

            send_mail_contact(name, email, mobile, subject, message)
            messages.success(request, "Mail send successfully")
            return redirect('contact')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('contact')
    else:
        messages.error(request, "Mail not send")
        return render(request, 'contact.html')


def quotation(request, message=None):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        product_name = request.POST['product_name']
        Other_product1 = request.POST.get('Other_product1')
        Other_product2 = request.POST.get('Other_product2')
        quantity1 = request.POST.get('quantity1')
        quantity2 = request.POST.get('quantity2')
        fullname = request.POST['fullname']
        mobile = request.POST.get('mobile')
        subject = request.POST['subject']
        message = request.POST['message']
        user_email = request.POST['email']
        quantity = request.POST['quantity']
        try:
            Qutation_request.objects.create(product_id=product_id, Product_name=product_name, fullname=fullname,
                                            email=user_email, subject=subject, message=message, mobile_number=mobile,
                                            quantity=quantity, other_product_name1=Other_product1, other_product_qty1=quantity1,
                                            other_product_name2=Other_product2, other_product_qty2=quantity2)

            # send_mail(subject, message, from_email, ['prince.singh@amtz.in'], fail_silently=False)
            if Other_product1 == None and Other_product2 == None:
                send_mail_Qutation(fullname, user_email, mobile, product_name, subject, message)
            elif Other_product1 == None and Other_product2 is not None:
                Other_product1 = ''
                send_mail_Qutation1(fullname, user_email, mobile, product_name, quantity,
                                    Other_product1, quantity1, Other_product2, quantity2, subject, message)
            elif Other_product2 == None and Other_product1 is not None:
                Other_product2 = ''
                send_mail_Qutation1(fullname, user_email, mobile, product_name, quantity,
                                    Other_product1, quantity1, Other_product2, quantity2, subject, message)

            else:
                send_mail_Qutation1(fullname, user_email, mobile, product_name, quantity,
                                    Other_product1, quantity1, Other_product2, quantity2, subject, message)
            messages.success(request, "Qutation Mail send successfully")
            return redirect('ProductDetails', id=product_id, product_name=replace_name(product_name))
        except:
            messages.success(request, "Qutation Mail not send Something went wrong")
            return redirect('ProductDetails', id=product_id, product_name=replace_name(product_name))
    else:
        return redirect('product_page')

def send_mail_Qutation(name, user_email, mobile, product_name, user_subject, message):
    subject = f'Qutation Request for {product_name}'
    message = f'Hello AMTZ Sales, \nWe have an enquiry email from AMTZ website for Quotation.\n' \
              f'{name} want to Qutation for {product_name}\n \n' \
              f'Customer Name : {name}\nEmail : {user_email}\nCustomer Mobile Number : {mobile}\n\n' \
              f'Subject : {user_subject}\n' \
              f'Message : \n{message}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['Sales@amtz.in']
    send_mail(subject, message, email_from, recipient_list)

def send_mail_Qutation1(name, user_email, mobile, product_name, quantity, product_name1, quantity1, product_name2, quantity2, user_subject, message):
    subject = f'Qutation Request for {product_name}, {product_name1}, {product_name2}'
    message = f'Hello AMTZ Sales, \nWe have an enquiry email from AMTZ website for Quotation.\n' \
              f'{name} want to Qutation for {product_name} : QTY- {quantity},{product_name1} : QTY- {quantity1},{product_name2}: QTY- {quantity2},\n \n' \
              f'Customer Name : {name}\nEmail : {user_email}\nCustomer Mobile Number : {mobile}\n\n' \
              f'Subject : {user_subject}\n' \
              f'Message : \n{message}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['Sales@amtz.in']
    send_mail(subject, message, email_from, recipient_list)

def send_mail_contact(name, email, mobile, user_subject, message):
    subject = f'Contact Request From Amtz Website'
    message = f'Hello AMTZ Team, \nThis mail is come from your Amtz website \n' \
              f'{name} want to Contact related to {user_subject}\n \n' \
              f'Sender Name : {name}\nEmail : {email}\nSender Mobile Number : {mobile}\n\n' \
              f'Subject : {user_subject}\n' \
              f'Message : \n{message}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['info@amtz.in']
    send_mail(subject, message, email_from, recipient_list)

def our_hubs(request):
    cart_count = settings.CART_COUNT
    hub_obj = OurHub.objects.filter(status='1').order_by('-id').reverse
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'our_hubs.html', {'hub_obj': hub_obj, 'cart_count': cart_count, 'event_year': event_year})


def manufactureUnit(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'manufacturing_units.html', {'cart_count': cart_count, 'event_year': event_year})


def amphenolSensor(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'amphenol.html', {'cart_count': cart_count, 'event_year': event_year})


def partners(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'partners.html', {'cart_count': cart_count, 'event_year': event_year})
def services(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    service_obj = OurService.objects.filter(status='1').order_by('-id').reverse
    return render(request, 'services.html', {'services': service_obj, 'cart_count': cart_count, 'event_year': event_year})

def services_details(request, name):
    try:
        center_id = request.GET["key"]
        cart_count = settings.CART_COUNT
        service_obj = OurService.objects.filter(id=center_id)
        ser_obj = OurService.objects.filter(id=center_id)[0]
        service_name = ser_obj.service_title
        event_year = Event_year.objects.filter(status='1')
        return render(request, 'service_details.html', {'services': service_obj, 'cart_count': cart_count,
                                                       'title': ser_obj.meta_title, 'description': ser_obj.meta_discription, 'name': service_name, 'event_year': event_year})
    except:
        return redirect('services')
def latest_notification(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    req_obj = Latest_notification.objects.filter(status='1')
    return render(request, 'latest_notification.html', {'cart_count': cart_count, 'event_year': event_year,
                                                        'req_obj': req_obj})

def handler404(request, exception):
    return render(request, 'home.html', status=404)

def internship(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        email = request.POST['email']
        Phone = request.POST['Phone']
        Address = request.POST['Address']
        Zipcode = request.POST['Zipcode']
        country = request.POST['country']
        state = request.POST['state']
        highest_education = request.POST['highest_education']
        name_of_study = request.POST['name_of_study']
        education_datefrom = request.POST['education_datefrom']
        education_dateto = request.POST['education_dateto']
        Organization = request.POST['Organization']
        designation = request.POST['designation']
        date_from = request.POST['date_from']
        date_to = request.POST['date_from']
        responsibilities = request.POST['responsibilities']
        experience = request.POST['experience']
        resume = request.FILES.get('resume')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:

                try:
                    Internship_Application.objects.create(first_name=fname, last_name=lname, gender=gender,
                                            email=email, Phone=Phone, Address=Address, Zipcode=Zipcode, country=country,
                                                          state=state, highest_education=highest_education, name_of_study=name_of_study,
                                                          education_date_from=education_datefrom, education_date_to=education_dateto, Organization=Organization,
                                                          designation=designation, date_from=date_from, date_to=date_to, responsibilities=responsibilities,
                                                          experience=experience,  resume=resume)
                    internship_mail(fname, lname, email, Phone, )
                    return render(request, 'internship_form.html', {'message': 'Application Send Successfully',
                                                                    'cart_count': cart_count, 'event_year': event_year})

                except:
                    return render(request, 'internship_form.html', {'error': 'Something Went wrong',
                                                                    'cart_count': cart_count, 'event_year': event_year})

        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('internship_form')
    else:
        return render(request, 'internship_form.html', {'cart_count': cart_count, 'event_year': event_year})


def pre_qualification(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'pre_qualification.html', {'cart_count': cart_count, 'event_year': event_year})


def brochures(request):
    return render(request, 'information/brochures.html')


def manufacturing_center(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/manufacturingInsent.html', {'cart_count': cart_count,
                                                                    'event_year': event_year})

def privacy(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'privacy.html', {'cart_count': cart_count, 'event_year': event_year})
def terms_condition(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'terms&conditions.html', {'cart_count': cart_count, 'event_year': event_year})
def innovation(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'innovation.html', {'cart_count': cart_count, 'event_year': event_year})
def preferential_market(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/preferential-market.html', {'cart_count': cart_count, 'event_year': event_year})
def incentive_scheme(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/incentive-scheme.html', {'cart_count': cart_count, 'event_year': event_year})
def RTI(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/RTI.html', {'cart_count': cart_count, 'event_year': event_year})
def elder_innovation(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/elder-inovation.html', {'cart_count': cart_count, 'event_year': event_year})
def women_innovation(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/women-innovation.html', {'cart_count': cart_count, 'event_year': event_year})

def bio_printing_innovation_call(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/bio_printing_innovation_call.html', {'cart_count': cart_count, 'event_year': event_year})

def biovalley_Innovation_Call(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/Biovalley-Innovation-Call.html',
                  {'cart_count': cart_count, 'event_year': event_year})


def auction_notice(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/Auction-notice.html', {'cart_count': cart_count, 'event_year': event_year})

def past_events(request, id):
    cart_count = settings.CART_COUNT
    pastevent_obj = Event.objects.filter(Event_year=id, Start_date__lte=datetime.now()-timedelta(days=1), end_date__lte=datetime.now()-timedelta(days=1), status='1').order_by('Start_date').reverse()
    paginator = Paginator(pastevent_obj, 9)
    page_number = request.GET.get('page')
    pastevents = paginator.get_page(page_number)
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'events/pastevent.html', {'pastevents': pastevents, 'cart_count': cart_count, 'event_year': event_year})

def past_event_details(request, id):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    event_obj = Event.objects.filter(id=id, status='1')
    return render(request, 'events/pastevent-details.html', {'pastevents': event_obj, 'event_year': event_year, 'cart_count': cart_count})

def ongoing_events(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    pastevent_obj = Event.objects.filter(Start_date__lte=datetime.now(), end_date__gte=datetime.now(), status='1').order_by('Start_date').reverse()
    return render(request, 'events/ongoingevents.html', {'ongoingevents': pastevent_obj, 'cart_count': cart_count, 'event_year': event_year})
def upcoming_events(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    pastevent_obj = Event.objects.filter(Start_date__gte=datetime.now()+timedelta(days=1), status='1').order_by('Start_date').reverse()
    return render(request, 'events/upcomingevents.html', {'upcomingevents': pastevent_obj, 'cart_count': cart_count, 'event_year': event_year})

def request_for_service(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        subject = 'Request for Service'
        message = request.POST['message']
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            Contact_request.objects.create(fullname=name, email=email, mobile_number=mobile,
                                           subject=subject, message=message)

            send_mail_contact(name, email, mobile, subject, message)
            event_year = Event_year.objects.filter(status='1')
            messages.success(request, 'Request message send successfully...')
            return render(request, 'home.html', {'event_year': event_year})
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('home')

    else:
        messages.error(request, "Mail not send")
        event_year = Event_year.objects.filter(status='1')
        return render(request, 'home.html', {'event_year': event_year})

def news(request):
    cart_count = settings.CART_COUNT
    news_obj = News.objects.filter(status='1').order_by('news_date').reverse()
    paginator = Paginator(news_obj, 9)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'events/news.html', {'news': news, 'cart_count': cart_count, 'event_year': event_year})

def percentage_cal(actual_price, percentage):
    after_percentage = int(actual_price) - int(actual_price)*int(percentage)/100;
    return after_percentage


def internship_mail(fname, lname, email, Phone):
    subject = f'INTERNSHIP APPLICATION REQUEST FROM YOUR AMTZ WEBSITE'
    message = f'Hello,\n     AMTZ HR Team \n     This mail is come from your Amtz website \n' \
              f'     {fname} {lname} Submit Internship Application. please Check the HR Admin Panel\n \n' \
              f'     Applicant Name : {fname} {lname}\n    Applicant Email : {email}\n     Applicant Mobile Number : {Phone}\n\n' \

    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['hr@amtz.in']
    send_mail(subject, message, email_from, recipient_list)


# Publicaytion sub-menu function .
def dossiers(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'publication/dossiers.html', {'cart_count': cart_count, 'event_year': event_year})
def market_intelligence(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'publication/market_intelligence.html', {'cart_count': cart_count, 'event_year': event_year})
def intellectual_property(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'publication/intellectual_property.html', {'cart_count': cart_count, 'event_year': event_year})
def distributor_empanelment(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/distributor-form.html', {'cart_count': cart_count, 'event_year': event_year})

def skill_lync(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/training/skill-lync.html', {'cart_count': cart_count, 'event_year': event_year})

def training(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    return render(request, 'information/training/training.html', {'cart_count': cart_count, 'event_year': event_year})

def our_videos(request):
    cart_count = settings.CART_COUNT
    event_year = Event_year.objects.filter(status='1')
    videos = Our_video.objects.filter(status='1').order_by('id')
    paginator = Paginator(videos, 12)
    page_number = request.GET.get('page')
    video = paginator.get_page(page_number)
    return render(request, 'events/our_videos.html', {'cart_count': cart_count, 'event_year': event_year, 'video': video})

def replace_name(strs):
    new_str = strs.replace(" ", "-")
    new_str1 = new_str.replace("|", "of")
    new_str2 = new_str1.replace("&", "and")
    new_str2 = new_str2.lower()
    return new_str2

def v2home_privacy(request):
    return render(request, 'v2home_privacy.html')