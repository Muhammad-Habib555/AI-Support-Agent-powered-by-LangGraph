from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class CustomerSupportState(TypedDict):
    messages: Annotated[list, add_messages]
    customer_id: str | None
    intent: str | None
    sentiment: str | None
    needs_escalation: bool
    response_draft: str | None


def create_initial_state(customer_id: str | None = None) -> CustomerSupportState:
    return CustomerSupportState(
        messages=[],
        customer_id=customer_id,
        intent=None,
        sentiment=None,
        needs_escalation=False,
        response_draft=None,
    )
