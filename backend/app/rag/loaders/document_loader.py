"""Document loader overview: selects the appropriate file loader and recursively loads the knowledge base."""

from pathlib import Path

from app.rag.loaders.markdown_loader import MarkdownLoader
from app.rag.app.schemas import Document


class DocumentLoader:
    """Main loader interface; future PDF, DOCX, and HTML loaders can be added here."""

    def __init__(self) -> None:
        self._markdown_loader = MarkdownLoader()

    def load_directory(self, knowledge_base_path: Path) -> list[Document]:
        """Load supported documents in a stable path order for reproducible ingestion."""
        if not knowledge_base_path.is_dir():
            raise FileNotFoundError(f"Knowledge base directory was not found: {knowledge_base_path}")

        markdown_files = sorted(knowledge_base_path.rglob("*.md"))
        return [self._markdown_loader.load(path, knowledge_base_path) for path in markdown_files]
