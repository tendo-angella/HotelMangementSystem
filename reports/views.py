from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone  # New: Used to get today's date
from rooms.models import Room
from guests.models import Guest
from payments.models import Payment

def dashboard(request):
    # --- Existing Stats ---
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(is_occupied=True).count()
    available_rooms = total_rooms - occupied_rooms
    total_guests = Guest.objects.count()

    # --- Financial Stats (Overall) ---
    total_revenue = Payment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    # --- NEW: Daily Report Stats ---
    # We get today's date from the server
    today = timezone.now().date()
    
    # We filter payments where the payment_date "starts with" today's date
    daily_revenue = Payment.objects.filter(
        payment_date__date=today
    ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    context = {
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': available_rooms,
        'total_guests': total_guests,
        'total_revenue': total_revenue,
        'daily_revenue': daily_revenue, # Added to context
        'today': today,
    }
    
    return render(request, 'dashboard.html', context)