import requests
import chromadb
from typing import List, Optional

class EmbeddingClient:
    def __init__(self, api_url: str, api_key: str, model: str):
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_embedding(self, text: str) -> List[float]:
        try:
            data = {
                "model": self.model,
                "input": text
            }
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            raise Exception(f"获取嵌入向量失败: {str(e)}")

    def batch_get_embeddings(self, texts: List[str]) -> List[List[float]]:
        return [self.get_embedding(text) for text in texts]


class ChromaVectorStore:
    def __init__(self, client: Optional[chromadb.Client] = None):
        self.client = client or chromadb.Client()
        self.collections = {}

    def create_collection(self, collection_name: str) -> chromadb.Collection:
        self.collections[collection_name] = self.client.create_collection(name=collection_name)
        return self.collections[collection_name]

    def get_collection(self, collection_name: str) -> chromadb.Collection:
        if collection_name not in self.collections:
            self.collections[collection_name] = self.client.get_collection(name=collection_name)
        return self.collections[collection_name]

    def add_documents(
        self, 
        collection_name: str, 
        documents: List[str], 
        embeddings: List[List[float]], 
        ids: List[str]
    ):
        collection = self.get_collection(collection_name)
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings
        )