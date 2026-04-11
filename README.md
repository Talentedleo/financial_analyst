# Financial Analyst AI Agent System

> Multi-agent system using Google ADK + LiteLLM + MiniMax for professional-grade stock analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-green.svg)](https://adk.dev/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-Proxy-orange.svg)](https://docs.litellm.ai/)
[![MiniMax](https://img.shields.io/badge/MiniMax-M2.1-red.svg)](https://www.minimax.io/)

---

## Overview

The Financial Analyst AI Agent System is an intelligent, multi-expert autonomous platform for professional-grade stock analysis using Google ADK with MiniMax models.

---

## Architecture

```
User Input
    ↓
Google ADK Agent
    ↓
LiteLlm (from google.adk.models.lite_llm)
    ↓
MiniMax API (api.minimax.io)
    ↓
FastAPI → JSON Response
```

**Note:** Google ADK uses `google.adk.models.lite_llm.LiteLlm` to connect to MiniMax via OpenAI-compatible API.

---

## Quick Start

### 1. Install Dependencies

```bash
pip install google-adk litellm fastapi uvicorn pydantic
```

### 2. Configure Environment

```bash
export MINIMAX_API_KEY="your-minimax-api-key"
```

### 3. Create Agent with MiniMax

```python
import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Create LiteLlm model (connects to MiniMax)
model = LiteLlm(
    model="minimax/MiniMax-M2.1",
    api_key=os.environ["MINIMAX_API_KEY"],
    api_base="https://api.minimax.io/v1"
)

# Create Agent
agent = Agent(
    name="plan_agent",
    model=model,
    instruction="You are a financial analysis coordinator...",
    description="Analyzes user questions and routes to sub-agents"
)

# Create session service
session_service = InMemorySessionService()

# Create runner
runner = Runner(
    agent=agent,
    app_name="financial_analyst",
    session_service=session_service
)
```

### 4. Run Agent

```python
import asyncio

async def run_agent(query: str):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    async for event in runner.run_async(
        user_id="user_1",
        session_id="session_001",
        new_message=content
    ):
        if event.is_final_response():
            return event.content.parts[0].text
    
asyncio.run(run_agent("Should I invest in Tesla?"))
```

---

## ADK + LiteLLM + MiniMax Integration

### The Key Connection

Google ADK provides native `LiteLlm` support:

```python
from google.adk.models.lite_llm import LiteLlm
```

This allows ADK to call **any OpenAI-compatible API** including MiniMax.

### Create Model

```python
model = LiteLlm(
    model="minimax/MiniMax-M2.1",  # Model name
    api_key=os.environ["MINIMAX_API_KEY"],
    api_base="https://api.minimax.io/v1"  # MiniMax API endpoint
)
```

### MiniMax Models Supported

| Model | Description | Input | Output |
|-------|-------------|-------|--------|
| minimax/MiniMax-M2.1 | High performance | $0.3/1M | $1.2/1M |
| minimax/MiniMax-M2.1-lightning | Fast, ~100 tps | $0.3/1M | $2.4/1M |
| minimax/MiniMax-M2Agent | Agentic, advanced reasoning | $0.3/1M | $1.2/1M |

---

## Multi-Agent Architecture

```
Plan Agent (Root)
    ↓
├── Web Search Agent → Search financial data
└── Financial Master Agent
    ├── Buffett Skill
    ├── Cathie Wood Skill
    └── Greg Abel Skill
```

### Plan Agent

```python
plan_agent = Agent(
    name="plan_agent",
    model=model,
    instruction="""You are a financial analysis coordinator.
    Analyze user questions and route to appropriate sub-agents.""",
    description="Coordinates analysis requests"
)
```

### Financial Master Agent

```python
financial_master = Agent(
    name="financial_master",
    model=model,
    instruction="""You are a financial expert using celebrity investment frameworks.
    Use Buffett, Cathie Wood, and Greg Abel perspectives.""",
    description="Provides expert financial analysis",
    sub_agents=[buffett_agent, wood_agent, abel_agent]
)
```

---

## Project Structure

```
financial_analyst/
├── agents/
│   ├── __init__.py
│   ├── plan_agent.py        # Root coordinator
│   ├── web_search_agent.py # Search sub-agent
│   └── financial_master.py  # Expert sub-agent
├── skills/
│   ├── buffett/
│   ├── cathie_wood/
│   └── greg_abel/
├── api/
│   └── main.py              # FastAPI endpoints
├── models/
│   └── schemas.py
├── requirements.txt
└── main.py
```

---

## API Endpoints

### POST /analyze

```json
Request:
{
  "question": "Should I invest in Tesla?",
  "style": "buffett" | "wood" | "abel" | "all"
}
```

### POST /search

```json
Request:
{
  "query": "Tesla Q1 2026 earnings"
}
```

---

## Celebrity Skills

This project uses [Celebrity Skills](https://github.com/Talentedleo/celebrity_skills):

| Skill | Description |
|-------|-------------|
| Warren Buffett | Value investing, moat analysis |
| Cathie Wood | Disruptive innovation, growth investing |
| Greg Abel | Operational excellence, Berkshire perspective |

---

## References

- [Google ADK](https://adk.dev/)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [LiteLLM](https://docs.litellm.ai/)
- [MiniMax API](https://www.minimax.io/)

---

## License

MIT License

Copyright (c) 2026 [Leo Li](https://github.com/Talentedleo)

MIT License © [Leo Li](https://github.com/Talentedleo)
