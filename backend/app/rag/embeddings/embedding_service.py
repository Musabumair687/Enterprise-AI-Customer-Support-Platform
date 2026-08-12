"""Embedding service overview: isolates Gemini embedding calls behind one stable interface for indexing and retrieval."""

from collections.abc import Sequence
from typing import Protocol

from app.config import get_settings


class EmbeddingService(Protocol):
    """Provider-neutral contract used by the vector store and semantic retriever."""

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


class GeminiEmbeddingService:
    """Embed text with the Gemini model selected in the application's existing settings."""

    def __init__(self, model_name: str | None = None, api_key: str | None = None, batch_size: int | None = None) -> None:
        settings = get_settings()
        self.model_name = model_name or settings.embedding_model
        self.api_key = api_key or settings.gemini_api_key
        self.batch_size = batch_size or settings.embedding_batch_size
        self.pause_seconds = settings.embedding_batch_pause_seconds
        if self.batch_size < 1:
            raise ValueError("batch_size must be at least 1.")
        self._client = None

    @property
    def client(self):
        """Create the provider client only when embeddings are actually requested."""
        if self._client is None:
            try:
                from langchain_google_genai import GoogleGenerativeAIEmbeddings
            except ImportError as exc:
                raise RuntimeError(
                    "Gemini embeddings require langchain-google-genai. Install backend requirements first."
                ) from exc
            # The integration exposes ``api_key`` as a Pydantic alias but its
            # generated type signature exposes a different field name.  Parsing
            # the provider payload keeps the supported public API and avoids a
            # false editor error on the alias keyword.
            self._client = GoogleGenerativeAIEmbeddings.model_validate(
                {"model": self.model_name, "api_key": self.api_key}
            )
        return self._client

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        """Create one vector per document/chunk while preserving the supplied order."""
        if not texts:
            return []
        embeddings: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = list(texts[start : start + self.batch_size])
            embeddings.extend(list(vector) for vector in self.client.embed_documents(batch))
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        """Create a vector for one customer-support question."""
        if not text.strip():
            raise ValueError("A query cannot be empty.")
        return list(self.client.embed_query(text))
