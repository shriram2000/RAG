from pathlib import Path

import app.rag.downloader as downloader


class DummyResponse:
    def __init__(self, content: bytes) -> None:
        self.content = content

    def raise_for_status(self) -> None:
        return None


def test_download_url_to_folder_saves_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(downloader.settings, "downloads_dir", str(tmp_path))
    monkeypatch.setattr(downloader.httpx, "get", lambda *args, **kwargs: DummyResponse(b"ok"))

    destination = downloader.download_url_to_folder("https://example.com/docs")

    assert destination.exists()
    assert destination.parent == Path(tmp_path)
    assert destination.read_bytes() == b"ok"
