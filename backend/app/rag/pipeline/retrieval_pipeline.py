"""Online retrieval orchestration: retrieve, fuse, rerank, and build context."""

from app.rag.context.context_builder import ContextBuilder, RetrievalContext
from app.rag.reranking.cross_encoder import CrossEncoderReranker
from app.rag.retrievers.keyword_retriever import KeywordRetriever
from app.rag.retrievers.rrf import ReciprocalRankFusion
from app.rag.retrievers.semantic_retriever import SemanticRetriever


class RetrievalPipeline:
    """Coordinate RAG retrieval stages while keeping provider details inside their own components."""

    def __init__(
        self,
        semantic_retriever: SemanticRetriever,
        keyword_retriever: KeywordRetriever,
        fusion: ReciprocalRankFusion | None = None,
        reranker: CrossEncoderReranker | None = None,
        context_builder: ContextBuilder | None = None,
    ) -> None:
        self.semantic_retriever = semantic_retriever
        self.keyword_retriever = keyword_retriever
        self.fusion = fusion or ReciprocalRankFusion()
        self.reranker = reranker or CrossEncoderReranker()
        self.context_builder = context_builder or ContextBuilder()

    def retrieve(self, query: str, candidate_k: int = 20, final_k: int = 5) -> RetrievalContext:
        """Return grounded, bounded context for one non-empty support question."""
        if not query.strip():
            raise ValueError("A query cannot be empty.")
        if candidate_k < 1 or final_k < 1:
            raise ValueError("candidate_k and final_k must be at least 1.")
        semantic = self.semantic_retriever.retrieve(query, candidate_k)
        keyword = self.keyword_retriever.retrieve(query, candidate_k)
        fused = self.fusion.fuse(semantic, keyword, top_k=candidate_k)
        reranked = self.reranker.rerank(query, fused, top_k=final_k)
        return self.context_builder.build(reranked)
