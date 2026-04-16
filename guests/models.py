from django.db import models
from django.core.exceptions import ValidationError
from rooms.models import Room

class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=17)
    email = models.EmailField(unique=True)
    id_number = models.CharField(max_length=20, unique=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="guests")

    def clean(self):
        print("--- DEBUG: THE CLEAN METHOD IS RUNNING! ---")

        if len(self.phone_number) < 9:
            raise ValidationError({'phone_number': "Phone number is too short!"})
        
 
        check_digits = self.phone_number.replace('+', '')
        if not check_digits.isdigit():
            raise ValidationError({'phone_number': "Only numbers and + allowed."})
        
        if self.first_name.lower() == self.last_name.lower():
            raise ValidationError({
                'last_name': "First name and last name cannot be the same. Please check for errors."
        })
        
        if not self.first_name.isalpha():
            print(f"DEBUG: Found a number in {self.first_name}")
            raise ValidationError({'first_name': "Names should only contain letters, no numbers or symbols."})
        
        if not self.last_name.isalpha():
            raise ValidationError({'last_name': "Names should only contain letters, no numbers or symbols."})


        if len(self.id_number) < 5:
            raise ValidationError({'id_number': "This ID number seems too short."})

    def save(self, *args, **kwargs):
        # This forces the clean() rules to run every time
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"