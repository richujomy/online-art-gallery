from django.db import models

# Create your models here.
# artworks/models.py
from django.db import models
from django.contrib.auth.models import User


# Model for Artwork
class Artwork(models.Model):
    # Choices for art types
    CATEGORY_CHOICES = [
        ('painting', 'Painting'),
        ('digital_art', 'Digital Art'),
        ('drawing', 'Drawing'),
        ('sculpture', 'Sculpture'),
        ('traditional_art', 'Traditional Art'),
    ]

    STATUS_COICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)  
    image = models.ImageField(upload_to='artworks/')  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  
    designer = models.ForeignKey(User, on_delete=models.CASCADE) 
    sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices= STATUS_COICES, default='pending')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def __str__(self):
        return f"{ self.title} - {self.designer.username}" 
    

    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @is_approved.setter
    def is_approved(self, value):
        if value:
            self.status = 'approved'
        else:
            self.status = 'pending'