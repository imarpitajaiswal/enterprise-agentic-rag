from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.agent.graph import process_query
import logging

app = FastAPI(title="Enterprise Agentic RAG Platform")
logging.basicConfig(level=logging.INFO)

@app.get("/")
async def health_check():
    return {"status": "production", "service": "Agentic RAG"}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive text from the client
            data = await websocket.receive_text()
            logging.info(f"Received query: {data}")
            
            # Process query through LangGraph
            response = process_query(data)
            
            # Send response back to client
            await websocket.send_text(response)
    except WebSocketDisconnect:
        logging.info("Client disconnected")
