from pymongo import MongoClient

from .config import DATABASE


def connect_db(name):
    try:
        client = MongoClient(DATABASE[name]['uri'])
        db = client[DATABASE[name]['name']]
        print("Database connected: {}".format(name))
    except Exception as e:
        print("Database connection error: {}".format(name))
        print(str(e))
    return db
