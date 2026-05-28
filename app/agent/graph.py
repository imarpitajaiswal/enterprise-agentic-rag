from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from app.vector_store.pinecone_db import retrieve_context
from app.config import settings

class AgentState(TypedDict):
    input: str
    context: str
    response: str

llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.1-8b-instant",
    groq_api_key=settings.GROQ_API_KEY
)

def retrieve_node(state: AgentState):
    try:
        context = retrieve_context(state["input"])
    except Exception as e:
        print(f"❌ RETRIEVAL ERROR: {e}") # <-- Add this line!
        context = "Database not initialized yet."
    return {"context": context}

def generate_node(state: AgentState):
    system_prompt = SystemMessage(
        content="You are an enterprise AI assistant. Answer using the context provided."
    )
    user_prompt = HumanMessage(
        content=f"Context: {state.get('context', '')}\n\nQuery: {state['input']}"
    )
    response = llm.invoke([system_prompt, user_prompt])
    return {"response": response.content}

workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app_graph = workflow.compile()

def process_query(query: str):
    final_state = app_graph.invoke({"input": query})
    return final_state["response"]