from pydantic import BaseModel
from typing import Optional

BILLING_PROMPT = """
You are a billing support agent.
- Explain charges clearly.
- Be polite and professional.
- Escalate if frustration is high.
"""


class BillingResponse(BaseModel):
    summary: str
    explanation: str
    invoice_id: Optional[str]
    next_steps: str
    escalation_recommended: bool
