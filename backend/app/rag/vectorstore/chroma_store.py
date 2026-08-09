"""Chroma store overview: persists chunk embeddings locally and exposes semantic nearest-neighbour search."""

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from app.config import get_settings
from app.rag.app.schemas import Chunk


DEFAULT_CHROMA_PATH = Path(get_settings().chroma_path)


class ChromaStore:
    """Own the Chroma collection so callers never depend on ChromaDB-specific APIs."""

    def __init__(self, path: Path = DEFAULT_CHROMA_PATH, collection_name: str = "support_knowledge") -> None:
        try:
            import chromadb
        except ImportError as exc:
            raise RuntimeError("ChromaDB is required for vector indexing. Install backend requirements first.") from exc
        path.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(path))
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        """Persist or update chunks atomically in batches while retaining their traceable metadata."""
        if len(chunks) != len(embeddings):
            raise ValueError("Each chunk must have exactly one embedding.")
        for start in range(0, len(chunks), 100):
            batch_chunks = chunks[start : start + 100]
            batch_embeddings = embeddings[start : start + 100]
            self._collection.upsert(
                ids=[chunk.chunk_id for chunk in batch_chunks],
                documents=[chunk.text for chunk in batch_chunks],
                embeddings=[list(vector) for vector in batch_embeddings],
                metadatas=[self._metadata_for_storage(chunk) for chunk in batch_chunks],
            )

    def query(self, embedding: Sequence[float], top_k: int = 10) -> dict[str, Any]:
        """Return raw Chroma matches; the semantic retriever converts them to application schemas."""
        if top_k < 1:
            raise ValueError("top_k must be at least 1.")
        record_count = self.count()
        if record_count == 0:
            raise ValueError("The Chroma collection is empty. Build the vector index before querying.")
        return self._collection.query(
            query_embeddings=[list(embedding)],
            n_results=min(top_k, record_count),
            include=["documents", "metadatas", "distances"],
        )

    def count(self) -> int:
        """Return the number of chunks already stored in the persistent collection."""
        return self._collection.count()

    def is_current(self, fingerprint: str, embedding_model: str, expected_count: int) -> bool:
        """Confirm persistent vectors were built from this chunk corpus and embedding model."""
        metadata = self._collection.metadata or {}
        return (
            self.count() == expected_count
            and metadata.get("corpus_fingerprint") == fingerprint
            and metadata.get("embedding_model") == embedding_model
            and metadata.get("index_complete") is True
        )

    def existing_ids(self, chunk_ids: Sequence[str]) -> set[str]:
        """Return IDs already persisted, allowing interrupted embedding jobs to resume safely."""
        if not chunk_ids:
            return set()
        records = self._collection.get(ids=list(chunk_ids), include=[])
        return set(records["ids"])

    def begin_index_build(self, fingerprint: str, embedding_model: str) -> None:
        """Mark an index build in progress and block accidental mixing of embedding models."""
        metadata = dict(self._collection.metadata or {})
        metadata.pop("hnsw:space", None)
        stored_model = metadata.get("embedding_model")
        if stored_model and stored_model != embedding_model:
            raise RuntimeError(
                "This Chroma collection uses a different embedding model. "
                "Use a new collection path rather than mixing incompatible vectors."
            )
        metadata.update(
            {
                "corpus_fingerprint": fingerprint,
                "embedding_model": embedding_model,
                "index_complete": False,
            }
        )
        self._collection.modify(metadata=metadata)

    def sync_chunk_ids(self, expected_ids: set[str]) -> int:
        """Remove obsolete vectors so changed documents cannot leave duplicate or stale retrieval results."""
        existing_ids = set(self._collection.get(include=[])["ids"])
        obsolete_ids = existing_ids - expected_ids
        if obsolete_ids:
            self._collection.delete(ids=sorted(obsolete_ids))
        return len(obsolete_ids)

    def set_index_metadata(self, fingerprint: str, embedding_model: str) -> None:
        """Record vector compatibility information without deleting the existing collection."""
        metadata = dict(self._collection.metadata or {})
        # Chroma treats this creation-time setting as immutable and rejects it on modify().
        metadata.pop("hnsw:space", None)
        metadata.update(
            {"corpus_fingerprint": fingerprint, "embedding_model": embedding_model, "index_complete": True}
        )
        self._collection.modify(metadata=metadata)

    @staticmethod
    def _metadata_for_storage(chunk: Chunk) -> dict[str, str | int | float | bool]:
        metadata: dict[str, str | int | float | bool] = {
            "chunk_id": chunk.chunk_id,
            "document_id": chunk.document_id,
        }
        for key, value in chunk.metadata.items():
            if value is not None and isinstance(value, (str, int, float, bool)):
                metadata[key] = value
        return metadata
