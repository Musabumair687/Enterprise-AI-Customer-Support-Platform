"""Build a bounded, traceable LLM context from final retrieval results."""

from dataclasses import dataclass
from collections.abc import Sequence

from app.rag.app.schemas import RetrievedChunk


@dataclass(slots=True)
class RetrievalContext:
    """LLM-ready context together with the chunks and sources that produced it."""

    text: str
    chunks: list[RetrievedChunk]
    sources: list[dict[str, str]]


class ContextBuilder:
    """Deduplicate evidence and retain source metadata within a conservative token budget."""

    def __init__(self, max_tokens: int = 3_000) -> None:
        if max_tokens < 1:
            raise ValueError("max_tokens must be at least 1.")
        self.max_tokens = max_tokens

    def build(self, results: Sequence[RetrievedChunk]) -> RetrievalContext:
        """Create labelled context blocks without splitting a selected chunk."""
        unique_results: list[RetrievedChunk] = []
        seen_ids: set[str] = set()
        for result in results:
            if result.chunk.chunk_id not in seen_ids:
                seen_ids.add(result.chunk.chunk_id)
                unique_results.append(result)

        groups: list[list[RetrievedChunk]] = []
        for result in unique_results:
            if groups and self._are_adjacent(groups[-1][-1], result):
                groups[-1].append(result)
            else:
                groups.append([result])

        selected: list[RetrievedChunk] = []
        sources: list[dict[str, str]] = []
        seen_ids: set[str] = set()
        used_tokens = 0
        blocks: list[str] = []
        for group in groups:
            first_chunk = group[0].chunk
            source = str(first_chunk.metadata.get("source", "unknown"))
            section = str(first_chunk.metadata.get("section", "Document"))
            block = f"[Source: {source} | Section: {section}]\n" + "\n\n".join(result.chunk.text for result in group)
            block_tokens = self._estimate_tokens(block)
            if selected and used_tokens + block_tokens > self.max_tokens:
                continue
            if not selected and block_tokens > self.max_tokens:
                continue
            used_tokens += block_tokens
            for result in group:
                chunk = result.chunk
                seen_ids.add(chunk.chunk_id)
                selected.append(result)
                sources.append(
                    {
                        "chunk_id": chunk.chunk_id,
                        "source": str(chunk.metadata.get("source", "unknown")),
                        "section": str(chunk.metadata.get("section", "Document")),
                    }
                )
            blocks.append(block)
        return RetrievalContext(text="\n\n---\n\n".join(blocks), chunks=selected, sources=sources)

    @staticmethod
    def _are_adjacent(previous: RetrievedChunk, current: RetrievedChunk) -> bool:
        """Allow neighbouring chunks from one document section to share a context block."""
        previous_index = previous.chunk.metadata.get("chunk_index")
        current_index = current.chunk.metadata.get("chunk_index")
        return (
            previous.chunk.document_id == current.chunk.document_id
            and previous.chunk.metadata.get("section") == current.chunk.metadata.get("section")
            and isinstance(previous_index, int)
            and isinstance(current_index, int)
            and current_index == previous_index + 1
        )

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """A safe, provider-independent approximation used solely for a context budget."""
        return max(1, (len(text) + 3) // 4)
