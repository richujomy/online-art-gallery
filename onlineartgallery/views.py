from django.shortcuts import render,redirect
from artworks.models import Artwork  
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone

def home(request):

    artworks = Artwork.objects.filter(status='approved').order_by('-created_at')[:4]
    
    designers = Profile.objects.filter(role='designer').select_related('user')
    categories = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in Artwork.CATEGORY_CHOICES
    ]

    price_ranges = [
        {'value': '0-10000', 'label': 'Under ₹10,000'},
        {'value': '10000-50000', 'label': '₹10,000 - ₹50,000'},
        {'value': '50000+', 'label': 'Above ₹50,000'},
    ]
    
    sort_options = [
        {'value': 'newest', 'label': 'Newest First'},
        {'value': 'price_low', 'label': 'Price: Low to High'},
        {'value': 'price_high', 'label': 'Price: High to Low'},
    ]
    
    context = {
        'artworks': artworks,
        'designers': designers,
        'categories': categories,
        'price_ranges': price_ranges,
        'sort_options': sort_options,
        'current_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'current_user': request.user.username if request.user.is_authenticated else None
    }
    
    return render(request, 'home.html', context)
