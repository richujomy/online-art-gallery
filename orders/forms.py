from django import forms
from accounts.models import Profile
from .models import Order

class AddressForm(forms.ModelForm):
    COUNTRY_CHOICES = [
        ('', 'Select Country'),
        ('USA', 'United States'),
        ('CAN', 'Canada'),
        ('UK', 'United Kingdom'),
        ('AUS', 'Australia'),
        ('IND', 'India'),
        # Add more countries as needed
    ]

    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'street_address', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'street_address': forms.Textarea(attrs={'rows': 2}),
        }

