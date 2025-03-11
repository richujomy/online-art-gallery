from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),  # For cart checkout
    path('checkout/<int:artwork_id>/', views.checkout, name='checkout'),  # For Buy Now
    path('enter-address/<str:artwork_ids>/', views.enter_address, name='enter_address'),  # Address entry
    path('order-summary/<str:artwork_ids>/', views.order_summary, name='order_summary'),  # Order summary
    path('payment/<str:artwork_ids>/', views.payment, name='payment'),  # Payment
    path('order-success/', views.order_success, name='order_success'),  # Success page
]
