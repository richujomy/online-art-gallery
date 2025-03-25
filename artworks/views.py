from django.shortcuts import render, get_object_or_404, redirect
from .models import Artwork
from .forms import ArtworkForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.db.models import Q


from django.db.models import Q

def artwork_list(request):
    query = request.GET.get('search', '')
    
    # Filter approved artworks
    artworks = Artwork.objects.filter(status='approved')
    
    # If there's a search query, filter the artworks
    if query:
        artworks = artworks.filter(
            Q(title__icontains=query) |  # Search in title
            Q(designer__username__icontains=query) |  # Search by designer username
            Q(description__icontains=query) |  # Search in description
            Q(category__icontains=query)  # Search in category
        )
    
    context = {
        'artworks': artworks,
        'search_query': query
    }
    
    return render(request, 'artworks/artwork_list.html', context)

@login_required
def artwork_detail(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)  # Fetch a specific artwork
    return render(request, 'artworks/artwork_details.html', {'artwork': artwork})


@login_required
def upload_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)  # Handle form submission
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.designer = request.user  # Assign the logged-in user as the designer
            artwork.save()
            messages.success(request, "New Artwork Added Successfully")
            return redirect('upload_artwork')  
    else:
        form = ArtworkForm()  # display an empty form for GET requests
    return render(request, 'artworks/upload_artwork.html', {'form': form})


