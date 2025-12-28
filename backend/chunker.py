import re

MAX_CHARS = 500


def chunk_text(pages):
    chunks = []

    for page in pages:
        text = page["text"]
        sentences = re.split(r'(?<=[.!?])\s+', text)

        buffer = ""

        for sentence in sentences:
            if len(buffer) + len(sentence) <= MAX_CHARS:
                buffer += sentence + " "
            else:
                chunks.append({
                    "page": page["page"],
                    "text": buffer.strip()
                })
                buffer = sentence + " "

        if buffer:
            chunks.append({
                "page": page["page"],
                "text": buffer.strip()
            })

    return chunks
