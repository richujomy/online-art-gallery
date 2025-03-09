from django.db import models

# Create your models here.
# orders/models.py
from django.db import models
from django.contrib.auth.models import User
from artworks.models import Artwork

# Model for Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links order to a user
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)  # Links order to an artwork
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the artwork in the order
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the order
    payment_status = models.CharField(max_length=50, default='Pending')  # Payment status (e.g., Pending, Completed)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.artwork.title} (User: {self.user.username})"