from django import forms
from .models import Guest
from rooms.models import Room
from django.core.exceptions import ValidationError # Needed for error messages

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'id_number', 'room']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +256...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Passport or ID number'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'id_number': 'National ID / Passport Number',
            'room': 'Assign to Room No',
        }

        #  error messages...
        error_messages = {
            'first_name': {'required': "Please enter the guest's first name."},
            'last_name': {'required': "Please enter the guest's last name."},
            'email': {'invalid': "This email address doesn't look right. Please check it.", 
                      'unique': "A guest with this email is already registered.",},
            'id_number': {'unique': "This ID/Passport number already exists in our records."},
            'phone_number': {'required': "We need a phone number to contact the guest."},
        }

    def __init__(self, *args, **kwargs):
        super(GuestForm, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(is_occupied=False)

    # --- VALIDATION RULES ---

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        
        # Rule 1: Only alphabets (no numbers or spaces)
        if not name.isalpha():
            raise ValidationError("First name must only contain letters.")
            
        # Rule 2: More than 2 characters
        if len(name) <= 2:
            raise ValidationError("First name must be longer than 2 characters.")
            
        return name

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name')
        
        if not name.isalpha():
            raise ValidationError("Last name must only contain letters.")
            
        if len(name) <= 2:
            raise ValidationError("Last name must be longer than 2 characters.")
            
        return name