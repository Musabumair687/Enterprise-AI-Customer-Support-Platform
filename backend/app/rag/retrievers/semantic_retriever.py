"""Semantic retriever overview: embeds a question and converts Chroma cosine matches into typed retrieval results."""

from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.app.schemas import Chunk, RetrievedChunk
from app.rag.vectorstore.chroma_store import ChromaStore


class SemanticRetriever:
    """Retrieve conceptually similar support content from persistent ChromaDB."""

    def __init__(self, embedding_service: EmbeddingService, chroma_store: ChromaStore) -> None:
        self.embedding_service = embedding_service
        self.chroma_store = chroma_store

    def retrieve(self, query: str, top_k: int = 10) -> list[RetrievedChunk]:
        """Embed a question, query Chroma, and map vector distances to a higher-is-better score."""
        if self.chroma_store.count() == 0:
            return []
        results = self.chroma_store.query(self.embedding_service.embed_query(query), top_k)
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        return [
            RetrievedChunk(
                chunk=Chunk(
                    chunk_id=record_metadata.pop("chunk_id", f"semantic-{index}"),
                    text=document,
                    document_id=str(record_metadata.pop("document_id", "unknown")),
                    metadata=record_metadata,
                ),
                score=1.0 - float(distance),
                retriever="semantic",
            )
            for index, (document, metadata, distance) in enumerate(zip(documents, metadatas, distances, strict=True))
            for record_metadata in [dict(metadata)]
        ]
