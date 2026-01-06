from pydantic import BaseModel
from typing import List, Optional

TECHNICAL_PROMPT = """
You are a technical support agent.
- Provide clear troubleshooting steps.
- Ask clarifying questions if needed.
- Escalate if severity is high.
"""


class TechnicalResponse(BaseModel):
    issue_summary: str
    possible_cause: Optional[str]
    troubleshooting_steps: List[str]
    escalation_recommended: bool
