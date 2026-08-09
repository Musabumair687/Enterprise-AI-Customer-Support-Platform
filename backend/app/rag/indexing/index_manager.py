"""Index manager overview: builds persistent Chroma and BM25 indexes from the cached ingestion chunks."""

from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.embeddings.embedding_service import GeminiEmbeddingService
from app.rag.indexing.bm25_index import BM25Index, DEFAULT_BM25_PATH
from app.rag.pipeline.ingestion_pipeline import IngestionPipeline
from app.rag.vectorstore.chroma_store import ChromaStore
import argparse
from time import sleep


class IndexManager:
    """Coordinate the two independent indexes while keeping ingestion and retrieval code separate."""

    def __init__(self, embedding_service: EmbeddingService, chroma_store: ChromaStore, bm25_index: BM25Index | None = None) -> None:
        self.embedding_service = embedding_service
        self.chroma_store = chroma_store
        self.bm25_index = bm25_index

    def build(self, force: bool = False) -> BM25Index:
        """Reuse current persistent indexes unless the chunk corpus or embedding model changed."""
        chunks = IngestionPipeline.load_chunks()
        fingerprint = BM25Index.chunk_fingerprint(chunks)
        embedding_model = getattr(self.embedding_service, "model_name", type(self.embedding_service).__qualname__)
        if not force and DEFAULT_BM25_PATH.exists() and self.chroma_store.is_current(fingerprint, embedding_model, len(chunks)):
            existing_index = BM25Index.load()
            if existing_index.fingerprint == fingerprint:
                self.bm25_index = existing_index
                return existing_index

        self.chroma_store.begin_index_build(fingerprint, embedding_model)
        self.chroma_store.sync_chunk_ids({chunk.chunk_id for chunk in chunks})
        existing_ids = set() if force else self.chroma_store.existing_ids([chunk.chunk_id for chunk in chunks])
        pending_chunks = [chunk for chunk in chunks if chunk.chunk_id not in existing_ids]
        batch_size = getattr(self.embedding_service, "batch_size", 100)
        pause_seconds = getattr(self.embedding_service, "pause_seconds", 0.0)
        for start in range(0, len(pending_chunks), batch_size):
            batch = pending_chunks[start : start + batch_size]
            embeddings = self.embedding_service.embed_documents([chunk.text for chunk in batch])
            self.chroma_store.upsert(batch, embeddings)
            if start + batch_size < len(pending_chunks) and pause_seconds:
                sleep(pause_seconds)
        self.bm25_index = BM25Index(chunks)
        self.bm25_index.save()
        self.chroma_store.set_index_metadata(fingerprint, embedding_model)
        return self.bm25_index


def main() -> None:
    """Build both persistent indexes as an explicit offline command-line task."""
    parser = argparse.ArgumentParser(description="Build or reuse the persistent RAG indexes.")
    parser.add_argument("--force", action="store_true", help="Re-embed all cached chunks even when indexes are current.")
    args = parser.parse_args()
    manager = IndexManager(GeminiEmbeddingService(), ChromaStore())
    bm25_index = manager.build(force=args.force)
    print(f"Indexed {len(bm25_index.chunks)} chunks into ChromaDB and the BM25 index.")


if __name__ == "__main__":
    main()
