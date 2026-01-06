from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.state import CustomerSupportState, create_initial_state
from app.agent import run_support_agent
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="AI Support Agent API")

# Global session state to remember conversation
session: CustomerSupportState = create_initial_state()


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


@app.post("/support")
def support_endpoint(req: ChatRequest):
    global session
    if not req.messages:
        return {"conversation": [], "final_response": ""}

    # Use the last user message
    last_msg: str = req.messages[-1].content

    # Run agent with full session memory
    session = run_support_agent(session, last_msg)  # type: ignore

    # Build conversation for frontend
    conversation: List[dict[str, str]] = [{"role": "user", "content": last_msg}]
    if session.get("messages"):
        for msg in session["messages"]:
            if isinstance(msg, AIMessage):
                conversation.append({"role": "assistant", "content": str(msg.content)})
            elif isinstance(msg, HumanMessage):
                conversation.append({"role": "user", "content": str(msg.content)})

    # Ensure response_draft is string
    response_text: str = str(session.get("response_draft") or "")

    return {
        "conversation": conversation,
        "final_response": response_text,
        "intent": session.get("intent"),
        "sentiment": session.get("sentiment"),
        "needs_escalation": session.get("needs_escalation"),
    }


@app.post("/reset")
def reset_chat():
    global session
    session = create_initial_state()
    return {"status": "new chat started"}
