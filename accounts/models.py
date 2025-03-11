from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('customer', 'Customer'),
    ('designer', 'Designer'),
    ('admin', 'Admin'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    # address Fields
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)  # Can be a dropdown in the form

    def __str__(self):
        return f"{self.user.username} - {self.role}"
