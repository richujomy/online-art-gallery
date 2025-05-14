from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class ArtworkReviewForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=True,
        label="Reason for approval/rejection"
    )