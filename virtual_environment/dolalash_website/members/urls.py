from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about-us/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('log-in-and-sign-up-page/', views.login_signup, name='login_signup'),
    path('book/', views.book, name='book'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
 ]
