"""Cleaner overview: normalizes Markdown whitespace while preserving support-critical commands, URLs, and codes."""

import re

from app.rag.app.schemas import Document


class DocumentCleaner:
    """Apply conservative text normalization without removing meaningful document content."""

    def clean(self, document: Document) -> Document:
        """Normalize line endings, trailing whitespace, and excessive blank lines."""
        content = document.content.replace("\r\n", "\n").replace("\r", "\n")
        content = "\n".join(line.rstrip() for line in content.split("\n"))
        content = re.sub(r"\n{3,}", "\n\n", content).strip()
        return Document(
            document_id=document.document_id,
            content=content,
            source=document.source,
            file_name=document.file_name,
            metadata=dict(document.metadata),
        )
