from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.vector_store.pinecone_db import retrieve_context
from app.config import settings

# Define the state for the agent
class AgentState(TypedDict):
    input: str
    context: str
    response: str

llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview", openai_api_key=settings.OPENAI_API_KEY)

def retrieve_node(state: AgentState):
    """Retrieves enterprise context based on user input."""
    context = retrieve_context(state["input"])
    return {"context": context}

def generate_node(state: AgentState):
    """Generates the final response using the LLM and retrieved context."""
    system_prompt = SystemMessage(
        content="You are an enterprise AI assistant. Answer the user's query strictly using the provided context. If the context does not contain the answer, say 'I do not have access to that information in the enterprise database.'"
    )
    user_prompt = HumanMessage(
        content=f"Context: {state.get('context', '')}\n\nQuery: {state['input']}"
    )
    
    response = llm.invoke([system_prompt, user_prompt])
    return {"response": response.content}

# Build the LangGraph State Machine
workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

# Define execution flow
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app_graph = workflow.compile()

def process_query(query: str):
    final_state = app_graph.invoke({"input": query})
    return final_state["response"]
