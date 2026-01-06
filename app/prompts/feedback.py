from pydantic import BaseModel

FEEDBACK_PROMPT = """
You are a feedback agent.
- Thank user for positive feedback.
- Acknowledge and empathize for negative feedback.
- Record suggestions.
"""


class FeedbackResponse(BaseModel):
    response: str
    escalate: bool
