# artworks/forms.py
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from .models import Artwork

class ArtworkForm(forms.ModelForm):
    # Size format validation
    size = forms.CharField(
        max_length=100,
        help_text="Format: Width x Height (cm), e.g., '30x30'",
        validators=[
            RegexValidator(
                regex=r'^\d+x\d+$',
                message="Size must be in format 'width x height', e.g., '30x30'"
            )
        ]
    )
        
    # Price validation
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(10, message="Price must be at least ₹10"),
            MaxValueValidator(1000000, message="Price cannot exceed ₹1,000,000")
        ],
        help_text="Price in ₹ (Min: ₹10, Max: ₹1,000,000)"
    )
    
    # Title validation
    title = forms.CharField(
        max_length=200,
        min_length=3,
        help_text="Title should be between 3-200 characters",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter artwork title',
            'class': 'title-field'
        })
    )
    
    # Description validation with minimum length
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Describe your artwork (min 10 characters)',
            'class': 'description-field'
        }),
        min_length=10,
        max_length=2000,
        help_text="Minimum 10 characters, maximum 2000"
    )

    # Image field with validation
    image = forms.ImageField(
        help_text="Upload an image (JPG, PNG, WEBP). Max size: 5MB",
        error_messages={
            'invalid_image': "Upload a valid image. The file you uploaded is either not an image or corrupted.",
            'missing': "Please select an image file to upload."
        }
    )
    
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'price', 'size', 'category', 'image']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'category-select'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required with custom error messages
        for field_name, field in self.fields.items():
            field.required = True
            field.error_messages = {
                'required': f"Please provide the {field_name} of your artwork."
            }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (limit to 5MB)
            if image.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise ValidationError("Image file too large. Size should not exceed 5MB.")
                
            # Check file extension
            allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
            ext = image.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError(f"Unsupported file extension. Use: {', '.join(allowed_extensions)}")
                
        return image
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Check if title contains only valid characters
        if title and not all(c.isalnum() or c.isspace() or c in '-_,.!?' for c in title):
            raise ValidationError("Title contains invalid characters. Use letters, numbers, and basic punctuation only.")
        return title