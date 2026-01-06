# app/config.py
import os

# importing
from pydantic import Field
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

# Import all category prompts and structured output models
from app.prompts import billing, technical, account, feedback, general, classifier

load_dotenv()


def get_llm(model_name: str = "gpt-4o-mini", temperature: float = 0.3) -> ChatOpenAI:
    """
    Initialize ChatOpenAI for LangChain v1.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment.")

    return ChatOpenAI(model=model_name, temperature=temperature)


# =============================================================================
# SYSTEM PROMPTS PER CATEGORY
# =============================================================================


class SystemPrompts(BaseModel):
    classifier: str = classifier.CLASSIFIER_PROMPT
    billing: str = billing.BILLING_PROMPT
    technical: str = technical.TECHNICAL_PROMPT
    account: str = account.ACCOUNT_PROMPT
    feedback: str = feedback.FEEDBACK_PROMPT
    general: str = general.GENERAL_PROMPT
    responder: str = Field(
        default="""You are a helpful customer support agent.
Provide a warm, professional response based on the classified intent and sentiment.
Escalate if needed."""
    )


SYSTEM_PROMPTS = SystemPrompts()


# =============================================================================
# STRUCTURED OUTPUT PER CATEGORY
# =============================================================================

STRUCTURED_MODELS = {
    "classifier": classifier.ClassificationResult,
    "billing": billing.BillingResponse,
    "technical": technical.TechnicalResponse,
    "account": account.AccountResponse,
    "feedback": feedback.FeedbackResponse,
    "general": general.GeneralResponse,
}
