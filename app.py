from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Dict
from core.fuse_client import langfuse_client
from services.auth import register_user, login_user
from services.chat import save_chat_message, get_chat_history, get_user_threads
from core.models import AgentState
import uuid
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Full Stack Chatbot on Netsol Document & Web Search")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # For local Streamlit testing
        "https://Full-Stack-RAG-Chatbot.onrender.com",  # Update with deployed frontend URL
    
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    query: str
    thread_id: str | None = None

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return token  # In a real app, validate token and return user_id


@app.get("/")
async def read_root():
    return {"message": "Your Fullstack RAG Chatbot is running 🚀"}

@app.post("/register")
async def register(user: UserRegister):
    trace = langfuse_client.create_trace(name="user_registration")
    user_id = register_user(user.username, user.email, user.password)
    if not user_id:
        trace.update(status="ERROR")
        raise HTTPException(status_code=400, detail="Registration failed")
    trace.update(status="SUCCESS")
    return {"user_id": user_id}

@app.post("/login")
async def login(user: UserLogin):
    trace = langfuse_client.create_trace(name="user_login")
    user_id = login_user(user.email, user.password)
    if not user_id:
        trace.update(status="ERROR")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    trace.update(status="SUCCESS")
    return {"user_id": user_id}

@app.post("/chat")
async def chat(request: ChatRequest, user_id: str = Depends(get_current_user)):
    trace = langfuse_client.create_trace(name="chat_interaction")
    trace.update(inputs={"query": request.query, "user_id": user_id})
    
    from services.chat import create_thread
    thread_id = request.thread_id or create_thread(user_id)
    if not thread_id:
        trace.update(status="ERROR")
        raise HTTPException(status_code=500, detail="Failed to create thread")
    
    initial_state = AgentState(
        messages=[{"role": "user", "content": request.query}],
        retrieved_docs=[],
        web_results="",
        final_answer="",
        needs_web_search=False,
        user_id=user_id,
        thread_id=thread_id
    )
    
    try:
        from services.search import process_query
        result = await process_query(initial_state)
        trace.update(outputs={"response": result["final_answer"]}, status="SUCCESS")
        return {"thread_id": thread_id, "response": result["final_answer"]}
    except Exception as e:
        trace.update(status="ERROR", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/threads")
async def get_threads(user_id: str = Depends(get_current_user)):
    trace = langfuse_client.create_trace(name="get_threads")
    threads = get_user_threads(user_id)
    trace.update(outputs={"threads": threads}, status="SUCCESS")
    return {"threads": threads}

@app.get("/thread/{thread_id}")
async def get_thread(thread_id: str, user_id: str = Depends(get_current_user)):
    trace = langfuse_client.create_trace(name="get_thread_history")
    history = get_chat_history(thread_id, user_id)
    trace.update(outputs={"history": history}, status="SUCCESS")
    return {"history": history}