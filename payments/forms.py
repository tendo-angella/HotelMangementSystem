from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['guest', 'room', 'amount_paid', 'payment_method', 'transaction_id']
        
        widgets = {
            'guest': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount in Shs'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM Reference / Receipt No'}),
        }

        error_messages = {
            'guest': {
                'required': "Please select the guest who is making the payment.",
            },
            'room': {
                'required': "Which room is being paid for?",
            },
            'amount_paid': {
                'required': "You must enter the amount in Shillings.",
                'invalid': "Please enter a valid number for the price.",
            },
            'payment_method': {
                'required': "Please select how the guest paid (Cash, MM, or Card).",
            }
        }