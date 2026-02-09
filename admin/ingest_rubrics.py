from __future__ import annotations
from importlib import metadata
import sys
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
import traceback

# Add parent directory to path so we can import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.doc_tools import load_manifest, load_text_file
from src.tools.vector_tools import get_collection, embed_batch, chunk_text, batched

RUBRICS_COLLECTION = "rubrics"
DEFAULT_CHROMA_DIR = ".chroma"
DEFAULT_MANIFEST_PATH = "src/data/manifest.json"

load_dotenv(override=True)

client = OpenAI()

def ingest_sources(
    manifest_path: str = DEFAULT_MANIFEST_PATH,    
    collection_name: str = RUBRICS_COLLECTION,
    embed_batch_size: int = 64,
) -> None:
     
    """
    Reads manifest -> loads sources -> chunks -> embeds -> upserts to Chroma.

    Metadata design:
      - assignment_id: stable join key (your domain truth)
      - doc_type: retrieval policy control (rubric vs question vs inferred)
      - source_ref: provenance/debuggability
      - chunk_index: deterministic ordering within a source
    """
    entries = load_manifest(manifest_path)
    collection = get_collection(name=collection_name)

    total_sources = 0
    total_chunks = 0
    print ("Starting ingestion...\n")
    for entry in entries:
        assignment_id = entry.assignment_id
        print(f"Processing assignment_id={assignment_id} with {len(entry.sources)} sources")

        for src in entry.sources:
            total_sources += 1
            p = Path(src.path)
            if not p.exists():
                raise FileNotFoundError(f"Missing source file: {src.path} (assignment_id={assignment_id})")

            if p.suffix.lower() not in {".md", ".txt"}:
                raise ValueError(f"Unsupported file type for Lesson 4: {p.suffix} (path={src.path})")

            raw = load_text_file(p)
            print(f"  {p.name}: raw_chars={len(raw)}")
            
            chunks = chunk_text(raw)
            if not chunks:
                continue

            # Build IDs and metadata per chunk
            ids = [f"{assignment_id}::{src.doc_type}::{p.name}::chunk::{i}" for i in range(len(chunks))]
            metadata = [{
                "assignment_id": assignment_id,
                "doc_type": src.doc_type,
                "source_type": p.suffix.lower().lstrip("."),   # "md" | "txt"
                "source_ref": str(p),
                "chunk_index": i,
            } for i in range(len(chunks))]

            # Embed in batches to keep request sizes reasonable
            embeddings: list[list[float]] = []
            for chunk_batch in batched(chunks, embed_batch_size):
                embeddings.extend(embed_batch(client, chunk_batch))

            # Safety: ensure alignment
            if not (len(ids) == len(chunks) == len(embeddings) == len(metadata)):
                raise RuntimeError("Alignment error: ids/chunks/embeddings/metadatas length mismatch")
                        
            try:            
                collection.upsert(
                    ids=ids,
                    documents=chunks,
                    embeddings=embeddings,
                    metadatas=metadata,
                )
            except BaseException as e:  # <-- important: catches SystemExit/KeyboardInterrupt too
                print(f"Error upserting to Chroma for assignment_id={assignment_id}, source={src.path}")
                raise
            total_chunks += len(chunks)

    print(f"\nDone. Sources ingested: {total_sources}, total chunks upserted: {total_chunks}")
    print(f"Chroma: collection={collection_name}")

if __name__ == "__main__":    
    try:
        ingest_sources()
    except BaseException:
        traceback.print_exc()
        raise