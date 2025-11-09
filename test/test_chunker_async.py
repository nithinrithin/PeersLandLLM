import pytest
import asyncio
from src.processing.chunker import chunk_code_async

@pytest.mark.asyncio
async def test_single_file_chunking():
    files = [{
        "path": "test.py",
        "content": "def foo():\n    return 'bar'\n\n" * 20  # ~500 characters
    }]
    chunks = await chunk_code_async(files, chunk_size=100, chunk_overlap=20)

    assert isinstance(chunks, list)
    assert all("page_content" in c and "path" in c for c in chunks)
    assert all(c["path"] == "test.py" for c in chunks)
    assert len(chunks) > 1  # Should split into multiple chunks

@pytest.mark.asyncio
async def test_multiple_files_chunking():
    files = [
        {"path": "a.py", "content": "print('A')\n" * 50},
        {"path": "b.py", "content": "print('B')\n" * 50}
    ]
    chunks = await chunk_code_async(files, chunk_size=100, chunk_overlap=10)

    paths = set(c["path"] for c in chunks)
    assert paths == {"a.py", "b.py"}
    assert len(chunks) > 2

@pytest.mark.asyncio
async def test_overlap_behavior():
    files = [{
        "path": "overlap.py",
        "content": "x = 1\n" * 100  # ~600+ characters
    }]
    chunks = await chunk_code_async(files, chunk_size=100, chunk_overlap=50)

    assert len(chunks) > 1
    # Check that overlap is present
    first = chunks[0]["page_content"]
    second = chunks[1]["page_content"]
    assert any(line in first for line in second.splitlines())

@pytest.mark.asyncio
async def test_empty_file():
    files = [{"path": "empty.py", "content": ""}]
    chunks = await chunk_code_async(files)
    assert len(chunks) == 0
