from django.urls import path
from . import views


urlpatterns = [
    path('room-search/', views.room_search, name='room_search'),
    path('room-list/', views.room_list, name='room_list'),
    path('book-now/<str:id>/', views.book_now, name='book_now'),
    path('room_handleResp/', views.room_handleResp),
    path('Booked-room/', views.Dashboard, name='dashboard'),
    path('Villa-terms-conditions/', views.Villa_terms_conditions),
    ]