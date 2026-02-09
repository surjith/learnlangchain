from __future__ import annotations

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

from src.data.manifest_schema import RetrievalResult

EMBED_MODEL = "text-embedding-3-small"
load_dotenv(override=True)  # Load environment variables from .env file

class RubricRetriever:
    def __init__(self, host: str = "localhost", port: int = 8000, collection_name: str = "rubrics"):
        self._chroma = chromadb.HttpClient(host=host, port=port)
        self._col = self._chroma.get_collection(collection_name)
        self._openai = OpenAI()

    def _embed_query(self, text: str) -> list[float]:
        resp = self._openai.embeddings.create(model=EMBED_MODEL, input=[text])
        return resp.data[0].embedding

    def retrieve_rubric_snippet(
        self,
        assignment_id: str,
        query: str = "rubric marking criteria assessment criteria",
        k: int = 8,
    ) -> RetrievalResult | None:
        qvec = self._embed_query(query)

        res = self._col.query(
            query_embeddings=[qvec],
            n_results=k,
            where={"$and": [{"assignment_id": assignment_id}, {"doc_type": "rubric"}]},
            include=["documents", "distances"],
        )
        docs = (res.get("documents") or [[]])[0]
        dists = (res.get("distances") or [[]])[0]
        if docs:
            return RetrievalResult(
                text="\n\n".join(docs),
                num_chunks=len(docs),
                avg_distance=sum(dists) / len(dists),
                source="rubric",
            )

        # 2) Fallback to assignment question
        res2 = self._col.query(
            query_embeddings=[qvec],
            n_results=min(k, 2),
            where={"$and": [
                {"assignment_id": assignment_id},
                {"doc_type": "assignment_question"},
            ]},
            include=["documents", "distances"],
        )

        docs2 = (res2.get("documents") or [[]])[0]
        dists2 = (res2.get("distances") or [[]])[0]

        if docs2:
            return RetrievalResult(
                text="\n\n".join(docs2),
                num_chunks=len(docs2),
                avg_distance=sum(dists2) / len(dists2),
                source="assignment_question",
            )

        return RetrievalResult(
            text=None,
            num_chunks=0,
            avg_distance=None,
            source="none",
        )