from pydantic import BaseModel

CLASSIFIER_PROMPT = """
You are a strict classification system.

Classify the user's issue into:
- problem_type: billing | technical | account | general
- severity: low | medium | high
- needs_escalation: true if user is angry or requests human support

Return ONLY structured data.
"""


class ClassificationResult(BaseModel):
    problem_type: str
    severity: str
    needs_escalation: bool
