from typing import Any, Iterable
import chromadb

EMBED_MODEL = "text-embedding-3-small"
# Keep these modest for Lesson 4; you can switch to token-based later.
CHUNK_MAX_CHARS = 2000
CHUNK_OVERLAP_CHARS = 200
DEFAULT_CHROMA_DIR = ".chroma"

def get_collection(name: str):
    client = chromadb.HttpClient(host="localhost", port=8000)
    return client.get_or_create_collection(name=name)


def chunk_text(text: str, max_chars: int = CHUNK_MAX_CHARS, overlap: int = CHUNK_OVERLAP_CHARS) -> list[str]:
    """
    Simple char-based chunker.
    For Lesson 4: stable, predictable, easy to reason about.
    Upgrade later to token-based chunking + structure-aware splitting.
    """
    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    i = 0
    step = max_chars - overlap
    if step <= 0:
        raise ValueError("chunk step must be positive; reduce overlap or increase max_chars")

    while i < len(text):
        chunk = text[i:i + max_chars].strip()
        if chunk:
            chunks.append(chunk)
        i += step

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