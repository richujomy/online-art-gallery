from django.shortcuts import render, get_object_or_404, redirect
from .models import Artwork
from .forms import ArtworkForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Profile


@login_required
def artwork_list(request):
    artworks = Artwork.objects.filter(status='approved')  # Fetch all artworks from the database
    return render(request, 'artworks/artwork_list.html', {'artworks': artworks})

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


