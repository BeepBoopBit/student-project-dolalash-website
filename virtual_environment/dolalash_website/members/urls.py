from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about-us/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('log-in-and-sign-up-page/', views.login_signup, name='login_signup'),
    path('book/', views.book, name='book'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('handle_registration/', views.handle_registration, name='handle_registration'),
    path('handle_login/', views.handle_login, name='handle_login'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('handle_booking/', views.handle_booking, name='handle_booking')
 ]
