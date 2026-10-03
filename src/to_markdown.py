def to_markdown(review_result):

    verdict = review_result["verdict"]
    summary = review_result["summary"]
    findings = review_result.get("findings")

    output = "## AI PR REVIEW\n\n"
    output += f"**Verdict:** {verdict}\n\n"
    output += f"**Summary:** {summary}\n\n"

    if not findings:
        output += "No findings were reported.\n"
        return output

    output += "### Findings\n\n"

    for finding in findings:
        output += f"- **{finding['title']}**\n"
        output += f"  - Severity: {finding['severity']}\n"
        output += f"  - File: {finding['file_path']}\n"
        output += f"  - Line: {finding['line_number']}\n"
        output += f"  - Summary: {finding['summary']}\n"
        output += f"  - Evidence: {finding['evidence']}\n"
        output += f"  - Recommendation: {finding['recommendations']}\n\n"

    return output