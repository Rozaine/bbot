import pymongo
from bson import ObjectId
from pymongo import errors

try:
    db_client = pymongo.MongoClient("mongodb://localhost:27017/")
    current_db = db_client["work"]
    collection = current_db["work01"]
except errors.ServerSelectionTimeoutError:
    print("database is down")


def searchBooks(name: str):
    search_result = collection.find({"$text": {"$search": name}}, {'score': {'$meta': 'textScore'}})
    res = list(search_result.sort([('score', {'$meta': 'textScore'})]))
    return res


def getCountBooks():
    return collection.find()


def getBookPathById(book_id: str):
    my_query = {'_id': ObjectId(book_id)}
    book_path = collection.find(my_query)
    return book_path
