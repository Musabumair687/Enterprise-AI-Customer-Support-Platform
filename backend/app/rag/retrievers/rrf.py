"""Reciprocal-rank fusion for combining independent retrieval rankings."""

from collections.abc import Sequence

from app.rag.app.schemas import RetrievedChunk


class ReciprocalRankFusion:
    """Fuse rankings without comparing incompatible BM25 and vector score scales."""

    def __init__(self, rank_constant: int = 60) -> None:
        if rank_constant < 1:
            raise ValueError("rank_constant must be at least 1.")
        self.rank_constant = rank_constant

    def fuse(self, *rankings: Sequence[RetrievedChunk], top_k: int = 20) -> list[RetrievedChunk]:
        """Return unique chunks scored by the sum of ``1 / (k + rank)``."""
        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        scores: dict[str, float] = {}
        chunks: dict[str, RetrievedChunk] = {}
        first_seen: dict[str, int] = {}
        ordinal = 0
        for ranking in rankings:
            for rank, result in enumerate(ranking, start=1):
                chunk_id = result.chunk.chunk_id
                scores[chunk_id] = scores.get(chunk_id, 0.0) + 1 / (self.rank_constant + rank)
                chunks.setdefault(chunk_id, result)
                first_seen.setdefault(chunk_id, ordinal)
                ordinal += 1

        ranked_ids = sorted(scores, key=lambda chunk_id: (-scores[chunk_id], first_seen[chunk_id], chunk_id))
        return [
            RetrievedChunk(chunk=chunks[chunk_id].chunk, score=scores[chunk_id], retriever="rrf")
            for chunk_id in ranked_ids[:top_k]
        ]
