from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.artwork_list, name='artwork_list'),
    path('<int:artwork_id>/', views.artwork_detail, name='artwork_detail'),
    path('upload/', views.upload_artwork, name='upload_artwork'),
    
]
