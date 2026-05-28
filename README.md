```markdown
# 🚀 Enterprise Agentic RAG Platform

## 📖 Overview
An asynchronous, production-grade conversational AI platform built to handle enterprise document retrieval. Utilizes a multi-agent architecture to route queries, query a vector database, and stream real-time responses.

## 🏗️ System Architecture
*(Architecture diagram placeholder: User -> FastAPI -> LangGraph -> Pinecone & LLM)*

## ⚙️ Tech Stack
* **Backend:** Python 3.10+, FastAPI, Uvicorn, WebSockets
* **AI/ML:** LangChain, LangGraph, OpenAI models
* **Data Layer:** Pinecone (Vector DB), Semantic Chunking
* **DevOps:** Docker, GitHub Actions, AWS EC2

## 🚀 Key Features
1. **Agentic Routing:** Dynamically routes queries to the correct specialized tool.
2. **Hybrid Search RAG:** Combines semantic and keyword search for high precision.
3. **Async Streaming:** Uses WebSockets for real-time token streaming.

## 🛠️ Local Setup (Dockerized)
1. Clone the repository.
2. Add your `OPENAI_API_KEY` and `PINECONE_API_KEY` to a local `.env` file.
3. Run `docker-compose up --build` to start the backend services.
