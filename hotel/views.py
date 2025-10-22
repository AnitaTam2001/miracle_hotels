from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import RoomType, Room, Booking, Contact
from django.utils import timezone

def home(request):
    room_types = RoomType.objects.all()
    return render(request, 'home.html', {'room_types': room_types})

def rooms(request):
    room_types = RoomType.objects.all()
    return render(request, 'rooms.html', {'room_types': room_types})

def room_detail(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    available_rooms = Room.objects.filter(room_type=room_type, is_available=True)
    return render(request, 'room_detail.html', {
        'room_type': room_type,
        'available_rooms': available_rooms
    })

def booking(request, room_id=None):
    room = None
    if room_id:
        room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        guest_email = request.POST.get('guest_email')
        guest_phone = request.POST.get('guest_phone')
        room_id = request.POST.get('room')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        
        room_obj = get_object_or_404(Room, id=room_id)
        
        # Calculate total price
        from datetime import datetime
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        nights = (check_out_date - check_in_date).days
        total_price = nights * room_obj.room_type.price_per_night
        
        booking = Booking.objects.create(
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            room=room_obj,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status='pending'
        )
        
        messages.success(request, 'Booking submitted successfully! We will contact you soon.')
        return redirect('home')
    
    rooms = Room.objects.filter(is_available=True)
    if room:
        rooms = rooms.filter(room_type=room.room_type)
    
    return render(request, 'booking.html', {'rooms': rooms, 'selected_room': room})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'contact.html')

def check_availability(request):
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        
        # Get rooms that are not booked for the selected dates
        booked_rooms = Booking.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in,
            status__in=['pending', 'confirmed']
        ).values_list('room_id', flat=True)
        
        available_rooms = Room.objects.filter(
            is_available=True
        ).exclude(id__in=booked_rooms)
        
        room_types = RoomType.objects.filter(
            room__in=available_rooms
        ).distinct()
        
        return render(request, 'availability.html', {
            'room_types': room_types,
            'check_in': check_in,
            'check_out': check_out
        })
    
    return render(request, 'check_availability.html')