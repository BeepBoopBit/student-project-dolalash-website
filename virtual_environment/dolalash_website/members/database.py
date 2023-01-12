import pymongo as pm

client: pm.MongoClient

def connect(username: str, password: str) -> None:
    global client
    client = pm.MongoClient(f"mongodb+srv://{username}:{password}@dolalash.onucqiy.mongodb.net/?retryWrites=true&w=majority")

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
