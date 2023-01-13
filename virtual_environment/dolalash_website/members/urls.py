from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('handle_registration/', views.handle_registration, name='handle_registration'),
    path('handle_login/', views.handle_login, name='handle_login'),
]
