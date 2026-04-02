"""
ContextLoader - Load documents from various sources to use as AI context.
Supports plain text, PDF, DOCX, JSON, YAML, CSV, and URLs.
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Union


class ContextLoader:
    """
    Loads documents from files or URLs and returns their text content
    to be used as context for GenAI calls.
    """

    def load(self, source: str) -> str:
        """
        Auto-detect source type and load content.

        Args:
            source: File path or URL.

        Returns:
            Text content of the document.
        """
        if source.startswith("http://") or source.startswith("https://"):
            return self.load_url(source)

        path = Path(source)
        ext = path.suffix.lower()

        loaders = {
            ".txt": self.load_text,
            ".md": self.load_text,
            ".json": self.load_json,
            ".yaml": self.load_yaml,
            ".yml": self.load_yaml,
            ".csv": self.load_csv,
            ".pdf": self.load_pdf,
            ".docx": self.load_docx,
        }

        loader = loaders.get(ext, self.load_text)
        return loader(source)

    def load_text(self, path: str) -> str:
        """Load plain text or markdown file."""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def load_json(self, path: str) -> str:
        """Load JSON file and return as formatted string."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2, ensure_ascii=False)

    def load_yaml(self, path: str) -> str:
        """Load YAML file and return as string."""
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML not installed. Run: pip install pyyaml")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return json.dumps(data, indent=2, ensure_ascii=False)

    def load_csv(self, path: str) -> str:
        """Load CSV file and return as readable text."""
        import csv
        rows = []
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(", ".join(f"{k}: {v}" for k, v in row.items()))
        return "\n".join(rows)

    def load_pdf(self, path: str) -> str:
        """Load PDF file and extract text."""
        try:
            import pypdf
            reader = pypdf.PdfReader(path)
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n\n".join(pages)
        except ImportError:
            pass

        try:
            import pdfplumber
            with pdfplumber.open(path) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
            return "\n\n".join(pages)
        except ImportError:
            raise ImportError(
                "PDF support requires pypdf or pdfplumber. "
                "Run: pip install pypdf  or  pip install pdfplumber"
            )

    def load_docx(self, path: str) -> str:
        """Load DOCX file and extract text."""
        try:
            from docx import Document
        except ImportError:
            raise ImportError(
                "DOCX support requires python-docx. Run: pip install python-docx"
            )
        doc = Document(path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)

    def load_url(self, url: str) -> str:
        """Fetch text content from a URL."""
        try:
            import requests
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")
            if "json" in content_type:
                return json.dumps(resp.json(), indent=2, ensure_ascii=False)
            return resp.text
        except ImportError:
            raise ImportError(
                "URL loading requires requests. Run: pip install requests"
            )

    def load_multiple(self, sources: List[str]) -> str:
        """Load multiple sources and concatenate their content."""
        parts = []
        for source in sources:
            content = self.load(source)
            parts.append(f"[Source: {source}]\n{content}")
        return "\n\n---\n\n".join(parts)
