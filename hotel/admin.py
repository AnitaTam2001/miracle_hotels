from django.contrib import admin
from .models import RoomType, Room, Booking, Contact

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_night', 'capacity']
    list_filter = ['capacity']
    search_fields = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'is_available']
    list_filter = ['room_type', 'is_available']
    search_fields = ['room_number']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'guest_name', 'room', 'check_in', 'check_out', 'status']
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['guest_name', 'guest_email']
    readonly_fields = ['created_at']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']