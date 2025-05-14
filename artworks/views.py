from django.shortcuts import render, get_object_or_404, redirect
from .models import Artwork
from .forms import ArtworkForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.db.models import Q
from django.http import JsonResponse
from .models import ArtworkMessage



def artwork_list(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    price_range = request.GET.get('price_range', '')
    sort_by = request.GET.get('sort_by', '')

    artworks = Artwork.objects.filter(status='approved')

    #search filter
    if query:
        artworks = artworks.filter(
            Q(title__icontains=query) |  
            Q(designer__username__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__icontains=query)  
        )

    if category:
        artworks = artworks.filter(category=category)

    #price range filter
    if price_range:
        if price_range == '0-10000':
            artworks = artworks.filter(price__lte=10000)
        elif price_range == '10000-50000':
            artworks = artworks.filter(price__gt=10000, price__lte=50000)
        elif price_range == '50000+':
            artworks = artworks.filter(price__gt=50000)

    #sorting
    if sort_by:
        if sort_by == 'price_low':
            artworks = artworks.order_by('price')
        elif sort_by == 'price_high':
            artworks = artworks.order_by('-price')
    else:
        artworks = artworks.order_by('-created_at')

    categories = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in Artwork.CATEGORY_CHOICES
    ]

    context = {
        'artworks': artworks,
        'search_query': query,
        'categories': categories,
        'selected_category': category,
        'price_range': price_range,
        'sort_by': sort_by,
    }
    
    return render(request, 'artworks/artwork_list.html', context)


@login_required
def artwork_detail(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id) 
    return render(request, 'artworks/artwork_details.html', {'artwork': artwork})


@login_required
def upload_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES) 
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.designer = request.user 
            artwork.save()
            messages.success(request, "New Artwork Added Successfully")
            return redirect('upload_artwork')  
    else:
        form = ArtworkForm() 
    return render(request, 'artworks/upload_artwork.html', {'form': form})



@login_required
def send_message(request):
    if request.method == 'POST':
        artwork_id = request.POST.get('artwork_id')
        message_text = request.POST.get('message')
        artwork = get_object_or_404(Artwork, id=artwork_id)
        
        message = ArtworkMessage.objects.create(
            artwork=artwork,
            sender=request.user,
            receiver=artwork.designer,
            message=message_text
        )
        
        return JsonResponse({
            'status': 'success',
            'message': {
                'text': message.message,
                'sender': message.sender.username,
                'created_at': message.created_at.strftime('%B %d, %Y, %I:%M %p')
            }
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_messages(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    messages = ArtworkMessage.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        artwork=artwork
    ).order_by('created_at').values(
        'message',
        'sender__username',
        'created_at'
    )
    
    return JsonResponse({'messages': list(messages)})

@login_required
def check_new_messages(request):
    """View to check for new unread messages"""
    unread_count = ArtworkMessage.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({'unread_count': unread_count})