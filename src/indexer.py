import os

from src.chunker import parse_javascript
from src.file_scanner import scanRepository
from src.vector_store import store_chunks


def main():
    repository_path = os.getenv("SOURCE_REPOSITORY_PATH", ".")
    files = scanRepository(repository_path)
    chunks = []

    for file_path in files:
        if file_path.endswith(".js"):
            chunks.extend(parse_javascript(file_path))

    if not chunks:
        raise ValueError(f"No JavaScript chunks found in {repository_path!r}")

    store_chunks(chunks, replace=True)


if __name__ == "__main__":
    main()
