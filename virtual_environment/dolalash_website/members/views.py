from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from . import database
from .user import User

# Create your views here.

def generate_html_view(path_to_html: str):
    def view(request):
        context = {
            "is_logged_in": User.is_logged_in,
            "full_name": f"{User.fname} {User.lname}",
            "email": User.email,
            "phone": User.phone,
            "username": User.username,
        }
        return render(request, path_to_html, context)
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

    user_data = matches[0]
    User.login(user_data)
    context = {
        "is_logged_in": User.is_logged_in,
        "full_name": f"{User.fname} {User.lname}",
        "email": User.email,
        "phone": User.phone,
        "username": User.username,        
    }
    return render(request, "login_success.html", context)    
    # validate credentials
    
def logout(request):
    User.logout()
    context = {
        "is_logged_in": User.is_logged_in,
        "full_name": f"{User.fname} {User.lname}",
        "email": User.email,
        "phone": User.phone,
        "username": User.username,
    }
    return render(request, "home.html", context)

home = generate_html_view("index.html")
services = generate_html_view("services.html")
about = generate_html_view("about-us.html")
contact = generate_html_view("contact.html")
login_signup = generate_html_view("log-in-and-sign-up-page.html")
book = generate_html_view("forms.html")
forgot_password = generate_html_view("forgot-password.html")
