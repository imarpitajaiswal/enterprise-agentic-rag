from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

import logging

from app.agent.graph import process_query


logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Enterprise Agentic RAG Platform"
)


@app.get("/")
async def health_check():

    return {
        "status": "healthy",
        "service": "Enterprise Agentic RAG"
    }


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    logging.info("✅ WebSocket connected")

    try:

        while True:

            data = await websocket.receive_text()

            logging.info(f"📩 User Query: {data}")

            response = process_query(data)

            await websocket.send_text(response)

    except WebSocketDisconnect:

        logging.info("❌ Client disconnected")

    except Exception as e:

        logging.error(f"🔥 WebSocket Error: {str(e)}")

        await websocket.send_text(
            f"Internal server error: {str(e)}"
        )