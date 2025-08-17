from typing import Dict, List, TypedDict, Annotated, Sequence
from langchain_core.messages import HumanMessage, AIMessage

class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage], "Messages in conversation"]
    retrieved_docs: List[Dict]
    web_results: str
    final_answer: str
    needs_web_search: bool
    user_id: str
    thread_id: str