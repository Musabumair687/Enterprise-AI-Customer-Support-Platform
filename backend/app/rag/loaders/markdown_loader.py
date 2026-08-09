"""Markdown loader overview: reads one UTF-8 Markdown file and gives it a stable document identity."""

from hashlib import sha256
from pathlib import Path

from app.rag.app.schemas import Document


class MarkdownLoader:
    """Load Markdown files without interpreting or discarding their support content."""

    def load(self, path: Path, knowledge_base_path: Path) -> Document:
        """Read one Markdown file and return the standard internal document representation."""
        resolved_path = path.resolve()
        relative_source = resolved_path.relative_to(knowledge_base_path.resolve()).as_posix()
        document_id = sha256(relative_source.encode("utf-8")).hexdigest()[:16]
        return Document(
            document_id=document_id,
            content=resolved_path.read_text(encoding="utf-8"),
            source=relative_source,
            file_name=resolved_path.name,
        )
