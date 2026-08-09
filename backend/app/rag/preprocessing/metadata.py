"""Metadata parser overview: derives enterprise retrieval metadata from source paths, filenames, headings, and versions."""

import re
from pathlib import PurePosixPath

from app.rag.app.schemas import Document


class MetadataParser:
    """Attach traceable source, category, product, type, title, and version metadata to documents."""

    _title_pattern = re.compile(r"^#\s+(.+)$", re.MULTILINE)
    _version_pattern = re.compile(r"\bversion\s*[:v]?\s*(\d+(?:\.\d+){0,3})\b", re.IGNORECASE)
    _document_types = {
        "administrator_guides": "administrator guide",
        "company": "company information",
        "faq": "faq",
        "manuals": "user manual",
        "policies": "policy",
        "products": "product overview",
        "release_notes": "release notes",
        "troubleshooting": "troubleshooting guide",
    }

    def enrich(self, document: Document) -> Document:
        """Return a copy of a document with metadata used by filters, citations, and chunking."""
        source_path = PurePosixPath(document.source)
        category = source_path.parts[0] if len(source_path.parts) > 1 else "general"
        title_match = self._title_pattern.search(document.content)
        title = title_match.group(1).strip() if title_match else source_path.stem.replace("-", " ").title()
        version_match = self._version_pattern.search(document.content)
        metadata = {
            **document.metadata,
            "source": document.source,
            "file_name": document.file_name,
            "category": category,
            "document_type": self._document_types.get(category, category.replace("_", " ")),
            "product": self._product_from_name(document.file_name),
            "title": title,
            "version": version_match.group(1) if version_match else None,
        }
        return Document(document.document_id, document.content, document.source, document.file_name, metadata)

    @staticmethod
    def _product_from_name(file_name: str) -> str | None:
        normalized = file_name.lower()
        for slug, product in (
            ("clouddesk-analytics", "CloudDesk Analytics"),
            ("clouddesk-api-platform", "CloudDesk API Platform"),
            ("clouddesk-chat", "CloudDesk Chat"),
            ("clouddesk-mobile", "CloudDesk Mobile"),
            ("clouddesk-tickets", "CloudDesk Tickets"),
        ):
            if slug in normalized:
                return product
        return None
