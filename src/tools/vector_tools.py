from typing import Any, Iterable
import chromadb
import re

EMBED_MODEL = "text-embedding-3-small"
# Keep these modest for Lesson 4; you can switch to token-based later.
CHUNK_MAX_CHARS = 1000
CHUNK_OVERLAP_CHARS = 100

def get_collection(name: str):
    client = chromadb.HttpClient(host="localhost", port=8000)
    return client.get_or_create_collection(name=name)


def chunk_text(text: str, max_chars: int = CHUNK_MAX_CHARS, overlap: int = CHUNK_OVERLAP_CHARS) -> list[str]:
    # Split on headings / bullet sections
    sections = re.split(r"\n(?=[A-Z][A-Za-z ]{3,}:)", text)
    chunks = []

    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        # Cap size defensively
        if len(sec) > 1200:
            chunks.extend([sec[i:i+800] for i in range(0, len(sec), 800)])
        else:
            chunks.append(sec)

    return chunks

def embed_batch(client, texts: list[str]) -> list[list[float]]:
    """
    Batch embedding call: one request for many inputs.
    Preserves order: embeddings[i] corresponds to texts[i].
    """
    if not texts:
        return []

    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts,
    )
    return [item.embedding for item in resp.data]

def batched(iterable: list[Any], batch_size: int) -> Iterable[list[Any]]:
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]