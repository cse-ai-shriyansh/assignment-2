from embedder import embed_query

def retrieve_relevant_chunks(question, chunks, vector_store, top_k=5):
    query_embedding = embed_query(question)

    results = vector_store.search(query_embedding, top_k=top_k)

    print("DEBUG RESULTS:", results)

    enriched = []
    for idx, score in results:
        enriched.append({
            "text": chunks[idx]["text"],
            "page": chunks[idx]["page"],
            "score": score
        })

    return enriched


if __name__ == "__main__":
    from pdf_ingest import extract_pdf_text
    from chunker import chunk_text
    from embedder import embed_chunks
    from vector_store import VectorStore

    print("\n--- LOADING PDF ---")
    pages = extract_pdf_text("../data/pdfs/DigitalElectronicsThoery.pdf")

    print("--- CHUNKING ---")
    chunks = chunk_text(pages)

    print("--- EMBEDDING ---")
    embedded = embed_chunks(chunks)

    print("--- BUILDING VECTOR STORE ---")
    store = VectorStore(dimension=len(embedded[0]["embedding"]))
    store.add(embedded)

    query = "What is Boolean logic?"

    print("\n--- RETRIEVED CHUNKS ---")
    results = retrieve_relevant_chunks(query, chunks, store)

    for r in results:
        print(f"\n[Page {r['page']}] (score={r['score']:.4f})")
        print(r["text"][:300])
