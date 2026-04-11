# Financial Analyst AI Agent System - Development Plan

> Multi-agent system using Google ADK + LiteLLM + MiniMax for professional-grade stock analysis

---

## System Architecture

```
User Input (API Request)
    ↓
Plan Agent (Google ADK Root Agent)
    ↓
┌─────────────────────────────────────────┐
│           Tool Calling Layer            │
│  ┌─────────────┐    ┌──────────────┐  │
│  │  Finnhub    │    │  Celebrity    │  │
│  │  API Tools  │    │  Skill Tools  │  │
│  └─────────────┘    └──────────────┘  │
└─────────────────────────────────────────┘
    ↓
LiteLlm → MiniMax-M2.1
    ↓
JSON Response
```

---

## Celebrity Skills (Already Developed)

| Skill | Location | Content |
|-------|----------|---------|
| Warren Buffett | `celebrity_skills/warren_buffett/` | Value investing, moat analysis, 60+ years philosophy |
| Cathie Wood | `celebrity_skills/cathie_wood/` | Disruptive innovation, Big Ideas, high-growth |
| Greg Abel | `celebrity_skills/greg_abel/` | Operational excellence, Berkshire perspective |

---

## Development Phases

### Phase 1: Core Infrastructure ✅ (Completed)

- [x] Project structure defined
- [x] README with architecture
- [x] Finnhub API tools
- [x] LiteLLM + MiniMax integration documented
- [x] Google ADK patterns documented

---

### Phase 2: Agent Implementation (Next)

**Priority 1 - Foundation Agents**

| Task | Description | Output |
|------|-------------|--------|
| 2.1 | Setup Google ADK project structure | `agents/__init__.py`, config |
| 2.2 | Create LLM service (MiniMax via LiteLlm) | `services/llm_service.py` |
| 2.3 | Create Finnhub data service | `services/data_service.py` |
| 2.4 | Create Base Agent class | `agents/base_agent.py` |

**Priority 2 - Tool Implementation**

| Task | Description | Output |
|------|-------------|--------|
| 2.5 | Implement stock quote tool | `tools/stock_tools.py` |
| 2.6 | Implement news tool | `tools/news_tools.py` |
| 2.7 | Implement fundamentals tool | `tools/fundamentals_tools.py` |

---

### Phase 3: Celebrity Skill Integration

**Priority 3 - Skill Loading**

| Task | Description | Output |
|------|-------------|--------|
| 3.1 | Create skill loader service | `services/skill_loader.py` |
| 3.2 | Load Buffett skill as context | `skills/buffett/` |
| 3.3 | Load Cathie Wood skill as context | `skills/cathie_wood/` |
| 3.4 | Load Greg Abel skill as context | `skills/greg_abel/` |

**Priority 4 - Expert Sub-Agents**

| Task | Description | Output |
|------|-------------|--------|
| 3.5 | Create Buffett expert agent | `agents/experts/buffett_agent.py` |
| 3.6 | Create Cathie Wood expert agent | `agents/experts/cathie_wood_agent.py` |
| 3.7 | Create Greg Abel expert agent | `agents/experts/greg_abel_agent.py` |

---

### Phase 4: Plan Agent (Root Coordinator)

**Priority 5 - Core Logic**

| Task | Description | Output |
|------|-------------|--------|
| 4.1 | Create Plan Agent with intent detection | `agents/plan_agent.py` |
| 4.2 | Implement routing logic | Routing to appropriate expert |
| 4.3 | Implement multi-perspective analysis | Combine all 3 expert views |
| 4.4 | Create response synthesizer | Format final JSON response |

---

### Phase 5: API Layer

**Priority 6 - FastAPI Endpoints**

| Task | Description | Output |
|------|-------------|--------|
| 5.1 | Create `/analyze` endpoint | Stock analysis with celebrity perspectives |
| 5.2 | Create `/search` endpoint | Real-time data search |
| 5.3 | Create `/health` endpoint | System health check |
| 5.4 | Add error handling | Robust error responses |
| 5.5 | Add request validation | Pydantic schemas |

---

### Phase 6: Testing & Polish

**Priority 7 - Testing**

| Task | Description |
|------|-------------|
| 6.1 | Unit tests for tools |
| 6.2 | Unit tests for agents |
| 6.3 | Integration tests |
| 6.4 | API endpoint tests |

**Priority 8 - Polish**

| Task | Description |
|------|-------------|
| 6.5 | Response formatting |
| 6.6 | Logging |
| 6.7 | Documentation |
| 6.8 | Docker support (optional) |

---

## Detailed Task List

### Phase 2 Tasks

```python
# Task 2.1: agents/__init__.py
# Task 2.2: services/llm_service.py
#   - Create LiteLlm model instance
#   - Handle API key configuration
#   - Provide model for all agents

# Task 2.3: services/data_service.py
#   - Finnhub client wrapper
#   - Cache layer for rate limits
#   - Error handling

# Task 2.4: agents/base_agent.py
#   - Base class for all agents
#   - Common tools and context
```

### Phase 3 Tasks

```python
# Task 3.1: services/skill_loader.py
#   - Load SKILL.md from celebrity_skills/
#   - Parse markdown to context string
#   - Provide to agents

# Task 3.2-3.4: Copy celebrity_skills to project
#   - ~/Desktop/sandbox/celebrity_skills/warren_buffett/
#   - ~/Desktop/sandbox/celebrity_skills/cathie_wood/
#   - ~/Desktop/sandbox/celebrity_skills/greg_abel/

# Task 3.5-3.7: Expert agents
#   - Load respective skill
#   - Instruction prompt with skill context
#   - Tool access
```

### Phase 4 Tasks

```python
# Task 4.1: agents/plan_agent.py
#   - Intent: "analyze", "search", "compare", "philosophy"
#   - Route to appropriate sub-agents
#   - Synthesize responses

# Task 4.2: Routing logic
#   - detect_intent(user_input) → routing decision
#   - style="buffett" | "wood" | "abel" | "all"

# Task 4.3: Multi-perspective
#   - Run all 3 experts in parallel
#   - Combine into cohesive response

# Task 4.4: Synthesizer
#   - Format: {answer, sources, agents_used, timestamp}
```

### Phase 5 Tasks

```python
# Task 5.1: POST /analyze
# Request: {"question": str, "style": str}
# Response: {"answer": str, "sources": [], "agents_used": []}

# Task 5.2: POST /search
# Request: {"query": str}
# Response: {"results": [{"title", "url", "snippet"}]}

# Task 5.3: GET /health
# Response: {"status": "healthy", "version": str}
```

---

## File Structure (Target)

```
financial_analyst/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base class
│   ├── plan_agent.py          # Root coordinator
│   └── experts/
│       ├── __init__.py
│       ├── buffett_agent.py   # Warren Buffett expert
│       ├── cathie_wood_agent.py  # Cathie Wood expert
│       └── greg_abel_agent.py  # Greg Abel expert
├── skills/                     # Celebrity Skills (copied)
│   ├── buffett/
│   ├── cathie_wood/
│   └── greg_abel/
├── tools/
│   ├── __init__.py
│   ├── finnhub_tools.py       # Finnhub API
│   └── skill_tools.py         # Skill loading
├── services/
│   ├── __init__.py
│   ├── llm_service.py        # LiteLlm + MiniMax
│   ├── data_service.py       # Finnhub wrapper
│   └── skill_loader.py       # Load celebrity skills
├── api/
│   └── main.py               # FastAPI app
├── models/
│   └── schemas.py            # Pydantic models
├── tests/
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_api.py
├── celebrity_skills/           # Symlink or copy
├── requirements.txt
├── config.yaml
└── main.py
```

---

## Environment Variables

```bash
# Required
MINIMAX_API_KEY=sk-xxx        # MiniMax API
FINNHUB_API_KEY=xxx           # Finnhub API

# Optional
LITEllM_API_KEY=sk-xxx       # If using LiteLLM proxy
PORT=8000                     # API port
```

---

## API Specification

### POST /analyze

**Request:**
```json
{
  "question": "Should I invest in Tesla?",
  "style": "buffett"  // "buffett" | "wood" | "abel" | "all"
}
```

**Response:**
```json
{
  "answer": "Based on Warren Buffett's framework...",
  "sources": [
    {"type": "news", "title": "...", "url": "..."},
    {"type": "skill", "name": "buffett"}
  ],
  "agents_used": ["buffett_agent", "data_agent"],
  "timestamp": "2026-04-11T18:13:00Z"
}
```

### POST /search

**Request:**
```json
{
  "query": "Tesla Q1 2026 earnings"
}
```

**Response:**
```json
{
  "results": [
    {"title": "...", "url": "...", "snippet": "..."}
  ]
}
```

---

## Execution Order

1. **Phase 2 (Foundation)** - Tasks 2.1 → 2.7
2. **Phase 3 (Skills)** - Tasks 3.1 → 3.7
3. **Phase 4 (Plan Agent)** - Tasks 4.1 → 4.4
4. **Phase 5 (API)** - Tasks 5.1 → 5.5
5. **Phase 6 (Testing)** - Tasks 6.1 → 6.8

---

## Next Step

**Task 2.1:** Setup Google ADK project structure

等待确认后开始执行
