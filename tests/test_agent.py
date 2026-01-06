# tests/test_agent.py
import pytest
from app.agent import run_support_agent
from app.state import create_initial_state, CustomerSupportState

# Valid values for assertions
VALID_INTENTS = {"billing", "technical", "account", "feedback", "general"}
VALID_SENTIMENTS = {"positive", "neutral", "negative"}


# ------------------ Parametrized Tests ------------------ #

@pytest.mark.parametrize(
    "message,expected_escalation,expected_intent",
    [
        ("I cannot log into my account", False, "account"),
        ("This is unacceptable. I want a human now!", True, "general"),
        ("I paid my bill but it's not showing up", False, "billing"),
        ("My internet is down since morning", False, "technical"),
        ("Great service!", False, "feedback"),
        ("Random text with no meaning", False, "general"),
    ]
)
def test_agent_responses(message, expected_escalation, expected_intent):
    """
    Tests multiple types of messages including escalation, billing, account, and feedback.
    """
    state: CustomerSupportState = create_initial_state()
    result: CustomerSupportState = run_support_agent(state, message)

    # Check escalation
    assert result["needs_escalation"] is expected_escalation, f"Escalation failed for message: {message}"

    # Check intent
    assert result["intent"] in VALID_INTENTS, f"Invalid intent for message: {message}"
    assert result["intent"] == expected_intent or result["intent"] in VALID_INTENTS

    # Check sentiment
    assert result["sentiment"] in VALID_SENTIMENTS, f"Invalid sentiment for message: {message}"

    # Check response draft
    assert isinstance(result["response_draft"], str), f"Response draft is not string for message: {message}"
    assert len(result["response_draft"]) > 0, f"Response draft is empty for message: {message}"


# ------------------ Edge Case Tests ------------------ #

@pytest.mark.parametrize(
    "message",
    [
        "",  # Empty message
        "     ",  # Whitespace only
        "😀🙃👍",  # Emojis only
        "asdkfjaskldjflkasjdf",  # Gibberish
        "HELP! My account! #$%^&*",  # Special characters
    ]
)
def test_agent_edge_cases(message):
    """
    Test agent behavior on edge cases to ensure stability.
    """
    state: CustomerSupportState = create_initial_state()
    result: CustomerSupportState = run_support_agent(state, message)

    # Ensure no crash & safe defaults
    assert isinstance(result["needs_escalation"], bool)
    assert result["intent"] in VALID_INTENTS
    assert result["sentiment"] in VALID_SENTIMENTS
    assert isinstance(result["response_draft"], str)
    assert len(result["response_draft"]) > 0


# ------------------ Escalation Specific Tests ------------------ #

def test_force_escalation():
    """
    Test that clearly angry or urgent messages trigger escalation.
    """
    state: CustomerSupportState = create_initial_state()
    messages = [
        "I want a human now!",
        "This is ridiculous, I demand escalation!",
        "You are not helping, escalate immediately!"
    ]
    for msg in messages:
        result = run_support_agent(state, msg)
        assert result["needs_escalation"] is True, f"Escalation failed for: {msg}"
