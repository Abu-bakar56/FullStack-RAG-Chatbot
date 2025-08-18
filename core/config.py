import os

# # Load environment variables
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY")
LANGFUSE_HOST = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
MONGO_URI = os.environ.get("MONGO_URI")

# MongoDB configuration
DB_NAME = "rag_database"
VECTOR_COLLECTION_NAME = "vector_store"
USER_COLLECTION_NAME = "users"
CHAT_COLLECTION_NAME = "chat_history"

