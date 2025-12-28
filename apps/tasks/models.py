from pymongo import MongoClient

# MongoDB connection (Option A)
client = MongoClient("mongodb://localhost:27017/")
db = client["task_manager_db"]
tasks_collection = db["tasks"]
