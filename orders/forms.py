from django import forms
from django.core.validators import RegexValidator
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
    
    # Basic field validations
    first_name = forms.CharField(
        max_length=50,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s\-\']+$',
                message="Invalid First name",
                code='invalid_first_name'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    
    last_name = forms.CharField(
        max_length=50,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s\-\']+$',
                message="Invalid Last name.",
                code='invalid_last_name'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    
    street_address = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Textarea(
            attrs={
                'rows': 2,
                'placeholder': 'Enter your street address',
            }
        )
    )
    
    city = forms.CharField(
        max_length=50,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s\-\'\.]+$',
                message="Invalid City.",
                code='invalid_city'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Enter your city'})
    )
    
    state = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your state/province'})
    )
    
    postal_code = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter postal/zip code'})
    )
    
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        required=True
    )
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'street_address', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'street_address': forms.Textarea(attrs={'rows': 2}),
        }
    
    def clean_postal_code(self):
        """Validate postal code format based on selected country"""
        postal_code = self.cleaned_data.get('postal_code')
        country = self.cleaned_data.get('country')
        
        if not postal_code:
            return postal_code
            
        # Different validation rules for different countries
        if country == 'USA':
            # US ZIP code: 5 digits or 5+4 format
            if not (re.match(r'^\d{5}$', postal_code) or re.match(r'^\d{5}-\d{4}$', postal_code)):
                raise forms.ValidationError("Enter a valid US ZIP code (e.g., 12345 or 12345-6789).")
        elif country == 'CAN':
            # Canadian postal code: A1A 1A1 format
            if not re.match(r'^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$', postal_code):
                raise forms.ValidationError("Enter a valid Canadian postal code (e.g., A1A 1A1).")
        elif country == 'UK':
            # UK postal code format validation
            if not re.match(r'^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$', postal_code.upper()):
                raise forms.ValidationError("Enter a valid UK postal code.")
        elif country == 'AUS':
            # Australian postal code: 4 digits
            if not re.match(r'^\d{4}$', postal_code):
                raise forms.ValidationError("Enter a valid Australian postal code (4 digits).")
        elif country == 'IND':
            # Indian postal code: 6 digits
            if not re.match(r'^\d{6}$', postal_code):
                raise forms.ValidationError("Enter a valid Indian PIN code (6 digits).")
                
        return postal_code
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        
        # Example of conditional validation based on country
        country = cleaned_data.get('country')
        state = cleaned_data.get('state')
        
        if country == 'USA' and state:
            # Validate US state abbreviations
            us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
                        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 
                        'DC', 'AS', 'GU', 'MP', 'PR', 'VI']
            
            if len(state) == 2 and state.upper() not in us_states:
                self.add_error('state', 'Enter a valid US state abbreviation.')
                
        return cleaned_data