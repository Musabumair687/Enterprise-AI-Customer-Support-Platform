"""Keyword retriever overview: returns BM25-ranked chunks for exact support terms and identifiers."""

from app.rag.indexing.bm25_index import BM25Index
from app.rag.app.schemas import RetrievedChunk


class KeywordRetriever:
    """Retrieve exact-term matches from the persisted BM25 index."""

    def __init__(self, bm25_index: BM25Index) -> None:
        self.bm25_index = bm25_index

    def retrieve(self, query: str, top_k: int = 10) -> list[RetrievedChunk]:
        """Return the best BM25 matches for a support question."""
        return self.bm25_index.search(query, top_k)
