# Financial Analyst AI Agent System

> Multi-agent system using Google ADK for professional-grade stock analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

The Financial Analyst AI Agent System is an intelligent, multi-expert autonomous platform designed to deliver professional-grade stock analysis on demand. When a user requests an analysis of any stock, the system instantly triggers a fully automated workflow.

---

## System Architecture

```
User Input
    ↓
Plan Agent (Coordinator)
    ↓
├── Web Search Agent ─→ Search financial news, data, analysis
└── Financial Master Agent
    ├── Warren Buffett Skill
    ├── Cathie Wood Skill
    └── Greg Abel Skill
    ↓
FastAPI → JSON Response
```

---

## Agents

### 1. Plan Agent (Root Agent)

**Role:** Analyzes user question, decides which agents to call

**Capabilities:**
- Parse user intent (investment advice, stock analysis, philosophy question)
- Route to appropriate sub-agents
- Synthesize final response

---

### 2. Web Search Agent

**Role:** Search real-time financial information

**Capabilities:**
- Search stocks, financial news
- Get current prices
- Find analyst reports

---

### 3. Financial Master Agent (Multi-Skill Agent)

**Role:** Provide expert-level financial analysis using celebrity skills

**Skills Loaded:**
- `warren_buffett_skill` - Value investing, moat analysis
- `cathie_wood_skill` - Disruptive innovation, growth investing
- `greg_abel_skill` - Operational excellence, Berkshire perspective

---

## API Endpoints (FastAPI)

### POST /analyze

Analyze a stock or investment question

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

Real-time web search

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
│   ├── __init__.py
│   ├── buffett/
│   │   └── SKILL.md
│   ├── cathie_wood/
│   │   └── SKILL.md
│   └── greg_abel/
│       └── SKILL.md
├── api/
│   └── main.py                # FastAPI endpoints
├── models/
│   └── schemas.py             # Pydantic models
├── services/
│   └── adk_service.py         # ADK initialization
├── tests/
├── requirements.txt
└── main.py                    # Entry point
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | Google ADK |
| LLM | Gemini (via ADK) |
| API | FastAPI |
| Skills | Celebrity Skills (Markdown) |
| Deployment | Docker (optional) |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Google ADK
- Gemini API key

### Installation

```bash
# Clone the repository
git clone https://github.com/Talentedleo/financial_analyst.git
cd financial_analyst

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GEMINI_API_KEY="your-api-key"
```

### Run the API

```bash
uvicorn api.main:app --reload --port 8000
```

### Run Tests

```bash
pytest tests/
```

---

## Development Phases

### Phase 1: Core Setup
- [ ] Initialize ADK project
- [ ] Create base agents
- [ ] Setup FastAPI skeleton
- [ ] Connect agents to API

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

This project uses the [Celebrity Skills](https://github.com/Talentedleo/celebrity_skills) framework:

| Skill | Description |
|-------|-------------|
| Warren Buffett | Value investing, moat analysis, long-term thinking |
| Cathie Wood | Disruptive innovation, growth investing, Big Ideas |
| Greg Abel | Operational excellence, Berkshire culture, capital allocation |

---

## License

MIT License

Copyright (c) 2026 [Leo Li](https://github.com/Talentedleo)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

MIT License © [Leo Li](https://github.com/Talentedleo)
