from django.contrib import admin
from .models import Artwork, ArtworkMessage
# Register your models here.

admin.site.register(Artwork)

admin.site.register(ArtworkMessage)