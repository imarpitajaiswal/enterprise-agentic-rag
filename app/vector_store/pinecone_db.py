import requests
from typing import List
from langchain_core.embeddings import Embeddings
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient
from app.config import settings

pc = PineconeClient(api_key=settings.PINECONE_API_KEY)

class LightweightHFEmbeddings(Embeddings):
    def __init__(self, model_id: str, hf_token: str):
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
        self.headers = {"Authorization": f"Bearer {hf_token}"}

    def _query(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._query({"inputs": texts})

    def embed_query(self, text: str) -> List[float]:
        return self._query({"inputs": text})

# ☁️ Cloud API Embeddings (Zero heavy dependencies!)
embeddings = LightweightHFEmbeddings(
    model_id="sentence-transformers/all-MiniLM-L6-v2",
    hf_token=settings.HF_TOKEN
)

def get_vector_store():
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    vector_store = Pinecone(index, embeddings.embed_query, "text")
    return vector_store

def retrieve_context(query: str, top_k: int = 3):
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(query, k=top_k)
    return "\n".join([doc.page_content for doc in docs])