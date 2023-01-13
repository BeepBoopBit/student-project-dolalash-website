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
    form_data = {}
    for key, value in request.POST.items():
        form_data[key] = value

    # check if username already exists
    query_username = { "username": form_data["username"] }
    matches_username = database.find("userdb", "users", query_username)

    query_email = { "email": form_data["email"] }
    matches_email = database.find("userdb", "users", query_email)

    # if there is a match, abort registrtion
    if len(matches_username) > 0 or len(matches_email) > 0:
        return render(request, "register_fail.html")

    # else
    database.insert("userdb", "users", form_data)    
    return render(request, "register_success.html")

@csrf_protect
def handle_login(request):
    form_data = request.POST

    credentials = {
        "username": form_data["username"],
        "password": form_data["password"],
    }

    # find account matching the credentials
    matches = database.find("userdb", "users", credentials)

    # if there are no accounts, credentials are wrong. abort
    if len(matches) == 0:
        return render(request, "login_fail.html")
        
    return render(request, "login_success.html")
    
    # validate credentials

home = generate_html_view("home.html")
services = generate_html_view("services.html")
products = generate_html_view("products.html")
profile = generate_html_view("profile.html")
about = generate_html_view("about.html")
register = generate_html_view("register.html")
login = generate_html_view("login.html")
