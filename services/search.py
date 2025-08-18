from sentence_transformers import SentenceTransformer
from langchain_tavily import TavilySearch
from core.database import vector_collection
from core.models import AgentState
import os
from core.config import TAVILY_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
tavily_tool = TavilySearch(max_results=5)

def generate_embedding(text: str) -> list[float]:
    return embedding_model.encode([text])[0].tolist()

def vector_search(user_query: str, top_k: int = 150) -> list[dict]:
    query_embedding = generate_embedding(user_query)
    if query_embedding is None:
        return []
    pipeline = [{
        "$vectorSearch": {
            "index": "vector_index",
            "queryVector": query_embedding,
            "path": "embedding",
            "numCandidates": top_k,
            "limit": 5,
        }
    }]
    try:
        return list(vector_collection.aggregate(pipeline))
    except Exception as e:
        print(f"Vector search failed: {e}")
        return []

async def process_query(state: AgentState) -> AgentState:
    # Import here to avoid circular import at module level
    from core.agent import graph
    return graph.invoke(state)
