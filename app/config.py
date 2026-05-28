import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Enterprise Agentic RAG"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "enterprise-rag-index")

settings = Settings()