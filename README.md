# Financial Analyst AI Agent System

> Multi-agent system using Google ADK + LiteLLM (proxy to MiniMax) for professional-grade stock analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-green.svg)](https://adk.dev/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-Proxy-orange.svg)](https://docs.litellm.ai/)
[![MiniMax](https://img.shields.io/badge/MiniMax-M2.1-red.svg)](https://www.minimax.io/)

---

## Overview

The Financial Analyst AI Agent System is an intelligent, multi-expert autonomous platform designed to deliver professional-grade stock analysis on demand. When a user requests an analysis of any stock, the system instantly triggers a fully automated workflow.

---

## Architecture

```
User Input
    ↓
Google ADK (Plan Agent)
    ↓
LiteLLM Proxy (Unified API)
    ↓
MiniMax-M2.1 Model
    ↓
FastAPI → JSON Response
```

**Note:** Google ADK does NOT support MiniMax directly. All LLM calls must go through **LiteLLM Proxy**, which provides OpenAI-compatible endpoints to connect to MiniMax.

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Agent Framework | Google ADK | Multi-agent orchestration |
| LLM Proxy | LiteLLM | Unified API gateway |
| LLM Provider | MiniMax | Language model (MiniMax-M2.1) |
| API | FastAPI | REST endpoints |

---

## Why LiteLLM?

Google ADK only supports these LLM providers natively:
- Gemini (Google)
- Claude (Anthropic)
- OpenAI

**MiniMax is NOT directly supported.** Therefore, we use **LiteLLM Proxy** to bridge Google ADK → OpenAI-compatible API → MiniMax.

### The Call Flow

```
Google ADK
    ↓ (OpenAI-compatible format)
LiteLLM Proxy (localhost:4000)
    ↓ (translates to MiniMax API)
MiniMax API (api.minimax.io)
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- MiniMax API Key
- LiteLLM Proxy running

### 1. Install Dependencies

```bash
pip install google-adk litellm fastapi uvicorn pydantic
```

### 2. Configure LiteLLM Proxy

Create `config.yaml`:

```yaml
model_list:
  - model_name: minimax/MiniMax-M2.1
    litellm_params:
      model: minimax/MiniMax-M2.1
      api_key: os.environ/MINIMAX_API_KEY
      api_base: https://api.minimax.io/v1

general_settings:
  master_key: sk-1234
```

### 3. Start LiteLLM Proxy

```bash
export MINIMAX_API_KEY="your-minimax-api-key"
litellm --config config.yaml --port 4000
```

### 4. Set Environment Variables for Google ADK

```bash
export LITEllM_API_KEY="sk-1234"  # LiteLLM proxy key
export LITEllM_BASE_URL="http://localhost:4000"
```

### 5. Run the API

```bash
uvicorn api.main:app --reload --port 8000
```

---

## MiniMax Models via LiteLLM

### Supported Models

| Model | Description | Input | Output |
|-------|-------------|-------|--------|
| MiniMax-M2.1 | High performance, multi-language | $0.3/1M | $1.2/1M |
| MiniMax-M2.1-lightning | Fast, ~100 tps | $0.3/1M | $2.4/1M |
| MiniMax-M2Agent | Agentic, advanced reasoning | $0.3/1M | $1.2/1M |

### LiteLLM SDK Usage

```python
import litellm

# Point to LiteLLM proxy
os.environ["LITEllM_API_KEY"] = "sk-1234"
os.environ["LITEllM_BASE_URL"] = "http://localhost:4000"

# Use MiniMax through LiteLLM
response = litellm.completion(
    model="minimax/MiniMax-M2.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    api_key=os.environ["LITEllM_API_KEY"],
    base_url=os.environ["LITEllM_BASE_URL"]
)
```

### With Tool Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_stocks",
            "description": "Search for stock information",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "market": {"type": "string"}
                }
            }
        }
    }
]

response = litellm.completion(
    model="minimax/MiniMax-M2.1",
    messages=[{"role": "user", "content": "What's the P/E ratio of Apple?"}],
    tools=tools
)
```

---

## Google ADK Agent Structure

### Agent with LiteLLM

```python
from google.adk.agents import Agent

# Google ADK → LiteLLM Proxy → MiniMax
agent = Agent(
    name="plan_agent",
    model="minimax/MiniMax-M2.1",  # ADK sees this as OpenAI-compatible
    description="Financial analysis coordinator",
    instruction="You are a financial analysis coordinator...",
    # ADK will route through LiteLLM proxy
)
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

Response:
{
  "answer": "...",
  "sources": [...],
  "agent_used": "financial_master"
}
```

### POST /search

```json
Request:
{
  "query": "Tesla Q1 2026 earnings"
}

Response:
{
  "results": [...]
}
```

---

## Project Structure

```
financial_analyst/
├── agents/
│   ├── plan_agent.py          # Root coordinator (Google ADK)
│   ├── web_search_agent.py   # Search agent
│   └── financial_master.py    # Expert agent
├── skills/                    # Celebrity Skills
│   ├── buffett/
│   ├── cathie_wood/
│   └── greg_abel/
├── api/
│   └── main.py               # FastAPI endpoints
├── services/
│   └── llm_service.py        # LiteLLM + MiniMax service
├── config.yaml                # LiteLLM Proxy config
├── requirements.txt
└── main.py
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
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [MiniMax API](https://www.minimax.io/)

---

## License

MIT License

Copyright (c) 2026 [Leo Li](https://github.com/Talentedleo)

MIT License © [Leo Li](https://github.com/Talentedleo)
