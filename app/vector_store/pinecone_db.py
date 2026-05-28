from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient
from app.config import settings

pc = PineconeClient(api_key=settings.PINECONE_API_KEY)

embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    task="feature-extraction",
    huggingfacehub_api_token=settings.HF_TOKEN
)

def get_vector_store():
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    vector_store = Pinecone(index, embeddings.embed_query, "text")
    return vector_store

def retrieve_context(query: str, top_k: int = 3):
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(query, k=top_k)
    return "\n".join([doc.page_content for doc in docs])