🧠 AI Support Agent

Structured Output · LangGraph · FastAPI · Streamlit

A production-grade AI support agent built using LangGraph for stateful orchestration, strict structured outputs with Pydantic, and a clean frontend–backend architecture.

This project demonstrates how to design deterministic, testable, and modular AI agents suitable for real-world systems.

✨ Features

✅ LangGraph-based stateful agent orchestration

✅ Strict structured outputs using Pydantic schemas

✅ Deterministic intent & severity classification

✅ Modular prompt-as-logic design

✅ Clean separation of state, logic, prompts, and transport layers

✅ FastAPI backend

✅ Streamlit frontend

✅ Pytest + Ruff enabled (production-ready quality)

🏗️ Architecture Overview
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ▼
LangGraph Agent
 │
 ├── Typed State (Pydantic)
 ├── Intent / Severity Classifier
 ├── Domain Routers
 ├── Prompt Modules
 └── Structured Response

📁 Project Structure

customer_agent/
├── app/
│   ├── agent.py        # LangGraph orchestration logic
│   ├── state.py        # Typed agent state (Pydantic)
│   ├── config.py       # LLM config & system prompts
│   ├── router.py       # Intent / domain routing
│   │
│   ├── prompts/        # Modular prompt logic
│   │   ├── classifier.py   # Intent & severity classification
│   │   ├── account.py      # Account-related responses
│   │   ├── billing.py      # Billing support logic
│   │   ├── technical.py    # Technical issue handling
│   │   ├── feedback.py     # Feedback & sentiment handling
│   │   └── general.py      # General inquiries
│   │
│   └── __init__.py
│
├── backend.py          # FastAPI API layer
├── frontend.py         # Streamlit UI
├── tests/              # Pytest test suite
│   ├── test_agent.py
│   ├── test_state.py
│   ├── test_backend.py
│   ├── test_prompts.py
│   └── conftest.py
│
├── pyproject.toml      # Tooling configuration
├── requirements.txt
├── .gitignore
└── README.md
