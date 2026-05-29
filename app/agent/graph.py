from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.vector_store.pinecone_db import retrieve_context
from app.config import settings
# Assuming you are using Groq/OpenAI or another LLM in your graph
# from langchain_groq import ChatGroq 

# 1. Define the Agent State
class AgentState(TypedDict):
    input: str
    context: str
    response: str

# 2. Define the Retrieval Node (Fixed with robust logging)
def retrieve_node(state: AgentState):
    try:
        context = retrieve_context(state["input"])
    except Exception as e:
        print(f"❌ CRITICAL RETRIEVAL ERROR: {str(e)}")
        context = f"SYSTEM ERROR: Failed to retrieve data from vector database. Reason: {str(e)}"
    return {"context": context}

# 3. Define the Generation Node
def generate_node(state: AgentState):
    # Your existing LLM generation logic here
    # Example placeholder structure:
    # llm = ChatGroq(temperature=0, groq_api_key=settings.GROQ_API_KEY)
    # response = llm.invoke(f"Context: {state['context']}\nQuestion: {state['input']}")
    # return {"response": response.content}
    return {"response": f"Processed input using context: {state['context'][:50]}..."}

# 4. Build the LangGraph Workflow
workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()