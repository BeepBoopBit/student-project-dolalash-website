import django
import json
from mongoHandler import MongoHandler
from schemas.user import User
from schemas.schedule import Schedule
import traceback

creds_path = 'credentials.json'
f = open(creds_path)
creds = json.load(f)

mongoHandler = MongoHandler(creds, "DoLaLash")

# user_id = mongoHandler.insert_user({
#         "username" : "beepBoopBit",
#         "password" : "watermelon",
#         "f_name" : "Beep",
#         "l_name" : "Boop",
#         "email" : "beepBoopBit+DoLaLash@gmail.com",
#         "mobile" : "07373737373"
#     })

# print(mongoHandler.find_user({ "username": "beepBoopBit"}))

# mongoHandler.delete_user(user_id)

# print(mongoHandler.find_user({ "id": user_id}))