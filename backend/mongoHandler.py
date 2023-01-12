from PyMo import PyMo
from schemas.user import User
from schemas.schedule import Schedule
import os, traceback
import signal 
from pymongo import MongoClient
from pymongoose.methods import set_schemas, get_cursor_length, AS_DICT, AS_STRING

class MongoHandler:
    def __init__(self, credentials, database_name):
        self.database_name = database_name
        self.credentials = credentials
        pass

    def mongo_init(self):
        """
        Description: Sets up mongoDB and its schemas
        """
        mongo = PyMo(self.credentials)
        
        try:
            schemas = {
                "users": User(empty=True).schema,
                "schedules": Schedule(empty=True).schema
            }

            set_schemas(mongo.mongoClient[self.database_name], schemas, _debug_log_=False)
        except:
            traceback.print_exc()
            print("Error initializing database")
            exit(1)

    def insert_user(self, schema):
        """
        `user: dict` - dict of User Schema
        """

        self.mongo_init()
        # Sample Inserting
        try:
            user = User(
                username=schema["username"],
                password=schema["password"],
                f_name=schema["f_name"],
                l_name=schema["l_name"],
                email=schema["email"],
                mobile=schema["mobile"]
            )
            user_id = user.save()
            return user_id
        except:
            traceback.print_exc()
            raise Exception("User insertion failed")

    def find_user(self, query):
        """
        `user: dict` - dict of User Schema - pass empty dict if you want to get all users

        """
        self.mongo_init()

        try:
            users = User.find(query, cursor=AS_DICT)
            return users
        except:
            traceback.print_exc()
            raise Exception("Error initializing database")

    def delete_user(self, id):
        """
        `id: string` - id of User to be deleted
        """
        self.mongo_init()
        try:
            count = User.delete({"_id": id})

            if count == 0:
                raise Exception("No data was deleted")
                return 1
            print("Delete one exit with code 0")
            return 0
        except:
            raise Exception("Error deleting one")
            return 1