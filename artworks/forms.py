# artworks/forms.py
from django import forms
from .models import Artwork

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'price', 'size', 'category', 'image']