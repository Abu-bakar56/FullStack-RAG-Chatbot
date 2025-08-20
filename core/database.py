import pymongo
from core.config import MONGO_URI

def get_mongo_client(mongo_uri: str) -> pymongo.MongoClient:
    client = pymongo.MongoClient(mongo_uri, appname="devrel.showcase.rag.python")
    try:
        if client.admin.command("ping").get("ok") == 1.0:
            print("Connected to MongoDB")
            return client
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
    return None

mongo_client = get_mongo_client(MONGO_URI)
db = mongo_client["rag_database"]
vector_collection = db["vector_store"]
user_collection = db["users"]
chat_collection = db["chat_history"]