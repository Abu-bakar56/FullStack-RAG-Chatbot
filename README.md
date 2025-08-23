# Full-Stack RAG Chatbot (NetSol Internship Project)

🚀 This project was developed during my internship at **NetSol**.  
It is a **full-stack Retrieval-Augmented Generation (RAG) chatbot** that can search company documents and perform **web-based queries**, providing accurate and context-aware responses.

---

## ✨ Features
- **RAG-based Chatbot**
  - Uses **LangChain** & **LangGraph** for document retrieval and reasoning.  
  - Supports **web search** for queries beyond company documents.  
- **Authentication System**
  - User **login & registration** with  **MongoDB**.  
- **Chat Interface**
  - Built with **Streamlit**, providing an interactive UI similar to ChatGPT.  
  - **Streaming responses** with real-time updates.  
  - **Threaded conversations** for chat history.  
  - **Start New Chat** option to reset context and begin fresh conversations.  
- **Database Integration**
  - **MongoDB** stores company documents, user accounts, and chat history.
- **Observability**
  - Integrated **Langfuse** for logging, tracing, and monitoring chatbot performance.   
- **Deployment**
  - Backend (**FastAPI**) and frontend (**Streamlit**) deployed on **Render**.  

---

## 🏗️ Tech Stack
- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **LLM Orchestration:** LangChain, LangGraph  
- **Database:** MongoDB  
- **Deployment:** Render
- **Observability:** Langfuse   
- **Other:** RAG, Web Search APIs  

---

## ⚙️ Architecture
```mermaid
flowchart TD
    A[User] -->|Query| B[Streamlit Chat UI]
    B -->|Send Request| C[FastAPI Backend]
    C -->|Authenticate| D[MongoDB - Users & Chats]
    C -->|RAG Pipeline| E[LangChain + LangGraph]
    E -->|Retrieve Context| F[NetSol Docs + Web Search]
    F -->|Relevant Data| E
    E -->|Response| C --> B --> A
    B -->|Start New Chat| G[Clear Context + New Thread]
    C -->|Logs & Traces| H[Langfuse]
````
---

## 🔗 Live Demo  

👉 [Click here to try the chatbot](https://fullstack-rag-chatbot.onrender.com) 
---

## 🚀 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/netsol-rag-chatbot.git
   cd netsol-rag-chatbot
   ```

2. **Create and activate environment**

   ```bash
   conda create -n ragchat python=3.9
   conda activate ragchat
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (e.g., `.env`)

   ```
   MONGO_URI=your_mongo_connection
   LANGCHAIN_API_KEY=your_key
   TAVILY_API_KEY=your_key  # for web search
   LANGFUSE_SECRET_KEY=your_key   # for Langfuse observability
   LANGFUSE_PUBLIC_KEY=your_key
   ```

5. **Run the backend (FastAPI)**

   ```bash
   uvicorn main:app --reload
   ```

6. **Run the frontend (Streamlit)**

   ```bash
   streamlit run app.py
   ```

7. **Access the app**

   * Backend: `http://127.0.0.1:8000`
   * Frontend: `http://localhost:8501`

---

## 📦 Deployment

* Deployed on **Render** (backend + frontend).
* CI/CD enabled with **GitHub integration**.
* **Langfuse observability** is enabled in production.

---

## 📸 Screenshots



https://github.com/user-attachments/assets/943050d3-d81f-487a-80a8-0ffe2c3fffa5



---
![WhatsApp Image 2025-08-23 at 19 42 13_526979ab](https://github.com/user-attachments/assets/5b896ae8-76f6-4350-8f4a-44782dd4166b)


---

## 📚 Learning Outcomes

During my internship at **NetSol**, I:

* Learned **full-stack development with FastAPI, Streamlit, and MongoDB**.
* Implemented **RAG pipelines** using LangChain and LangGraph.
* Designed a **real-time chatbot interface** with streaming responses and threaded history.
* Built a **“Start New Chat”** option for improved UX.
* Integrated **Langfuse** for logging, tracing, and monitoring chatbot performance.
* Gained experience in **deploying production-ready apps on Render**.



