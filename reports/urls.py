from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pole/<int:id>/', views.pole_detail, name='pole_detail'),
    path('about/', views.about, name='about'),
    path('track/', views.track_complaint, name = 'track_complaint'),
]