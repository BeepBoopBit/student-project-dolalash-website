from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
]
