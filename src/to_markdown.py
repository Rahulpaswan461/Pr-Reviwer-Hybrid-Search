def to_markdown(review_result):
    output = "## AI PR REVIEW\n\n"
    output += f"**Verdict:** {review_result.verdict}\n\n"
    output += f"**Summary:** {review_result.summary}\n\n"

    if not review_result.findings:
        output += "No findings were reported.\n"
        return output

    output += "### Findings\n\n"

    for finding in review_result.findings:
        output += f"- **{finding.title}**\n"
        output += f"  - Severity: {finding.severity}\n"
        output += f"  - File: {finding.file_path}\n"
        output += f"  - Line: {finding.line_number}\n"
        output += f"  - Summary: {finding.summary}\n"
        output += f"  - Evidence: {finding.evidence}\n"
        output += f"  - Recommendation: {finding.recommendations}\n\n"

    return output