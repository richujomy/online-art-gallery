from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.artwork_list, name='artwork_list'),
    path('<int:artwork_id>/', views.artwork_detail, name='artwork_detail'),
    path('upload/', views.upload_artwork, name='upload_artwork'),
    path('send-message/', views.send_message, name='send_message'),
    path('get-messages/<int:artwork_id>/', views.get_messages, name='get_messages'),
    path('check-new-messages/', views.check_new_messages, name='check_new_messages'),
]
