from sentence_transformers import SentenceTransformer

# Load model ONCE
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(
        texts,
        batch_size=16,
        show_progress_bar=True
    )

    embedded = []
    for chunk, emb in zip(chunks, embeddings):
        embedded.append({
            "text": chunk["text"],
            "page": chunk["page"],
            "embedding": emb.tolist()
        })

    print("DEBUG embed_chunks returned:", len(embedded))
    return embedded


def embed_query(question: str):
    embedding = model.encode(question)
    return embedding.tolist()
