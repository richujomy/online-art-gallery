from django.shortcuts import render, redirect
from artworks.models import Artwork
from .models import Cart
from django.contrib import messages
# Create your views here.

def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user, artwork__sold=False)
    total_price = sum(item.artwork.price for item in cart_items)
    return render(request, "cart/cart.html" , {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, artwork_id):
    artwork = Artwork.objects.get(id = artwork_id)
    cart_item , created = Cart.objects.get_or_create(artwork= artwork,
                                                user = request.user)
    if created:
        messages.success(request, 'Item added to Cart')
    else:
        messages.warning(request, 'Item already in Cart')

    cart_item.save()
    return redirect('cart:cart')

def remove_from_cart(request, artwork_id):
    cart_item = Cart.objects.get(artwork_id = artwork_id, user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from cart")
    return redirect('cart:cart')

