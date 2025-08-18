from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from core.models import AgentState
from services.search import vector_search , tavily_tool
from services.chat import get_chat_history, get_username
from langchain_core.messages import HumanMessage, AIMessage
from langfuse.langchain import CallbackHandler  
from core.config import GROQ_API_KEY
langfuse_handler = CallbackHandler()

llm = ChatGroq(model="llama3-8b-8192", api_key=GROQ_API_KEY)


def tool_node(state: AgentState) -> AgentState:
    user_query = state["messages"][-1].content
    docs = vector_search(user_query)
    serializable_docs = [
        {
            "chunk": doc.get("chunk", ""),
            "metadata": dict(doc.get("metadata", {}))
        }
        for doc in docs
    ]
    state["retrieved_docs"] = serializable_docs
    state["web_results"] = ""
    return state

def chatbot_node(state: AgentState) -> AgentState:
    user_query = state["messages"][-1].content
    retrieved_docs = state["retrieved_docs"]
    user_id = state["user_id"]
    thread_id = state["thread_id"]

    chat_history = get_chat_history(thread_id, user_id)
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history]) if chat_history else ""
    context = "\n".join([doc.get("chunk", "") for doc in retrieved_docs]) if retrieved_docs else "No documents found."
    is_greeting = user_query.lower().strip() in ["hi", "hello"]

    prompt = f"""
You are a friendly AI assistant. 
- If the latest user query is a greeting (e.g., 'hi' or 'hello'), respond with a concise 'Hello [username]!' using the user's username, and end.
- For all other queries, evaluate independently and provide a fresh response, using retrieved context as the primary source if relevant, and conversation history only as supplementary information for follow-ups.

Latest User Query:
{user_query}

Retrieved Context:
{context}

Conversation History (optional context):
{history_text}

Steps:
1. If the latest query is a greeting, respond with 'Hello [username]!' where [username] is {get_username(user_id)}, and end.
2. Otherwise, assess if the retrieved context is relevant and sufficient.
3. If YES, use it to answer and end with: [USE_DOCS]
4. If NO or if the query involves real-time information (e.g., news, weather), suggest a web search with: [USE_WEB]
5. For follow-ups, leverage conversation history to maintain context.

Final response:
"""

    response = llm.invoke(prompt, config={"callbacks": [langfuse_handler]})
    content = response.content.strip()
    state["messages"].append(AIMessage(content=content))
    state["final_answer"] = content
    state["needs_web_search"] = "[USE_WEB]" in content
    return state

def web_search_node(state: AgentState) -> AgentState:
    user_query = next((msg.content for msg in reversed(state["messages"]) if isinstance(msg, HumanMessage)), "")
    user_id = state["user_id"]
    thread_id = state["thread_id"]

    chat_history = get_chat_history(thread_id, user_id)
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history]) if chat_history else ""
    web_results = tavily_tool.invoke(user_query, config={"callbacks": [langfuse_handler]})
    state["web_results"] = web_results

    prompt = f"""
You are a helpful assistant. Evaluate the user query independently and provide a fresh response. Use the web results as the primary source, and consider conversation history only as supplementary information for follow-ups.

User Query:
{user_query}

Web Search Results:
{web_results}

Conversation History (optional context):
{history_text}

Answer the question clearly and concisely based on the web results, using history only if relevant.
"""
    response = llm.invoke(prompt)
    content = response.content.strip()
    state["messages"].append(AIMessage(content=content))
    state["final_answer"] = content
    return state

def decide_node(state: AgentState) -> str:
    return "web_search" if state.get("needs_web_search", False) else "end"

workflow = StateGraph(AgentState)
workflow.add_node("tool", tool_node)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("end", lambda x: x)
workflow.add_edge("tool", "chatbot")
workflow.add_conditional_edges("chatbot", decide_node, {
    "web_search": "web_search",
    "end": END
})
workflow.add_edge("web_search", "end")
workflow.set_entry_point("tool")
graph = workflow.compile()

async def process_query(state: AgentState) -> AgentState:
    try:
        result = graph.invoke(state)
        return result
    except Exception as e:
        raise
