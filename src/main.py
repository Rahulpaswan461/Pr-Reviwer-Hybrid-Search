from src.vector_store import searchCode
from src.schema import review_json_schema
from src.validateSchema import ReviewResult
from src.failed_closed_result import fail_closed_result
from src.sanitizer import redact_secrets
import sys
import os
from src.reviewer import review_code
from src.github import post_pr_comment

def main():
    is_github_action = os.getenv("GITHUB_ACTIONS") == "true"

    if is_github_action:
        with open("pr.diff", "r", encoding="utf-8") as file:
            diff_text = file.read()
    else:
        diff_text = sys.stdin.read()

    if not diff_text:
        print("No diff text provided", file=sys.stderr)
        sys.exit(1)

    redacted_diff = redact_secrets(diff_text)
    limited_diff = redacted_diff[:4000]

    reference = searchCode(limited_diff)
    result = review_code(limited_diff, reference, review_json_schema)

    try:
        validated = ReviewResult.model_validate(result)
    except Exception as error:
        validated = ReviewResult.model_validate(fail_closed_result(error))

    if is_github_action:
        post_pr_comment(validated)
    else:
        print(validated)


if __name__ == "__main__":
    main()
