def sanitize_sources(chunks):
    seen = set()
    clean = []
    
    for c in chunks:
        key = (c["page"], c["text"])
        if key not in seen:
            seen.add(key)
            clean.append({
                "page": int(c["page"]),
                "text": str(c["text"])
        })
   
    return clean[:3]  # limit sources
def sanitize_sources(chunks):
    clean = []
    for c in chunks:
        clean.append({
            "page": c["page"],
            "text": c["text"][:300]
        })
    return clean
