from django.urls import path, re_path
from sixerrapp import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path('gigs/(?P<id>[0-9]+)/$', views.gig_detail, name='gig_detail'),
]
