from pymongo import MongoClient
from pymongo.server_api import ServerApi

def get_mongodb():
    uri = "mongodb+srv://maximusm_22:<password>@cluster0.aemcehc.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi("1"))
    db = client["BD-homework"]
    return db