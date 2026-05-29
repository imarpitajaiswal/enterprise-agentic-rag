import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "Enterprise Agentic RAG"

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

    HF_TOKEN = os.getenv("HF_TOKEN")

settings = Settings()