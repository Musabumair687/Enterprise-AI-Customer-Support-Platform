"""Cross-encoder reranking with a deterministic local fallback for development."""

from collections.abc import Sequence
import re

from app.rag.app.schemas import RetrievedChunk


class CrossEncoderReranker:
    """Score query/chunk pairs with a sentence-transformers cross encoder when available."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2", allow_fallback: bool = True) -> None:
        self.model_name = model_name
        self.allow_fallback = allow_fallback
        self._model = None
        self._model_load_failed = False

    @property
    def model(self):
        """Load the model only on the first reranking request."""
        if self._model_load_failed:
            return None
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder
            except ImportError as exc:
                if not self.allow_fallback:
                    raise RuntimeError("Install sentence-transformers to use cross-encoder reranking.") from exc
                return None
            try:
                self._model = CrossEncoder(self.model_name)
            except Exception as exc:
                if not self.allow_fallback:
                    raise RuntimeError(f"Unable to load cross-encoder model '{self.model_name}'.") from exc
                self._model_load_failed = True
                return None
        return self._model

    def rerank(self, query: str, candidates: Sequence[RetrievedChunk], top_k: int = 5) -> list[RetrievedChunk]:
        """Return the most relevant candidates, preserving their original chunks and metadata."""
        if top_k < 1:
            raise ValueError("top_k must be at least 1.")
        if not query.strip() or not candidates:
            return []

        model = self.model
        if model is None:
            scores = self._fallback_scores(query, candidates)
        else:
            scores = [float(score) for score in model.predict([(query, candidate.chunk.text) for candidate in candidates])]
        ranked = sorted(enumerate(scores), key=lambda item: (-item[1], item[0]))[:top_k]
        return [
            RetrievedChunk(chunk=candidates[index].chunk, score=score, retriever="cross_encoder")
            for index, score in ranked
        ]

    @staticmethod
    def _fallback_scores(query: str, candidates: Sequence[RetrievedChunk]) -> list[float]:
        """Use lexical overlap only when no model is installed; it is not a semantic substitute."""
        query_terms = set(re.findall(r"[A-Za-z0-9_./:-]+", query.lower()))
        if not query_terms:
            return [0.0] * len(candidates)
        return [len(query_terms & set(re.findall(r"[A-Za-z0-9_./:-]+", candidate.chunk.text.lower()))) / len(query_terms) for candidate in candidates]
