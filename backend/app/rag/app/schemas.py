"""Schema overview: typed, serializable document and chunk contracts shared by every RAG component."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Document:
    """A source document after loading, before it is converted into retrieval chunks."""

    document_id: str
    content: str
    source: str
    file_name: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Chunk:
    """A meaningful, self-contained section of a document used during retrieval."""

    chunk_id: str
    text: str
    document_id: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RetrievedChunk:
    """A chunk returned by a retriever together with its retrieval score and source method."""

    chunk: Chunk
    score: float
    retriever: str
