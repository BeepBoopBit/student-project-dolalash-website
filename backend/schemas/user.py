import datetime
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema, MongoException, MongoError
from bson import json_util
from bson.objectid import ObjectId

users = None

def user_model_init (db):
   global users
   users = db["users"]

class User(Schema):
    """
    Sets up the User Schema
    """
    
    schema_name = "user"

    id = None
    username = None
    password = None
    f_name = None
    l_name = None
    email = None
    mobile = None
    
    def __init__(self, **kwargs):
        req_string = {
                "type": Types.String,
                "required": True
            }

        self.schema = {
            "username": req_string,
            "password": req_string,
            "f_name": req_string,
            "l_name": req_string,
            "email": req_string,
            "mobile": req_string,
        }

        super().__init__(self.schema_name, self.schema, kwargs)

    def __str__(self):
        return f"User: {self.username}, First Name: {self.f_name}, Last Name: {self.l_name}, Email: {self.email}, Mobile: {self.mobile}"