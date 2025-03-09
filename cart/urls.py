from django.urls import path, include
from .import views

app_name= 'cart'

urlpatterns =[
    path('',views.cart_view,name="cart"),
    path('add/<int:artwork_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:artwork_id>/', views.remove_from_cart, name='remove_from_cart'),
]