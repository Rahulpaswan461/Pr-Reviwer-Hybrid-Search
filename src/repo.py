from src.repository import clone_repository
from src.file_scanner import scanRepository
from src.chunker import parse_javascript

# repo_url = "https://github.com/Rahulpaswan461/Pr-Reviwer-Agent"
# destination = "./repositories/test-repo"

def cloneRepositoryContent():
    repo_url = "https://github.com/Rahulpaswan461/Pr-Reviwer-Agent"
    destination = "./repositories/test-repo"

    clone_repository(repo_url,destination)
    files = scanRepository(destination)

    all_chunks = []

    for file in files:
        if file.endswith(".js"):
            chunk = parse_javascript(file)
            all_chunks.extend(chunk)

    return all_chunks