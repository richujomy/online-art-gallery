from django.db import models

# Create your models here.
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

# Choices for user roles
ROLE_CHOICES = [
    ('customer', 'Customer'),
    ('designer', 'Designer'),
    ('admin', 'Admin'),
]

# Model for User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to the User model
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')  # User role

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def is_designer(self):
        return self.role == 'designer'

    def is_customer(self):
        return self.role == 'customer'