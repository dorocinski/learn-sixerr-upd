from django.urls import path, re_path
from sixerrapp import views

urlpatterns = [
    path('', views.home, name='home'),
    #re_path('gigs/(?P<id>[0-9]+)/$', views.gig_detail, name='gig_detail'),
    path('gigs/<int:id>/', views.gig_detail, name='gig_detail'),
    path('my_gigs/', views.my_gigs, name='my_gigs'),
    path('create_gig/', views.create_gig, name='create_gig'),
    path('edit_gig/<int:id>/', views.edit_gig, name='edit_gig'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('checkout/', views.create_purchase, name='create_purchase'),
    path('my_buyings/', views.my_buyings, name='my_buyings'),
    path('my_sellings/', views.my_sellings, name='my_sellings'),
]

# Help for URL PAtterns: https://consideratecode.com/2018/05/02/django-2-0-url-to-path-cheatsheet/
