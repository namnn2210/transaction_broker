import pymongo

from pymongo import MongoClient

def get_database():
    # Replace this string with your MongoDB connection URL
    mongodb_url = "mongodb://localhost:27017/"

    # Connect to MongoDB using the URL
    client = MongoClient(mongodb_url)

    # Get the database
    db = client['transaction_broker']

    return db