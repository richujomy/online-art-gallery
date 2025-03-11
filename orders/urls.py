from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:artwork_id>/', views.checkout, name='checkout'),  # Checkout for specific artwork
    path('enter-address/<int:artwork_id>/', views.enter_address, name='enter_address'),  # Address entry
    path('order-summary/<int:artwork_id>/', views.order_summary, name='order_summary'),  # Order summary
    path('payment/<int:artwork_id>/', views.payment, name='payment'),  # Payment
    path('order-success/', views.order_success, name='order_success'),  # Success page
]
