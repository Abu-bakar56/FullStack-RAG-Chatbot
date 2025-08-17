import os

# # Environment variables
os.environ["TAVILY_API_KEY"] = "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"

os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-8a7c9180-32aa-47c7-af35-23ddeb070851"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-d812c460-f6cc-44d4-9dae-90042eaa7c46"
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"



# # Load environment variables
# TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY")
# LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY")
# LANGFUSE_HOST = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
# MONGO_URI = os.environ.get("MONGO_URI")

# MongoDB configuration
MONGO_URI = "mongodb+srv://abubakarshahzad730:pI9luB1GcElMXeGV@interncluster.telwaoi.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "rag_database"
VECTOR_COLLECTION_NAME = "vector_store"
USER_COLLECTION_NAME = "users"
CHAT_COLLECTION_NAME = "chat_history"

