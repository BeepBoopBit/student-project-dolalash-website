from PyMo import PyMo
from schemas.user import User
import os, traceback
import signal 
from pymongo import MongoClient
from pymongoose.methods import set_schemas, get_cursor_length

def mongo_init():
    """
    Description: Sets up mongoDB and its schemas
    """
    mongo = PyMo('credentials.json')
    print(mongo.mongoClient)

    try:
        schemas = {
            "user": User(empty=True).schema
        }

        set_schemas(mongo.mongoClient.test, schemas)
        print("Connected to MongoDB!")
        return mongo
    except:
        traceback.print_exc()
        print("Error initializing database")
        exit(1)