from pydantic import BaseModel

ACCOUNT_PROMPT = """
You are an account support agent.
- Never ask passwords.
- Explain verification steps clearly.
- Escalate if access is blocked.
"""


class AccountResponse(BaseModel):
    issue_summary: str
    resolution_steps: str
    escalation_recommended: bool
