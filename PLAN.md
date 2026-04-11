# Financial Analyst AI Agent System

> Multi-agent system using Google ADK for professional-grade stock analysis

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

## Agent Design

### 1. Plan Agent (Root Agent)

**Role:** Analyzes user question, decides which agents to call

**Capabilities:**
- Parse user intent (investment advice, stock analysis, philosophy question)
- Route to appropriate sub-agents
- Synthesize final response

**Tools:**
- `web_search_agent` - for real-time information
- `financial_master_agent` - for expert analysis

---

### 2. Web Search Agent

**Role:** Search real-time financial information

**Capabilities:**
- Search stocks, financial news
- Get current prices
- Find analyst reports

**Tools:**
- Google search
- Financial news APIs
- Stock data APIs

---

### 3. Financial Master Agent (Multi-Skill Agent)

**Role:** Provide expert-level financial analysis using celebrity skills

**Skills Loaded:**
- `warren_buffett_skill` - Value investing, moat analysis
- `cathie_wood_skill` - Disruptive innovation, growth investing
- `greg_abel_skill` - Operational excellence, Berkshire perspective

**Capabilities:**
- Analyze stocks using Buffett moat framework
- Evaluate growth/innovation plays
- Answer investment philosophy questions
- Provide multi-perspective analysis

---

## Project Structure

```
financial_analyst/
├── agents/
│   ├── __init__.py
│   ├── plan_agent.py          # Root coordinator
│   ├── web_search_agent.py   # Search agent
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
│   └── adk_service.py        # ADK initialization
├── tests/
├── requirements.txt
└── main.py                   # Entry point
```

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

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | Google ADK |
| LLM | Gemini (via ADK) |
| API | FastAPI |
| Skills | Celebrity Skills (Markdown) |
| Deployment | Docker (optional) |

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

## Key Questions to Resolve

1. **Which ADK version?** (ADK vs legacy LangChain)
2. **Gemini API key** - Need to configure
3. **Skill format** - Convert Celebrity Skills to ADK tool format?
4. **Search provider** - Brave Search, SerpAPI, or built-in?

---

## Next Steps

1. Confirm architecture
2. Setup development environment
3. Implement Phase 1

