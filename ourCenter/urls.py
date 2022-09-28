from django.contrib import admin
from django.urls import path
from ourCenter import views


urlpatterns = [
    path('our-centers/', views.our_center),
    path('our-centers/center-details/<str:name>/', views.centerDetails),
    path('our-centers/who-collaborating-centre-for-health-innovation/', views.whocc),
    path('service-query/<int:id>/', views.service_contact),
]