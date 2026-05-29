def retrieve_node(state: AgentState):
    try:
        context = retrieve_context(state["input"])
    except Exception as e:
        print(f"❌ CRITICAL RETRIEVAL ERROR: {str(e)}")
        context = f"Error connecting to database: {str(e)}"
    return {"context": context}