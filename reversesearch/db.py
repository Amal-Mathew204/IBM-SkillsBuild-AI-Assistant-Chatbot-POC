from pymongo import MongoClient
from config import CONFIG
import os
def get_mongo_client():
    url: str = f"mongodb://{os.getenv('MONGO_CONTAINER')}:{os.getenv('MONGO_PORT')}"
    return MongoClient(url,
                       username = os.getenv('MONGO_USER'),
                       password = os.getenv('MONGO_PASSWORD'),
                       authMechanism = os.getenv('MONGO_AUTH_MECHANISM')
                       )

def fetch_documents(collection_name, limit=10):
    client = get_mongo_client()
    db = client[os.getenv('MONGO_CHATBOT_DATABASE')]
    collection = db[collection_name]
    return list(collection.find().limit(limit))
