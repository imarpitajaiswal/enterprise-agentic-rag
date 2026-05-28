import asyncio
import websockets

async def chat():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        print("🟢 Connected! Type a message. Type 'exit' to quit.")
        while True:
            query = input("\nYou: ")
            if query.lower() == 'exit': break
            await websocket.send(query)
            response = await websocket.recv()
            print(f"🤖 AI: {response}")

if __name__ == "__main__":
    asyncio.run(chat())