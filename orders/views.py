from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from artworks.models import Artwork
from .forms import AddressForm
from .models import Order

@login_required
def checkout(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # If address is missing, redirect to enter address page
    if not all([profile.first_name, profile.last_name, profile.street_address, 
                profile.city, profile.state, profile.postal_code, profile.country]):
        return redirect('enter_address', artwork_id=artwork.id)

    return redirect('order_summary', artwork_id=artwork.id)



# Address Entry View
@login_required
def enter_address(request, artwork_id):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('order_summary', artwork_id=artwork_id)  # Redirect to order summary
    else:
        form = AddressForm(instance=profile)

    return render(request, 'orders/address_form.html', {'form': form})



# Order Summary View
@login_required
def order_summary(request, artwork_id):
    profile = Profile.objects.get(user=request.user)
    artwork = get_object_or_404(Artwork, id=artwork_id)

    return render(request, 'orders/order_summary.html', {'profile': profile, 'artwork': artwork})



# Payment View
@login_required
def payment(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    if artwork.sold:
        return redirect('home')

    if request.method == 'POST':
        order = Order.objects.create(
            user = request.user,
            artwork = artwork,
            quantity = 1,
            total_price = artwork.price,
            payment_status = 'Completed',
        )
        artwork.sold = True
        artwork.save()
        return redirect('order_success')

    return render(request, 'orders/payment.html', {'artwork': artwork})



# Order Success View
@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')