from typing import Type
from pydantic import BaseModel
from app.prompts import billing, technical, account, feedback, general


def get_responder(intent: str) -> tuple[str, Type[BaseModel]]:
    if intent == "billing":
        return billing.BILLING_PROMPT, billing.BillingResponse
    if intent == "technical":
        return technical.TECHNICAL_PROMPT, technical.TechnicalResponse
    if intent == "account":
        return account.ACCOUNT_PROMPT, account.AccountResponse
    if intent == "feedback":
        return feedback.FEEDBACK_PROMPT, feedback.FeedbackResponse
    return general.GENERAL_PROMPT, general.GeneralResponse
