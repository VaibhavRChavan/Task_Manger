from pymongo import MongoClient
from django.conf import settings

_client = None

def get_mongo_client():
    """Get MongoDB client (singleton pattern)"""
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGODB_URI)
    return _client

def get_database():
    """Get the task_manager database"""
    client = get_mongo_client()
    return client[settings.MONGO_DB_NAME]

def get_tasks_collection():
    """Get tasks collection"""
    db = get_database()
    return db['tasks']