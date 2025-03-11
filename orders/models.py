from django.db import models

# Create your models here.
# orders/models.py
from django.db import models
from django.contrib.auth.models import User
from artworks.models import Artwork

# Model for Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_status = models.CharField(max_length=50, default='Pending')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.artwork.title} (User: {self.user.username})"