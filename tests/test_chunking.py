from app.rag.chunking import chunk_text


def test_chunk_text_splits_long_text() -> None:
    text = "A" * 2500
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    assert len(chunks) > 1
    assert all(len(c) <= 500 for c in chunks)


def test_chunk_text_handles_empty() -> None:
    assert chunk_text("   ") == []
