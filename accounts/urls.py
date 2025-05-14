from django.urls import path, include
from . import views

app_name = 'accounts'



urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

    path('designer/dashboard/', views.designer_dashboard, name='designer_dashboard'),
    path('designer/update_artwork/<int:artwork_id>', views.update_artwork, name='update_artwork'),

    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/artwork_approval/', views.admin_artwork_approval, name='admin_artwork_approval'),
    path('admin/artwork_approve/<int:artwork_id>', views.approve_artwork, name='approve_artwork'),
    path('admin/artwork_reject/<int:artwork_id>', views.reject_artwork, name='reject_artwork'),
    path('admin/manage_artists', views.manage_artists, name='manage_artists'),
    path('admin/remove_artist/<int:artist_id>', views.remove_artist, name='remove_artist'),
    path('admin/manage_artowrks/',views.manage_artworks,name='manage_artworks'),
    path('admin/remove_artowrk/<int:artwork_id>',views.remove_artwork,name='remove_artwork'),
    path('admin/manage_customers/',views.manage_customers,name='manage_customers'),
    path('admin/remove_customer/<int:customer_id>',views.remove_customer, name='remove_customer'),

    path('admin/artwork/approve-ajax/', views.approve_artwork_ajax, name='approve_artwork_ajax'),
    path('admin/artwork/reject-ajax/', views.reject_artwork_ajax, name='reject_artwork_ajax'),
]
