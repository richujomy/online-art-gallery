from django.shortcuts import render,redirect
from artworks.models import Artwork  
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    # Fetch the first 4 artworks for the home page preview
    artworks = Artwork.objects.all()[:4]
    
    # Fetch all profiles where role is 'designer'
    designers = Profile.objects.filter(role='designer').select_related('user')
    
    # Pass both artworks and designers to the template
    return render(request, 'home.html', {
        'artworks': artworks,
        'designers': designers
    })




