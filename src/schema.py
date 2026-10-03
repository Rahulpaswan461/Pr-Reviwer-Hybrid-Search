review_json_schema = {
    "type": "object",
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["pass", "warn", "fail"]
        },
        "summary": {
            "type": "string"
        },
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string"
                    },
                    "title": {
                        "type": "string"
                    },
                    "severity": {
                        "type": "string",
                        "enum": [
                            "none",
                            "low",
                            "medium",
                            "high",
                            "critical"
                        ],
                        "description": (
                            "The severity level of the security or code issue"
                        )
                    },
                    "summary": {
                        "type": "string"
                    },
                    "file_path": {
                        "type": "string"
                    },
                    "line_number": {
                        "type": "number"
                    },
                    "evidence": {
                        "type": "string"
                    },
                    "recommendations": {
                        "type": "string"
                    }
                },
                "required": [
                    "id",
                    "title",
                    "severity",
                    "summary",
                    "file_path",
                    "line_number",
                    "evidence",
                    "recommendations"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": [
        "verdict",
        "summary",
        "findings"
    ],
    "additionalProperties": False
}