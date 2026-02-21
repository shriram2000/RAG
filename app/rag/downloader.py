from pathlib import Path
from urllib.parse import urlparse

import httpx

from app.config import settings


def download_url_to_folder(url: str) -> Path:
    response = httpx.get(url, follow_redirects=True, timeout=60)
    response.raise_for_status()

    parsed = urlparse(url)
    raw_name = Path(parsed.path).name or "downloaded_page"
    safe_name = raw_name.replace("/", "_")
    if "." not in safe_name:
        safe_name = f"{safe_name}.html"

    downloads_dir = Path(settings.downloads_dir)
    downloads_dir.mkdir(parents=True, exist_ok=True)
    destination = downloads_dir / safe_name
    destination.write_bytes(response.content)
    return destination
