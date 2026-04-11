# Financial Analyst AI Agent System

> Multi-agent system using Google ADK + LiteLLM + MiniMax for professional-grade stock analysis

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
Plan Agent (Google ADK)
    ↓
├── Web Search Agent ─→ Search financial news, data
└── Financial Master Agent
    ├── Warren Buffett Skill
    ├── Cathie Wood Skill
    └── Greg Abel Skill
    ↓
LiteLLM Proxy (MiniMax-M2.1)
    ↓
FastAPI → JSON Response
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | Google ADK |
| LLM Provider | MiniMax (via LiteLLM) |
| Model | MiniMax-M2.1 |
| API | FastAPI |
| Skills | Celebrity Skills (Markdown) |

---

## Quick Start

### Prerequisites

- Python 3.10+
- MiniMax API Key
- LiteLLM Proxy

### 1. Install Dependencies

```bash
pip install google-adk litellm fastapi uvicorn pydantic
```

### 2. Configure LiteLLM Proxy with MiniMax

Create `config.yaml`:

```yaml
model_list:
  - model_name: minimax/MiniMax-M2.1
    litellm_params:
      model: minimax/MiniMax-M2.1
      api_key: os.environ/MINIMAX_API_KEY
      api_base: https://api.minimax.io/v1

litellm_settings:
  drop_params: true
  set_verbose: true
```

Start the proxy:

```bash
litellm --config config.yaml --port 4000
```

### 3. Set Environment Variables

```bash
export MINIMAX_API_KEY="your-minimax-api-key"
export ADK_LITEllM_BASE_URL="http://localhost:4000"
```

### 4. Run the API

```bash
uvicorn api.main:app --reload --port 8000
```

---

## MiniMax Models via LiteLLM

LiteLLM provides unified access to MiniMax models through OpenAI/Anthropic-compatible APIs.

### Supported Models

| Model | Description | Input Cost | Output Cost |
|-------|-------------|------------|-------------|
| MiniMax-M2.1 | Powerful multi-language, enhanced programming | $0.3/1M tokens | $1.2/1M tokens |
| MiniMax-M2.1-lightning | Faster, ~100 tps | $0.3/1M tokens | $2.4/1M tokens |
| MiniMax-M2Agent | Agentic, advanced reasoning | $0.3/1M tokens | $1.2/1M tokens |

### Basic Usage with LiteLLM SDK

```python
import litellm

# Set environment variables
os.environ["MINIMAX_API_KEY"] = "your-minimax-api-key"
os.environ["MINIMAX_API_BASE"] = "https://api.minimax.io/v1"

# Simple completion
response = litellm.completion(
    model="minimax/MiniMax-M2.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
)
print(response.choices[0].message.content)
```

### With Tool Calling

```python
import litellm

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"]
            }
        }
    }
]

response = litellm.completion(
    model="minimax/MiniMax-M2.1",
    messages=[{"role": "user", "content": "What's the weather in SF?"}],
    tools=tools
)
```

### With Reasoning Split

```python
response = litellm.completion(
    model="minimax/MiniMax-M2.1",
    messages=[{"role": "user", "content": "Solve: 2+2=?"}],
    extra_body={"reasoning_split": True}
)

# Access thinking and response separately
if hasattr(response.choices[0].message, 'reasoning_details'):
    print(f"Thinking: {response.choices[0].message.reasoning_details}")
print(f"Response: {response.choices[0].message.content}")
```

---

## Google ADK Agent Structure

### Agent Definition

```python
from google.adk.agents import Agent
from google.adk.tools import Tool

# Define your agent
root_agent = Agent(
    name="plan_agent",
    model="minimax/MiniMax-M2.1",  # Via LiteLLM
    description="Analyzes user questions and routes to sub-agents",
    instruction="You are a financial analysis coordinator...",
    tools=[web_search_tool, financial_master_tool]
)
```

### Tool Definition

```python
from google.adk.tools import Tool

web_search_tool = Tool(
    name="web_search",
    description="Search for financial news and data",
    handler=web_search_handler  # Your custom handler
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

### GET /health

System health check

---

## Project Structure

```
financial_analyst/
├── agents/
│   ├── __init__.py
│   ├── plan_agent.py          # Root coordinator
│   ├── web_search_agent.py    # Search agent
│   └── financial_master.py    # Expert agent with skills
├── skills/
│   ├── buffett/
│   ├── cathie_wood/
│   └── greg_abel/
├── api/
│   └── main.py                # FastAPI endpoints
├── models/
│   └── schemas.py             # Pydantic models
├── services/
│   └── adk_service.py         # ADK + LiteLLM setup
├── config.yaml                 # LiteLLM Proxy config
├── requirements.txt
└── main.py
```

---

## Development Phases

### Phase 1: Core Setup ✅
- [x] System architecture defined
- [ ] Initialize ADK project
- [ ] Configure LiteLLM + MiniMax
- [ ] Setup FastAPI skeleton

### Phase 2: Skills Integration
- [ ] Load Buffett skill
- [ ] Load Cathie Wood skill
- [ ] Load Greg Abel skill
- [ ] Test skill-based responses

### Phase 3: Web Search
- [ ] Implement web search agent
- [ ] Integrate real-time data
- [ ] Connect to analysis pipeline

### Phase 4: Polish
- [ ] Error handling
- [ ] Response formatting
- [ ] Testing
- [ ] Documentation

---

## Celebrity Skills

This project uses [Celebrity Skills](https://github.com/Talentedleo/celebrity_skills):

| Skill | Description |
|-------|-------------|
| Warren Buffett | Value investing, moat analysis, long-term thinking |
| Cathie Wood | Disruptive innovation, growth investing, Big Ideas |
| Greg Abel | Operational excellence, Berkshire culture, capital allocation |

---

## References

- [Google ADK](https://adk.dev/)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [MiniMax API](https://www.minimax.io/)

---

## License

MIT License

Copyright (c) 2026 [Leo Li](https://github.com/Talentedleo)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

MIT License © [Leo Li](https://github.com/Talentedleo)
