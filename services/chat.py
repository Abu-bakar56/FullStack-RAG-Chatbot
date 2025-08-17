import uuid
from datetime import datetime
from typing import List, Dict
from core.database import chat_collection, user_collection

def create_thread(user_id: str) -> str:
    thread_id = str(uuid.uuid4())
    thread_data = {
        "thread_id": thread_id,
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "messages": []
    }
    try:
        chat_collection.insert_one(thread_data)
        print(f"Thread {thread_id} created for user {user_id}")
        return thread_id
    except Exception as e:
        print(f"Thread creation failed: {e}")
        return None

def save_chat_message(thread_id: str, user_id: str, message: Dict):
    try:
        chat_collection.update_one(
            {"thread_id": thread_id, "user_id": user_id},
            {"$push": {"messages": {
                "content": message['content'],
                "role": message['role'],
                "timestamp": datetime.utcnow()
            }}}
        )
        print(f"Message saved to thread {thread_id}")
    except Exception as e:
        print(f"Failed to save message: {e}")

def get_chat_history(thread_id: str, user_id: str) -> List[Dict]:
    try:
        thread = chat_collection.find_one({"thread_id": thread_id, "user_id": user_id})
        return thread.get("messages", []) if thread else []
    except Exception as e:
        print(f"Failed to retrieve chat history: {e}")
        return []

def get_user_threads(user_id: str) -> List[str]:
    try:
        threads = chat_collection.find({"user_id": user_id}, {"thread_id": 1})
        return [thread["thread_id"] for thread in threads]
    except Exception as e:
        print(f"Failed to retrieve threads: {e}")
        return []

def get_username(user_id: str) -> str:
    try:
        user = user_collection.find_one({"user_id": user_id})
        return user["username"] if user else "Unknown"
    except Exception as e:
        print(f"Failed to retrieve username: {e}")
        return "Unknown"