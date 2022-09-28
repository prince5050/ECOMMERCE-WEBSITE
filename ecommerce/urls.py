from django.contrib import admin
from django.urls import path
from ecommerce import views


urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('verify/<auth_token>', views.verify),
    path('cart/', views.cart, name='cart'),
    path('Add-cart/<int:id>/', views.Add_cart),
    path('delete-item/<int:product_id>/', views.delete_product),
    path('quantity-change/', views.quantity_change),
    path('buy-item$1/', views.delivery_address, name='delivery_address'),
    path('buy-item/', views.delivery_form),
    path('buy-item$2/<int:address_id>/', views.checkout),
    path('edit-address/<int:address_id>/', views.edit_address),
    path('delete-address/<int:address_id>/', views.delete_address),
    path('edit-address$2/', views.edit_address_form),
    path('state/', views.load_state),
    path('buy-item$3/', views.checkout, name='checkout'),
    path('handleResp/', views.handleResponse, name='RU'),
    path('myOrder/', views.my_order, name='order'),
    path('order-details/<str:order_id>/', views.order_details),
    path('logout/', views.logout_request),
    path('forgot-password/', views.forgot_password),
    path('change-password/', views.change_password, name="change_password"),
    path('profile/', views.profile, name="profile"),
    path('update_profile/', views.update_profile),
    path('state_change/', views.state_change),
    path('user-dashboard/', views.user_dashboard),
    path('reset-password/', views.reset_password),
    path('quantity-change-buy/', views.quantity_change_buy),
    path('buy-now/', views.buy_now),
    # path('refund-form/', views.refund_form),



]