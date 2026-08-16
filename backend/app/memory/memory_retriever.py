"""Memory-retriever overview: selects a small relevant subset of durable customer facts for the current request."""

import re

from app.models.models import CustomerMemory


class MemoryRetriever:
    """Use transparent lexical relevance until durable customer memory becomes large enough for separate vector search."""

    _token_pattern = re.compile(r"[a-z0-9_-]+", re.IGNORECASE)

    def retrieve(self, query: str, memories: list[CustomerMemory], limit: int = 5) -> list[CustomerMemory]:
        """Rank memory by overlapping request terms, then importance, without loading an unbounded history."""
        query_tokens = set(self._token_pattern.findall(query.lower()))
        ranked = []
        for memory in memories:
            content_tokens = set(self._token_pattern.findall(memory.content.lower()))
            overlap = len(query_tokens & content_tokens)
            score = overlap * 10 + memory.importance
            if overlap or not query_tokens:
                ranked.append((score, memory))
        ranked.sort(key=lambda item: (item[0], item[1].updated_at), reverse=True)
        return [memory for _, memory in ranked[:limit]]
