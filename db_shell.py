from pymongo import MongoClient
spams = MongoClient()['spam-db'].spams
