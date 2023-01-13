import pymongo as pm

client: pm.MongoClient

def connect(connection_string: str) -> None:
    global client
    client = pm.MongoClient(connection_string)

def insert(database: str, collection: str, data: dict) -> None:
    global client
    db = client[database]
    col = db[collection]
    col.insert_one(data)

def find(database: str, collection: str, query: dict) -> tuple:
    global client
    db = client[database]
    col = db[collection]
    return tuple(col.find(query))
