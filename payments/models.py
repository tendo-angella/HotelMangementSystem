from django.db import models
from guests.models import Guest
from rooms.models import Room  # Imports the Room model so we can link payments to specific rooms

# Create your models here.
class Payment(models.Model):
    # This list creates the options for the dropdown menu in your forms
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Mobile Money', 'Mobile Money'),
        ('Card', 'Credit/Debit Card'),
    ]

    # Links the payment to a specific guest; if the guest is deleted, their payments are also removed
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    
    # Links the payment to a room; SET_NULL keeps the payment record even if the room is deleted later
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True) 
    
    # Stores the money amount; max_digits=10 allows for amounts up to 99,999,999.99 (plenty for Shillings!)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Automatically records the exact date and time when the payment is created
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # Stores the method used; defaults to Mobile Money as it is the most common
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='Mobile Money')
    
    # An optional field to store receipt numbers or Mobile Money reference codes
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # This controls how the payment appears in the Django Admin and dropdown lists
        # It shows the amount in Shillings, the Guest's name, and the Room number
        room_no = self.room.room_number if self.room else 'N/A'
        return f"Shs {self.amount_paid} - {self.guest.first_name} (Room {room_no})"
