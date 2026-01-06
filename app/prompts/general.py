from pydantic import BaseModel

GENERAL_PROMPT = """
You are a general support agent.
- Answer politely, concise and friendly.
"""


class GeneralResponse(BaseModel):
    response: str
