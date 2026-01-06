from typing import List, cast
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from app.config import SYSTEM_PROMPTS, get_llm
from app.state import CustomerSupportState
from app.prompts.classifier import ClassificationResult, CLASSIFIER_PROMPT
from app.router import get_responder

llm = get_llm()


def classify_node(state: CustomerSupportState) -> dict:
    """Classify user intent and sentiment and determine escalation."""
    structured_llm = llm.with_structured_output(ClassificationResult)
    messages: List[BaseMessage] = [
        SystemMessage(content=CLASSIFIER_PROMPT),
        *state["messages"],
    ]

    result = structured_llm.invoke(messages)  # type: ignore

    # Safely extract attributes
    if hasattr(result, "dict"):
        result_dict = result.dict()
    else:
        result_dict = dict(result)

    # Default LLM output
    intent = result_dict.get("intent", "general")
    sentiment = result_dict.get("sentiment", "neutral")

    # ⚡ Custom escalation logic based on user message content
    user_text = state["messages"][-1].content.lower()  # last human message
    ESCALATION_KEYWORDS = [
        "unacceptable",
        "human now",
        "escalate immediately",
        "ridiculous",
        "not helping",
        "ceo",
        "manager",
        "supervisor",
        "complaint",
        "urgent",
        "cancel account",
        "refund",
        "quit company",
        "frustrated",
        "angry",
        "disappointed",
        "waiting forever",
    ]

    needs_escalation = any(word in user_text for word in ESCALATION_KEYWORDS)

    return {
        "intent": intent,
        "sentiment": sentiment,
        "needs_escalation": needs_escalation,
    }


def respond_node(state: CustomerSupportState) -> dict:
    """Generate AI response, preserving full conversation."""
    intent_str = state["intent"] or "general"
    prompt_text, _ = get_responder(intent_str)

    context = f"Intent: {state['intent']}\nSentiment: {state['sentiment']}"
    messages: List[BaseMessage] = [
        SystemMessage(content=SYSTEM_PROMPTS.responder),
        SystemMessage(content=context),
        *state["messages"],
    ]

    response = llm.invoke(messages)
    ai_message = AIMessage(content=response.content)
    if "messages" in state and isinstance(state["messages"], list):
        state["messages"].append(ai_message)

    return {"messages": [ai_message], "response_draft": response.content}


def escalate_node(state: CustomerSupportState) -> dict:
    """Generate escalation message if needed."""
    msg = "Connecting you with a human support agent."
    ai_message = AIMessage(content=msg)
    if "messages" in state and isinstance(state["messages"], list):
        state["messages"].append(ai_message)
    return {"messages": [ai_message], "response_draft": msg}


def route_after_classification(state: CustomerSupportState) -> str:
    return "escalate" if state["needs_escalation"] else "respond"


def build_support_agent() -> CompiledStateGraph:
    """Construct LangGraph agent with conversation memory."""
    graph = StateGraph(CustomerSupportState)
    graph.add_node("classify", classify_node)
    graph.add_node("respond", respond_node)
    graph.add_node("escalate", escalate_node)
    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify",
        route_after_classification,
        {"respond": "respond", "escalate": "escalate"},
    )
    graph.add_edge("respond", END)
    graph.add_edge("escalate", END)
    return graph.compile()


def run_support_agent(
    state: CustomerSupportState, customer_message: str, timeout: int = 30
) -> CustomerSupportState:
    """
    Run agent with message, preserving full conversation.

    Timeout added: if LLM does not respond in `timeout` seconds, fallback response is used.
    """
    from functools import partial

    # Append new user message
    state["messages"].append(HumanMessage(content=customer_message))
    agent = build_support_agent()

    def invoke_agent(s: CustomerSupportState) -> CustomerSupportState:
        return cast(CustomerSupportState, agent.invoke(s))

    final_state: CustomerSupportState

    # Run with thread timeout
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(partial(invoke_agent, state))
        try:
            final_state = future.result(timeout=timeout)
        except TimeoutError:
            # Fallback response on timeout
            fallback_msg = "Sorry, I'm taking too long to respond. Please try again."
            ai_message = AIMessage(content=fallback_msg)
            if "messages" in state and isinstance(state["messages"], list):
                state["messages"].append(ai_message)
            final_state = state.copy()
            final_state["response_draft"] = fallback_msg
            final_state["intent"] = "general"
            final_state["sentiment"] = "neutral"
            final_state["needs_escalation"] = False

    # Ensure TypedDict fields always exist
    final_state.setdefault("intent", "general")
    final_state.setdefault("sentiment", "neutral")
    final_state.setdefault("needs_escalation", False)
    final_state.setdefault("response_draft", "")

    return final_state
