from django.db import models

# Create your models here.
# cart/models.py
from django.db import models
from django.contrib.auth.models import User
from artworks.models import Artwork

# Model for Cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links cart to a user
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)  # Links cart to an artwork
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart item #{self.id} - {self.artwork.title} (User: {self.user.username})"