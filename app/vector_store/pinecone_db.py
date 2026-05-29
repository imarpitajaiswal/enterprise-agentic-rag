import time
import requests
from typing import List

from pinecone import Pinecone
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Pinecone as PineconeVectorStore

from app.config import settings


pc = Pinecone(api_key=settings.PINECONE_API_KEY)


class LightweightHFEmbeddings(Embeddings):

    def __init__(self, model_id: str, hf_token: str):
        self.api_url = (
            f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
        )

        self.headers = {
            "Authorization": f"Bearer {hf_token}"
        }

    def _query(self, payload, retries=4):

        for i in range(retries):

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )

            if response.status_code == 503:
                print(f"⏳ HF model loading... retry {i+1}/{retries}")
                time.sleep(10)
                continue

            if response.status_code != 200:
                raise Exception(
                    f"HuggingFace API Error: {response.status_code} {response.text}"
                )

            return response.json()

        raise Exception("HF embedding API timeout")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._query({"inputs": texts})

    def embed_query(self, text: str) -> List[float]:

        result = self._query({"inputs": text})

        if (
            isinstance(result, list)
            and len(result) > 0
            and isinstance(result[0], list)
        ):
            return result[0]

        return result


embeddings = LightweightHFEmbeddings(
    model_id="sentence-transformers/all-MiniLM-L6-v2",
    hf_token=settings.HF_TOKEN
)


def get_vector_store():

    index = pc.Index(settings.PINECONE_INDEX_NAME)

    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        text_key="text"
    )

    return vector_store


def retrieve_context(query: str, top_k: int = 3):

    try:
        vector_store = get_vector_store()

        docs = vector_store.similarity_search(query, k=top_k)

        if not docs:
            return "No relevant context found."

        return "\n".join(
            [doc.page_content for doc in docs]
        )

    except Exception as e:
        print(f"❌ Pinecone Retrieval Error: {str(e)}")
        return f"Vector retrieval failed: {str(e)}"