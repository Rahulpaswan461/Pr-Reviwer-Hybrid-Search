from pydantic import BaseModel
from typing import Literal


class Finding(BaseModel):
    id: str
    title: str
    severity: Literal[
        "none",
        "low",
        "medium",
        "high",
        "critical"
    ]
    summary: str
    file_path: str
    line_number: float
    evidence: str
    recommendations: str


class ReviewResult(BaseModel):
    verdict: Literal["pass", "warn", "fail"]
    summary: str
    findings: list[Finding]