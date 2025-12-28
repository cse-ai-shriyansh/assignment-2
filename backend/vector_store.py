import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add(self, embeddings):
        vectors = np.array(
            [e["embedding"] for e in embeddings],
            dtype="float32"
        )

        self.index.add(vectors)
        self.metadata.extend(embeddings)

        print("FAISS TOTAL VECTORS:", self.index.ntotal)

    def search(self, query_vector, top_k=5):
        query_vector = np.array([query_vector], dtype="float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue
            results.append((int(idx), float(dist)))

        return results
