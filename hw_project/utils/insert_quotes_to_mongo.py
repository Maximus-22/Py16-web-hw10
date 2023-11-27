import json
from bson.objectid import ObjectId

from pymongo import MongoClient


# client = MongoClient("mongodb+srv://maximusm_22:<password>@cluster0.aemcehc.mongodb.net/")
client = MongoClient("mongodb://localhost")

db = client["BD-homework"]

with open("quotes.json", "r", encoding = "UTF-8") as fd:
    quotes = json.load(fd)

for quote in quotes:
    author = db.authors.find_one({"fulname": quote["author"]})
    if author:
        db.quotes.insert_one({
        "quote": quote["quote"],
        "tags": quote["tags"],
        "author": ObjectId(author["_id"])
        })