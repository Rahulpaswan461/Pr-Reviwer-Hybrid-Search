def fail_closed_result(error):

    return {
        "verdict": "fail",
        "summary": (
            "The AI review response failed validation, so the system "
            "returned a fail-closed result."
        ),
        "findings": [
            {
                "id": "validation-error",
                "title": "Response validation failed",
                "severity": "high",
                "summary": "The model output did not match the required schema.",
                "file_path": "N/A",
                "line_number": 0,
                "evidence": str(error),
                "recommendations": (
                    "Review the model output, check the schema, and retry "
                    "only after fixing the contract mismatch."
                ),
            }
        ],
    }