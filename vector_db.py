import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct

class QdrantStorage:

    def __init__(self, url: str | None = None, collection: str = "docs", dim: int = 3072):
        url = url or os.getenv("QDRANT_URL", "http://localhost:6333")

        api_key = os.getenv("QDRANT_API_KEY")

        self.client = QdrantClient(url=url, api_key=api_key, timeout=30)
        self.collection = collection

        try:
               self.client.get_collections()
        except Exception as e:
            raise RuntimeError(
                f"Qdrant not reachable at {url}. Start Docker Qdrant or set QDRANT_URL."
            ) from e


        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def upsert(self, ids, vectors, payloads):

        points = [
            PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, query_vector, top_k: int = 5):
        res = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            with_payload=True,
            limit=top_k)

        contexts = []
        sources = set()

        for p in res.points:
            payload = p.payload or {}
            text = payload.get("text")
            source = payload.get("source")
            if text:
                contexts.append(text)
            if source:
                sources.add(source)

        return {"contexts": contexts, "sources": list(sources)}

