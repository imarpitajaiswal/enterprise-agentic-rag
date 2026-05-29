from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

from app.vector_store.pinecone_db import retrieve_context
from app.config import settings


class AgentState(TypedDict):
    input: str
    context: str
    response: str


llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)


def retrieve_node(state: AgentState):

    query = state["input"]

    context = retrieve_context(query)

    return {
        "context": context
    }


def generate_node(state: AgentState):

    prompt = f"""
You are an enterprise-grade AI assistant.

Use ONLY the provided context.

If context is insufficient, say:
"I could not find sufficient information."

Context:
{state['context']}

User Question:
{state['input']}
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("retrieve")

workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

graph = workflow.compile()


def process_query(user_input: str):

    result = graph.invoke({
        "input": user_input,
        "context": "",
        "response": ""
    })

    return result["response"]