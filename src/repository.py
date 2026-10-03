from git import Repo

def clone_repository(repo_url,destination):
    Repo.clone_from(repo_url,destination)
    print(f"Repository cloned to {destination}")

