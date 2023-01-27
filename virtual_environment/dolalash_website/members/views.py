from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from . import database
from .user import User
from pprint import pprint
from .PyCa import PyCaMod
import pathlib
from datetime import datetime, time
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

def generate_html_view(path_to_html: str):
    def view(request):
        return render(request, path_to_html)
    return view

@csrf_protect
def handle_registration(request):
    # a dict containing the form answers
    form_data = dict(request.POST.items())
    form_data.pop("csrfmiddlewaretoken", None)

    form_data["first_name"] = form_data["first_name"].strip()
    form_data["last_name"] = form_data["last_name"].strip()

    pprint(form_data)
    
    do_passwords_match = form_data["password"] == form_data["confirm_password"]
    if not do_passwords_match:
        print("Passwords do not match.")
        print("Registration aborted.")
        return redirect("/log-in-and-sign-up-page")

    form_data.pop("confirm_password")
    database.connect("mongodb+srv://watermelon:ThisIsWatermelon073@cluster0.vrjatpa.mongodb.net/?retryWrites=true&w=majority")
    
    # check if username is already registered.
    query_username = { "username": form_data["username"] }
    matches_username = database.find("userdb", "users", query_username)
    is_username_unique = len(matches_username) == 0
    if not is_username_unique:
        print(f"Username {form_data['username']} already registered.")
        print("Registration aborted.")    
        return redirect("/log-in-and-sign-up-page")

    # check if email is already registered.
    query_email = { "email": form_data["email"] }
    matches_email = database.find("userdb", "users", query_email)
    is_email_unique = len(matches_email) == 0
    if not is_email_unique:
        print(f"Email {form_data['email']} already registered.")
        print("Registration aborted.")    
        return redirect("/log-in-and-sign-up-page")

    # if this point is reached, then everything is valid
    # add to database
    database.insert("userdb", "users", form_data)
    print("Registration successful!")
    
    return redirect("/log-in-and-sign-up-page")

@csrf_protect
def handle_login(request):
    form_data = dict(request.POST.items())
    form_data.pop("csrfmiddlewaretoken", None)
    
    credentials = {
        "email": form_data["email"],
        "password": form_data["password"],
    }

    database.connect("mongodb+srv://watermelon:ThisIsWatermelon073@cluster0.vrjatpa.mongodb.net/?retryWrites=true&w=majority")

    # find account matching the credentials
    matches = database.find("userdb", "users", credentials)
    
    # if there are no accounts, credentials are wrong. abort
    if len(matches) == 0:
        print("Email or password is incorrect.")
        print("Login failed.")
        return redirect("/log-in-and-sign-up-page")
    
    # if this point is reached, the credentials are valid.
    user_data = matches[0]
    user_data.pop("_id")
    user_data.pop("password")
    print("Login successful!")

    User.login(user_data)
    
    return redirect("/profile")

@csrf_protect
def reset_password(request):
    email = request.POST["email"]

    # send reset password link to email provided

    return redirect("/log-in-and-sign-up-page")

@csrf_protect
def handle_booking(request):
    # Create an instance of PyCAMod using the path
    root = f"{pathlib.Path(__file__).parent.absolute()}";
    PyCaInstance = PyCaMod.PyCa(tokenPath=f"{root}\\PyCa\\token.json", 
                                credentialPath=f"{root}\\PyCa\\credentials.json")
    
    # Get all events
    events = PyCaInstance.getEvent()

    # Get the data and store it as a dictionary
    form_data = dict(request.POST.items())
    
    print(request.POST.items())

    # Get the date time and change the format to RFC3339
    startDate = form_data['datetime'] + ":00.00Z"
    
    # Split the data and time and add 1 hour to the time
    myDateTime = form_data['datetime'].split("T")
    d,t = myDateTime[0], myDateTime[1].split(':')
    endDate = d + "T"+ str(int(t[0]) + 1) + ":" + t[1] + ":00.00Z"

    # Prepare the data for the event
    data = {
        # CHANGE THIS
        'summary': "WATERMELON",
        # CHANGE THIS
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': str(form_data['notes']),
        'start': { 
            'dateTime': startDate,
            'timeZone': 'Asia/Hong_Kong',
        },
        'end': {
            'dateTime': endDate,
            'timeZone': 'Asia/Hong_Kong',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            # CHANGE THIS
            {'email': "water@example.com"}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    
    d = d.split('-')
    # newEvent = data["summary"] + "|" + str(int(t[0])) + ":" + t[1] + "|" + str(int(t[0]) + 1) + ":" + t[1]
    newEvent = f"{data['summary']}|{d[0]}-{d[1]}-{d[2]}T{str(int(t[0]))}:{t[1]}:00|{d[0]}-{d[1]}-{d[2]}T{str(int(t[0]) + 1)}:{t[1]}:00"
    is_valid = _validate_event(events, newEvent)

    if not is_valid:
        messages.info(request,'Unavailable date, please choose a different one.')
        return redirect('book')

    # Create the Event
    PyCaInstance.createEvent(data)
    
    # Close the Server
    database.closeServer()
    return redirect("/")
    
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

def profile(request):
    if User.is_logged_in:
        context = {
            "full_name": f"{User.first_name} {User.last_name}",
            "email": User.email,
            "phone": User.phone,
            "password_hidden": "*******"
        }
        return render(request, "profile.html", context)
    else:
        return redirect("/log-in-and-sign-up-page")

def book(request):
    if User.is_logged_in:
        return render(request, "forms.html")
    else:
        return redirect("/log-in-and-sign-up-page")

def _validate_event(events, event) -> bool:
    valid = True
    # Extract date and time input
    
    i_startDateTime = event.split('|')[1]

    i_startDate = i_startDateTime.split("T")[0]
    i_startTime = i_startDateTime.split("T")[1]
    i_startHours = i_startTime.split(":")[0]
    i_startMin = i_startTime.split(":")[1]
    i_startSec = i_startTime.split(":")[2][:-1]

    i_startTimeObj = time(int(i_startHours), int(i_startMin), int(i_startSec))

    i_endDateTime = event.split('|')[2]

    i_endDate = i_endDateTime.split("T")[0]
    i_endTime = i_endDateTime.split("T")[1]
    i_endHours = i_endTime.split(":")[0]
    i_endMin = i_endTime.split(":")[1]
    i_endSec = i_endTime.split(":")[2][:-1]

    i_endTimeObj = time(int(i_endHours), int(i_endMin), int(i_endSec))

    for e in events:
        e_startDateTime = e.split('|')[1]

        e_startDate = e_startDateTime.split("T")[0]
        e_startTime = e_startDateTime.split("T")[1]
        e_startHours = e_startTime.split(":")[0]
        e_startMin = e_startTime.split(":")[1]
        e_startSec = e_startTime.split(":")[2][:-1]
        
        e_startTimeObj = time(int(e_startHours), int(e_startMin), int(e_startSec))

        e_endDateTime = e.split('|')[2]

        e_endDate = e_endDateTime.split("T")[0]
        e_endTime = e_endDateTime.split("T")[1]
        e_endHours = e_endTime.split(":")[0]
        e_endMin = e_endTime.split(":")[1]
        e_endSec = e_endTime.split(":")[2][:-1]

        e_endTimeObj = time(int(e_endHours), int(e_endMin), int(e_endSec))

        if e_startDate == i_startDate or e_endDate == i_endDate or\
           e_startDate == i_endDate or e_endDate == i_startDate:
            # Check if input START object is in between an existing start and end time
            if i_startTimeObj >= e_startTimeObj and i_startTimeObj <= e_endTimeObj:
                valid = False
                break

            # Check if input END object is in between an existing start and end time
            if i_endTimeObj >= e_startTimeObj and i_endTimeObj <= e_endTimeObj:
                valid = False
                break
    return valid
    
home = generate_html_view("index.html")
services = generate_html_view("services.html")
about = generate_html_view("about-us.html")
contact = generate_html_view("contact.html")
login_signup = generate_html_view("log-in-and-sign-up-page.html")
forgot_password = generate_html_view("forgot-password.html")
