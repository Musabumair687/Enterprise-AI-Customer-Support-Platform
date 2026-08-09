from app.rag.app.schemas import Chunk, RetrievedChunk
from app.rag.context.context_builder import ContextBuilder
from app.rag.evaluation.retrieval_metrics import evaluate
from app.rag.evaluation.test_dataset import RetrievalTestCase
from app.rag.reranking.cross_encoder import CrossEncoderReranker
from app.rag.retrievers.rrf import ReciprocalRankFusion


def _result(chunk_id: str, text: str, source: str) -> RetrievedChunk:
    return RetrievedChunk(
        chunk=Chunk(chunk_id, text, "document", {"source": source, "file_name": source, "section": "Guide"}),
        score=1.0,
        retriever="test",
    )


def test_rrf_rewards_a_chunk_present_in_both_rankings() -> None:
    chunk_a = _result("a", "reset password steps", "a.md")
    chunk_b = _result("b", "billing information", "b.md")
    chunk_c = _result("c", "unrelated", "c.md")
    fused = ReciprocalRankFusion().fuse([chunk_a, chunk_c], [chunk_b, chunk_a])
    assert [result.chunk.chunk_id for result in fused] == ["a", "b", "c"]


def test_context_builder_deduplicates_and_preserves_sources() -> None:
    chunk = _result("a", "reset password steps", "manual.md")
    context = ContextBuilder().build([chunk, chunk])
    assert len(context.chunks) == 1
    assert context.sources == [{"chunk_id": "a", "source": "manual.md", "section": "Guide"}]
    assert "reset password steps" in context.text


def test_fallback_reranker_and_metrics_work_without_a_downloaded_model() -> None:
    relevant = _result("a", "reset password steps", "manual.md")
    irrelevant = _result("b", "invoice receipt", "billing.md")
    ranked = CrossEncoderReranker(allow_fallback=True).rerank("reset password", [irrelevant, relevant])
    assert ranked[0].chunk.chunk_id == "a"
    metrics = evaluate(
        [RetrievalTestCase("reset password", ("manual.md",))],
        lambda _: ranked,
    )
    assert metrics.recall_at_k == metrics.mean_reciprocal_rank == 1.0
    assert metrics.precision_at_k == 0.2
