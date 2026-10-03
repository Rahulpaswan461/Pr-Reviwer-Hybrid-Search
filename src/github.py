import os

import requests

from src.to_markdown import to_markdown


def post_pr_comment(review_result):
    token = os.getenv("GH_ACCESS_TOKEN")
    repo = os.getenv("REPO")
    pr_number = os.getenv("PR_NUMBER")

    if not token or not repo or not pr_number:
        raise ValueError("Missing GH_ACCESS_TOKEN, REPO or PR_NUMBER")

    owner, repo_name = repo.split("/", maxsplit=1)
    body = to_markdown(review_result)
    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo_name}/issues/{pr_number}/comments"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.post(url, headers=headers, json={"body": body})
    response.raise_for_status()

    print("PR comment posted successfully")
