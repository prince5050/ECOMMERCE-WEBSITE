from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View


class Login(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email

                return redirect('product_page')
            else:
                error_message = 'Email or password invalid !!'
        else:
            error_message = 'Email or password invalid !!'

        print(email, password)
        return render(request, 'auth/login.html', {'error': error_message})
