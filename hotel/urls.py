from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('room/<int:room_type_id>/', views.room_detail, name='room_detail'),
    path('booking/', views.booking, name='booking'),
    path('booking/<int:room_id>/', views.booking, name='booking_with_room'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('check-availability/', views.check_availability, name='check_availability'),
]