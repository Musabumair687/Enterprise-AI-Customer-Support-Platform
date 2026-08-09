"""BM25 index overview: provides persistent exact-term ranking for error codes, endpoints, and product versions."""

from collections import Counter
from hashlib import sha256
from math import log
from pathlib import Path
import pickle
import re

from app.config.config import PROJECT_ROOT
from app.rag.app.schemas import Chunk, RetrievedChunk


DEFAULT_BM25_PATH = PROJECT_ROOT / "backend" / "data" / "rag" / "bm25.pkl"
INDEX_SCHEMA_VERSION = 2
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_./:-]+")


class BM25Index:
    """A small dependency-free BM25 implementation with a serializable inverted index."""

    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75) -> None:
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.document_tokens = [self.tokenize(chunk.text) for chunk in chunks]
        self.term_frequencies = [Counter(tokens) for tokens in self.document_tokens]
        self.document_frequencies: Counter[str] = Counter()
        self.postings: dict[str, list[int]] = {}
        for index, tokens in enumerate(self.document_tokens):
            self.document_frequencies.update(set(tokens))
            for term in set(tokens):
                self.postings.setdefault(term, []).append(index)
        self.average_document_length = (
            sum(len(tokens) for tokens in self.document_tokens) / len(self.document_tokens)
            if self.document_tokens
            else 0.0
        )
        self.fingerprint = self.chunk_fingerprint(chunks)

    @staticmethod
    def chunk_fingerprint(chunks: list[Chunk]) -> str:
        """Return a stable identity for the exact chunk corpus represented by an index."""
        digest = sha256()
        for chunk in chunks:
            digest.update(chunk.chunk_id.encode("utf-8"))
            digest.update(b"\0")
            digest.update(chunk.text.encode("utf-8"))
            digest.update(b"\0")
        return digest.hexdigest()

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """Preserve support identifiers such as ERR-CD-401 and POST /v1/tickets as searchable terms."""
        return [token.lower() for token in TOKEN_PATTERN.findall(text)]

    def search(self, query: str, top_k: int = 10) -> list[RetrievedChunk]:
        """Rank chunks using Okapi BM25 and return only positive keyword matches."""
        if top_k < 1:
            raise ValueError("top_k must be at least 1.")
        query_tokens = self.tokenize(query)
        if not query_tokens or not self.chunks:
            return []
        total_documents = len(self.chunks)
        scores: dict[int, float] = {}
        candidate_indexes = {index for term in query_tokens for index in self.postings.get(term, [])}
        for index in candidate_indexes:
            tokens = self.document_tokens[index]
            frequencies = self.term_frequencies[index]
            length_normalizer = 1 - self.b + self.b * len(tokens) / self.average_document_length
            score = 0.0
            for term in query_tokens:
                frequency = frequencies.get(term, 0)
                if frequency:
                    document_frequency = self.document_frequencies[term]
                    inverse_document_frequency = log(1 + (total_documents - document_frequency + 0.5) / (document_frequency + 0.5))
                    score += inverse_document_frequency * frequency * (self.k1 + 1) / (frequency + self.k1 * length_normalizer)
            scores[index] = score
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return [RetrievedChunk(self.chunks[index], score, "keyword") for index, score in ranked[:top_k] if score > 0]

    def save(self, path: Path = DEFAULT_BM25_PATH) -> None:
        """Persist the index and source chunks so it can be reused without re-tokenizing all documents."""
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": INDEX_SCHEMA_VERSION,
            "chunks": self.chunks,
            "k1": self.k1,
            "b": self.b,
            "fingerprint": self.fingerprint,
            "document_tokens": self.document_tokens,
            "term_frequencies": self.term_frequencies,
            "document_frequencies": self.document_frequencies,
            "postings": self.postings,
            "average_document_length": self.average_document_length,
        }
        with path.open("wb") as index_file:
            pickle.dump(payload, index_file, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, path: Path = DEFAULT_BM25_PATH) -> "BM25Index":
        """Load a trusted index artifact produced by this application."""
        with path.open("rb") as index_file:
            payload = pickle.load(index_file)
        if payload.get("schema_version") != INDEX_SCHEMA_VERSION:
            raise ValueError("Unsupported BM25 index schema version.")
        index = cls.__new__(cls)
        index.chunks = payload["chunks"]
        index.k1 = payload["k1"]
        index.b = payload["b"]
        index.fingerprint = payload["fingerprint"]
        index.document_tokens = payload["document_tokens"]
        index.term_frequencies = payload["term_frequencies"]
        index.document_frequencies = payload["document_frequencies"]
        index.postings = payload["postings"]
        index.average_document_length = payload["average_document_length"]
        return index
