from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Profile
from artworks.models import Artwork
from cart.models import Cart
from .forms import AddressForm
from .models import Order


@login_required
def checkout(request, artwork_id=None):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # if address is missing, redirect to enter address page
    if not all([profile.first_name, profile.last_name, profile.street_address, 
                profile.city, profile.state, profile.postal_code, profile.country]):
        return redirect('enter_address') 

    if artwork_id:  # Case 1: "Buy Now" - Single artwork checkout
        artwork = get_object_or_404(Artwork, id=artwork_id)
        items_to_checkout = [artwork]
    else:  # Case 2: "Checkout from Cart" - Multiple artworks
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.warning(request, "Your cart is empty!")
            return redirect('cart:cart')
        items_to_checkout = [item.artwork for item in cart_items]

    return redirect('order_summary', artwork_ids=",".join(str(item.id) for item in items_to_checkout))




@login_required
def enter_address(request, artwork_ids):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('order_summary', artwork_ids=artwork_ids) 
    else:
        form = AddressForm(instance=profile)

    return render(request, 'orders/address_form.html', {'form': form})




@login_required
def order_summary(request, artwork_ids):
    if not artwork_ids: 
        return redirect('cart:cart')

    artwork_ids_list = artwork_ids.split(",")  # Convert "1,2,3" → ["1", "2", "3"]
    artworks = Artwork.objects.filter(id__in=artwork_ids_list)
    profile = Profile.objects.get(user=request.user)  

    return render(request, "orders/order_summary.html", {
        "artworks": artworks,
        'profile': profile,
        "artwork_ids": artwork_ids  
    })





# Payment View
@login_required
def payment(request, artwork_ids):
    artwork_ids = artwork_ids.split(",") 
    artworks = Artwork.objects.filter(id__in=artwork_ids)

    # Prevent ordering sold artworks
    if any(art.sold for art in artworks):
        return redirect('home')

    total_price = sum(art.price for art in artworks)  # Calculate total price
    if request.method == 'POST':

        # Create separate orders for each artwork
        for art in artworks:
            Order.objects.create(
                user=request.user,
                artwork=art,
                quantity=1,
                total_price=art.price,  # each artwork has its own price
                payment_status='Completed',
            )
            art.sold = True  # Mark as sold
            art.save()

        return redirect('order_success')

    return render(request, 'orders/payment.html', {'artworks': artworks,'total_price': total_price,})


# Order Success View
@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')