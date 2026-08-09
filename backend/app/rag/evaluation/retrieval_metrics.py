"""Recall, precision, and reciprocal-rank metrics for retrieval evaluation."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from app.rag.app.schemas import RetrievedChunk
from app.rag.context.context_builder import RetrievalContext
from app.rag.evaluation.test_dataset import RetrievalTestCase


@dataclass(frozen=True, slots=True)
class RetrievalMetrics:
    recall_at_k: float
    precision_at_k: float
    mean_reciprocal_rank: float


def evaluate(
    cases: Sequence[RetrievalTestCase],
    retrieve: Callable[[str], RetrievalContext | Sequence[RetrievedChunk]],
    k: int = 5,
) -> RetrievalMetrics:
    """Evaluate document-level relevance for a retrieval callable."""
    if not cases or k < 1:
        raise ValueError("cases must not be empty and k must be at least 1.")
    recalls: list[float] = []
    precisions: list[float] = []
    reciprocal_ranks: list[float] = []
    for case in cases:
        outcome = retrieve(case.question)
        results = outcome.chunks if isinstance(outcome, RetrievalContext) else list(outcome)
        returned = [str(result.chunk.metadata.get("file_name", "")) for result in results[:k]]
        expected = set(case.expected_documents)
        matches = [filename in expected for filename in returned]
        recalls.append(len(set(returned) & expected) / len(expected))
        precisions.append(sum(matches) / k)
        reciprocal_ranks.append(next((1 / rank for rank, match in enumerate(matches, start=1) if match), 0.0))
    return RetrievalMetrics(sum(recalls) / len(cases), sum(precisions) / len(cases), sum(reciprocal_ranks) / len(cases))
