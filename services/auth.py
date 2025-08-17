import bcrypt
import uuid
from datetime import datetime
from core.database import user_collection

def register_user(username: str, email: str, password: str) -> str:
    user_id = str(uuid.uuid4())
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
    try:
        
        if user_collection.find_one({"$or": [{"email": email}, {"username": username}]}):
            print(f"User registration failed: Email or username already exists")
            return None
        user_collection.insert_one(user_data)
        print(f"User {username} registered with ID: {user_id}")
        return user_id
    except Exception as e:
        print(f"User registration failed: {e}")
        return None

def login_user(email: str, password: str) -> str:
    try:
        user = user_collection.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            print(f"User {user['username']} logged in with ID: {user['user_id']}")
            return user["user_id"]
        else:
            print("Login failed: Invalid email or password")
            return None
    except Exception as e:
        print(f"Login failed: {e}")
        return None