import pymongo
from core.config import MONGO_URI, DB_NAME, VECTOR_COLLECTION_NAME, USER_COLLECTION_NAME, CHAT_COLLECTION_NAME

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
db = mongo_client[DB_NAME]
vector_collection = db[VECTOR_COLLECTION_NAME]
user_collection = db[USER_COLLECTION_NAME]
chat_collection = db[CHAT_COLLECTION_NAME]