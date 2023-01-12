from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from . import database

# Create your views here.

def generate_html_view(path_to_html: str):
    def view(request):
        template = loader.get_template(path_to_html)
        return render(request, path_to_html)
    return view

@csrf_protect
def handle_registration(request):
    # a dict containing the form answers
    form_data = request.POST

    # add data to database
    credentials = {
        "username": form_data["username"],
        "password": form_data["password"],
    }

    profile = {
        "fname": form_data["fname"],
        "lname": form_data["lname"],
        "email": form_data["email"],
        "phone": form_data["phone"],
    }
    
    database.insert("userdb", "credentials", credentials)
    database.insert("userdb", "profiles", profile)
    
    return render(request, "register_success.html")

@csrf_protect
def handle_login(request):
    form_data = request.POST

    credentials = {
        "username": form_data["username"],
        "password": form_data["password"],
    }

    # validate credentials

home = generate_html_view("home.html")
services = generate_html_view("services.html")
products = generate_html_view("products.html")
profile = generate_html_view("profile.html")
about = generate_html_view("about.html")
register = generate_html_view("register.html")
