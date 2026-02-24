from pathlib import Path

from docling.document_converter import DocumentConverter


class DocumentParser:
    def __init__(self) -> None:
        self.converter = DocumentConverter()

    def parse(self, file_path: str) -> str:
        result = self.converter.convert(file_path)
        document = result.document
        return document.export_to_markdown()

    def parse_with_artifacts(self, file_path: str) -> tuple[str, list[str]]:
        text = self.parse(file_path)
        artifacts = self._find_local_images(text, Path(file_path).parent)
        return text, artifacts

    @staticmethod
    def _find_local_images(markdown: str, base_dir: Path) -> list[str]:
        images: list[str] = []
        for line in markdown.splitlines():
            if "![](" in line:
                maybe = line.split("![](", 1)[1].split(")", 1)[0]
                candidate = (base_dir / maybe).resolve()
                if candidate.exists():
                    images.append(str(candidate))
        return images
