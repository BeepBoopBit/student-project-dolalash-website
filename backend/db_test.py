import django
import json
from mongoHandler import MongoHandler
from schemas.user import User
from schemas.schedule import Schedule
import traceback

print(django.get_version())

creds_path = 'credentials.json'
f = open(creds_path)
creds = json.load(f)

mongoHandler = MongoHandler(creds, "DoLaLash")

users = mongoHandler.insert_user({
        "username" : "beepBoopBit",
        "password" : "watermelon",
        "f_name" : "Beep",
        "l_name" : "Boop",
        "email" : "beepBoopBit+DoLaLash@gmail.com",
        "mobile" : "07373737373"
    })

print(mongoHandler.delete_user("63c0406ffaec984550c1dec6"))