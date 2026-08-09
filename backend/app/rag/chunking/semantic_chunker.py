"""Semantic chunker overview: keeps Markdown sections, paragraphs, and code blocks together whenever practical."""

from hashlib import sha256
import re

from app.rag.app.schemas import Chunk, Document


class SemanticChunker:
    """Create bounded chunks with a heading context instead of arbitrary fixed-width slices."""

    def __init__(self, max_characters: int = 1400, overlap_characters: int = 180) -> None:
        if max_characters <= 0 or overlap_characters < 0 or overlap_characters >= max_characters:
            raise ValueError("max_characters must be positive and greater than overlap_characters.")
        self.max_characters = max_characters
        self.overlap_characters = overlap_characters

    def chunk(self, document: Document) -> list[Chunk]:
        """Split a document by Markdown heading, then pack paragraphs into readable retrieval chunks."""
        sections = self._sections(document.content)
        chunks: list[Chunk] = []
        for section_heading, section_text in sections:
            for text in self._pack_paragraphs(section_text):
                index = len(chunks)
                chunk_id = sha256(f"{document.document_id}:{index}:{text}".encode("utf-8")).hexdigest()[:20]
                chunks.append(Chunk(chunk_id, text, document.document_id, {**document.metadata, "section": section_heading, "chunk_index": index}))
        return chunks

    @staticmethod
    def _sections(content: str) -> list[tuple[str, str]]:
        """Split only on real Markdown headings, never headings shown inside fenced code examples."""
        heading_pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
        sections: list[tuple[str, str]] = []
        current_heading = "Document"
        current_lines: list[str] = []
        in_fenced_code_block = False

        def save_section() -> None:
            text = "\n".join(current_lines).strip()
            if text:
                sections.append((current_heading, f"{current_heading}\n\n{text}".strip()))

        for line in content.splitlines():
            if line.strip().startswith(("```", "~~~")):
                in_fenced_code_block = not in_fenced_code_block
            heading_match = None if in_fenced_code_block else heading_pattern.match(line)
            if heading_match:
                save_section()
                current_heading = heading_match.group(2).strip()
                current_lines = []
            else:
                current_lines.append(line)
        save_section()
        return sections

    def _pack_paragraphs(self, text: str) -> list[str]:
        paragraphs = self._paragraphs_preserving_code_blocks(text)
        packed: list[str] = []
        current = ""
        for paragraph in paragraphs:
            if len(paragraph) > self.max_characters:
                if current:
                    packed.append(current)
                    current = ""
                packed.extend(self._split_long_text(paragraph))
            elif not current:
                current = paragraph
            elif len(current) + len(paragraph) + 2 <= self.max_characters:
                current = f"{current}\n\n{paragraph}"
            else:
                packed.append(current)
                overlap = current[-self.overlap_characters :].strip()
                current = f"{overlap}\n\n{paragraph}" if overlap else paragraph
        if current:
            packed.append(current)
        return packed

    @staticmethod
    def _paragraphs_preserving_code_blocks(text: str) -> list[str]:
        """Keep every fenced code block as one unit even if it contains blank lines."""
        paragraphs: list[str] = []
        current_lines: list[str] = []
        in_fenced_code_block = False
        for line in text.splitlines():
            if line.strip().startswith(("```", "~~~")):
                in_fenced_code_block = not in_fenced_code_block
            if not in_fenced_code_block and not line.strip():
                paragraph = "\n".join(current_lines).strip()
                if paragraph:
                    paragraphs.append(paragraph)
                current_lines = []
            else:
                current_lines.append(line)
        paragraph = "\n".join(current_lines).strip()
        if paragraph:
            paragraphs.append(paragraph)
        return paragraphs

    def _split_long_text(self, text: str) -> list[str]:
        chunks: list[str] = []
        start = 0
        while start < len(text):
            end = min(start + self.max_characters, len(text))
            if end < len(text):
                boundary = max(text.rfind(" ", start, end), text.rfind("\n", start, end))
                end = boundary if boundary > start else end
            chunks.append(text[start:end].strip())
            if end >= len(text):
                break
            start = max(end - self.overlap_characters, start + 1)
        return [chunk for chunk in chunks if chunk]
