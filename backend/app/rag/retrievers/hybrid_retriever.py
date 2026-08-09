"""Hybrid retriever overview: runs semantic and keyword retrieval independently for later RRF fusion."""

from dataclasses import dataclass

from app.rag.retrievers.keyword_retriever import KeywordRetriever
from app.rag.retrievers.semantic_retriever import SemanticRetriever
from app.rag.app.schemas import RetrievedChunk


@dataclass(slots=True)
class HybridRetrievalResult:
    """Independent result sets that will be fused by the next RRF stage."""

    semantic: list[RetrievedChunk]
    keyword: list[RetrievedChunk]


class HybridRetriever:
    """Coordinate both retrieval strategies without deciding final rank order yet."""

    def __init__(self, semantic_retriever: SemanticRetriever, keyword_retriever: KeywordRetriever) -> None:
        self.semantic_retriever = semantic_retriever
        self.keyword_retriever = keyword_retriever

    def retrieve(self, query: str, top_k: int = 10) -> HybridRetrievalResult:
        """Return parallel semantic and keyword candidates for RRF fusion."""
        return HybridRetrievalResult(
            semantic=self.semantic_retriever.retrieve(query, top_k),
            keyword=self.keyword_retriever.retrieve(query, top_k),
        )
