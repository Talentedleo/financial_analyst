# Financial Analyst AI Agent System

> Multi-agent system using Google ADK + LiteLLM + MiniMax for professional-grade stock analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-green.svg)](https://adk.dev/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-Proxy-orange.svg)](https://docs.litellm.ai/)
[![MiniMax](https://img.shields.io/badge/MiniMax-M2.1-red.svg)](https://www.minimax.io/)

---

## Official Examples Studied

### Google ADK Official Repository
**Repo:** https://github.com/google/adk-python

### Key Official Examples

| Example | Path | Purpose |
|---------|------|---------|
| Simple Agent | `adk-python/samples/agents/` | Basic agent with tools |
| Financial Advisor | `adk-samples/python/agents/financial-advisor/` | Domain-specific agent |
| Parallel Task | `adk-samples/python/agents/parallel_task_decomposition_execution/` | Multi-agent coordination |
| Hierarchical Workflow | `adk-samples/python/agents/hierarchical-workflow-automation/` | Complex multi-agent system |

---

## Architecture

```
User Input
    ↓
Google ADK (Plan Agent)
    ↓
LiteLlm (google.adk.models.lite_llm)
    ↓
MiniMax-M2.1 API
    ↓
FastAPI → JSON Response
```

---

## Quick Start (Official Pattern)

### 1. Install Dependencies

```bash
pip install google-adk litellm fastapi uvicorn pydantic
```

### 2. Create Agent (Official ADK Pattern)

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import Tool
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# Create LLM model (MiniMax via LiteLlm)
model = LiteLlm(
    model="minimax/MiniMax-M2.1",
    api_key=os.environ["MINIMAX_API_KEY"],
    api_base="https://api.minimax.io/v1"
)

# Create Agent
root_agent = Agent(
    name="financial_advisor",
    model=model,
    description="Financial analysis agent",
    instruction="You are a helpful financial assistant.",
)

# Create session service
session_service = InMemorySessionService()

# Create runner
runner = Runner(
    agent=root_agent,
    app_name="financial_analyst",
    session_service=session_service
)
```

### 3. Run Agent (Official Pattern)

```python
import asyncio
from google.genai import types

async def main():
    # Create user message
    content = types.Content(
        role="user",
        parts=[types.Part(text="Should I invest in Apple?")]
    )
    
    # Run agent
    async for event in runner.run(
        user_id="user_1",
        session_id="session_001",
        new_message=content
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)

asyncio.run(main())
```

---

## Multi-Agent Patterns (from Official Examples)

### Pattern 1: Sequential Sub-Agents

```python
from google.adk.agents import Agent
from google.adk.agents.sequential_agent import SequentialAgent

# Create sub-agents
research_agent = Agent(name="research", model=model, ...)
analysis_agent = Agent(name="analysis", model=model, ...)

# Create sequential agent
sequential_agent = SequentialAgent(
    name="financial_analysis_pipeline",
    model=model,
    description="Pipeline for financial analysis",
    sub_agents=[research_agent, analysis_agent]
)
```

### Pattern 2: Parallel Execution

```python
from google.adk.agents.parallel_agent import ParallelAgent

# Create parallel agents
buffett_agent = Agent(name="buffett", model=model, ...)
wood_agent = Agent(name="wood", model=model, ...)

parallel_agent = ParallelAgent(
    name="multi_perspective_analysis",
    model=model,
    sub_agents=[buffett_agent, wood_agent]
)
```

### Pattern 3: Tool Integration

```python
from google.adk.tools import Tool

def search_web(query: str) -> str:
    """Search the web for financial information"""
    # Implementation
    return results

web_search_tool = Tool(
    name="web_search",
    description="Search for financial news and data",
    method=search_web
)

agent = Agent(
    name="financial_advisor",
    model=model,
    tools=[web_search_tool]
)
```

---

## Our Implementation Plan

### Phase 1: Core Agents

```
Plan Agent (Root)
    ↓
├── Web Search Agent → Financial data search
└── Financial Master Agent
    ├── Buffett Analysis
    ├── Cathie Wood Analysis
    └── Greg Abel Analysis
```

### Phase 2: Tools

- Web search tool
- Stock data tool
- News tool

### Phase 3: Integration

- Celebrity Skills loaded as context
- Multi-perspective analysis
- FastAPI endpoints

---

## Project Structure

```
financial_analyst/
├── agents/
│   ├── __init__.py
│   ├── plan_agent.py        # Root coordinator
│   ├── web_search_agent.py # Search sub-agent
│   └── financial_master.py # Expert sub-agent
├── skills/                  # Celebrity Skills
│   ├── buffett/
│   ├── cathie_wood/
│   └── greg_abel/
├── tools/
│   └── search_tool.py      # Custom tools
├── api/
│   └── main.py             # FastAPI
├── models/
│   └── schemas.py
├── services/
│   └── llm_service.py      # LLM service
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

- [Google ADK GitHub](https://github.com/google/adk-python)
- [ADK Samples](https://github.com/google/adk-samples)
- [LiteLLM](https://docs.litellm.ai/)
- [MiniMax API](https://www.minimax.io/)

---

## License

MIT License

Copyright (c) 2026 [Leo Li](https://github.com/Talentedleo)

MIT License © [Leo Li](https://github.com/Talentedleo)

---

## Data Source: Finnhub API

We use **Finnhub API** for real-time stock data and financial news.

### Finnhub Features

| Endpoint | Description |
|----------|-------------|
| `/quote` | Real-time stock quote (price, volume, etc.) |
| `/company-news` | Company-specific news |
| `/general-news` | General market news |
| `/stock/candle` | OHLCV candlestick data |
| `/stock/profile2` | Company profile and fundamentals |
| `/earnings` | Earnings data |

### Finnhub Python SDK

```python
import finnhub

# Initialize client
finnhub_client = finnhub.Client(api_key=os.environ["FINNHUB_API_KEY"])

# Get real-time quote
quote = finnhub_client.quote('AAPL')
print(f"Apple price: ${quote['c']}")
print(f"Change: {quote['dp']}%")

# Get company news
news = finnhub_client.company_news('AAPL', _from="2026-01-01", to="2026-04-11")
for article in news:
    print(f"{article['headline']}")

# Get company profile
profile = finnhub_client.profile2(symbol='AAPL')
print(f"Industry: {profile['finnhubIndustry']}")
```

### Install Finnhub SDK

```bash
pip install finnhub-python
```

### Environment Variable

```bash
export FINNHUB_API_KEY="your-finnhub-api-key"
```

---

## Tool Integration Architecture

```
Agent Tools
    ↓
┌─────────────────────────────┐
│     Finnhub API Client      │
├─────────────────────────────┤
│ • Stock quotes              │
│ • Company news              │
│ • Market news              │
│ • Company fundamentals      │
│ • Earnings data            │
└─────────────────────────────┘
    ↓
Returns structured data
```

---

## Updated Project Structure

```
financial_analyst/
├── agents/
│   ├── __init__.py
│   ├── plan_agent.py           # Root coordinator
│   ├── web_search_agent.py    # Web search
│   └── financial_master.py      # Expert sub-agent
├── skills/                     # Celebrity Skills
├── tools/
│   ├── __init__.py
│   └── finnhub_tools.py       # Finnhub API tools
├── api/
│   └── main.py                # FastAPI
├── services/
│   └── data_service.py        # Data aggregation
├── requirements.txt
└── main.py
```
