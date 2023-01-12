from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def generate_html_view(path_to_html: str):    
    def view(request):
        template = loader.get_template(path_to_html)
        return HttpResponse(template.render())
    return view

home = generate_html_view("home.html")
services = generate_html_view("services.html")
products = generate_html_view("products.html")
profile = generate_html_view("profile.html")
about = generate_html_view("about.html")
register = generate_html_view("register.html")
