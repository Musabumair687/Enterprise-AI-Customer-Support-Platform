"""Thin AI-facing adapter for the Phase 5 retrieval pipeline."""

from app.rag.pipeline.retrieval_pipeline import RetrievalPipeline
from app.tools.schemas import KnowledgeBaseResult, KnowledgeBaseSearchInput, KnowledgeBaseSearchOutput


def knowledge_base_search_tool(retrieval_pipeline: RetrievalPipeline, tool_input: KnowledgeBaseSearchInput) -> KnowledgeBaseSearchOutput:
    """Return bounded, traceable knowledge-base context for a support question."""
    context = retrieval_pipeline.retrieve(tool_input.query, candidate_k=tool_input.candidate_k, final_k=tool_input.final_k)
    return KnowledgeBaseSearchOutput(
        context=context.text,
        results=[KnowledgeBaseResult(chunk_id=result.chunk.chunk_id, score=result.score,
                                     source=str(result.chunk.metadata.get("source", "unknown")),
                                     section=str(result.chunk.metadata.get("section", "Document")), text=result.chunk.text)
                 for result in context.chunks],
    )
