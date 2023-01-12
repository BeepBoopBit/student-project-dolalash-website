import datetime
from pymongoose import methods
from pymongoose.mongo_types import Types, Schema, MongoException, MongoError
from bson import json_util
from bson.objectid import ObjectId

schedules = None

def user_model_init (db):
   global schedules
   schedules = db["schedules"]

class Schedule(Schema):
    """
    Sets up the Schedule Schema
    """

    schema_name = "schedules"
    
    id = None
    title = None
    user = None
    start_date = None
    end_date = None
    type_of_service = None
    user_note = None
    
    def __init__(self, **kwargs):
        req_string = {
                "type": Types.String,
                "required": True
            }

        self.schema = {
            "title": req_string,
            "user": {
                "type": Types.ObjectId,
                "refs": "user"
            },
            "start_date": req_string,
            "end_date": req_string,
            "type_of_service": req_string,
            "user_note": req_string,
        }

        super().__init__(self.schema_name, self.schema, kwargs)

    def __str__(self):
        return f"User: {self.name}, Actions: {self.action}"