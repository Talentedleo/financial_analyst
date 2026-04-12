# Financial Analyst AI Agent System

> Multi-agent stock analysis using Google ADK + LiteLLM + MiniMax with celebrity investor perspectives

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-green.svg)](https://adk.dev/)
[![MiniMax](https://img.shields.io/badge/MiniMax-M2.7--highspeed-red.svg)](https://www.minimax.chat/)

---

## Features

- **Direct Expert Routing**: No coordinator layer, direct call to expert agents
- **ADK Skills**: Each expert uses Google's official SkillToolset for investment philosophy
- **Real-Time Data**: Finnhub (free) + Yahoo Finance (premium) for market data
- **Celebrity Investor Perspectives**: Warren Buffett, Cathie Wood, Greg Abel
- **Push Notifications**: Bark integration for iOS notifications
- **REST API**: FastAPI-powered endpoints with session management

---

## Requirements

- **Python 3.12+** (required for Google ADK)

---

## Quick Start

### 1. Install Python 3.12

```bash
brew install python@3.12
```

### 2. Create Virtual Environment

```bash
cd ~/Desktop/sandbox/financial_analyst
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Run Tests

```bash
python tests/test_main.py
```

### 6. Start the API Server

```bash
python main.py
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/agents` | GET | List available expert agents |
| `/analyze` | POST | Analyze stock with expert perspective |
| `/search` | POST | Search stock data |
| `/clear-session` | POST | Clear conversation session |

### Example Requests

```bash
# Analyze with Warren Buffett
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"question": "NVDA值得购买吗？", "style": "warren_buffett"}'

# Analyze with Cathie Wood
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"question": "TSLA值得购买吗？", "style": "cathie_wood"}'

# Analyze with Greg Abel
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"question": "AAPL值得购买吗？", "style": "greg_abel"}'
```

### Expert Agents

| Style Parameter | Expert | Philosophy |
|----------------|--------|-------------|
| `warren_buffett` | Warren Buffett | Value investing, moat analysis |
| `cathie_wood` | Cathie Wood | Disruptive innovation, high-growth |
| `greg_abel` | Greg Abel | Operational excellence, Berkshire |

---

## Architecture

```
User Question
    ↓
┌─────────────────────────────────────┐
│          Direct Expert Agent         │
│   (based on style parameter)        │
├─────────────────────────────────────┤
│  - Read ADK SkillToolset           │
│  - Gather real-time data            │
│  - Apply investment framework      │
│  - First-person response            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│          Data Service                │
├──────────────┬──────────────────────┤
│   Finnhub   │   Yahoo Finance      │
│ (Quote/News)│     (Candles)        │
└──────────────┴──────────────────────┘
    ↓
LiteLlm → MiniMax-M2.7-highspeed
    ↓
JSON Response + Bark Notification
```

---

## Project Structure

```
financial_analyst/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .env.example               # Environment template
├── agents/
│   ├── __init__.py
│   └── experts/
│       ├── __init__.py
│       ├── warren_buffett_agent.py
│       ├── cathie_wood_agent.py
│       └── greg_abel_agent.py
├── tools/
│   ├── __init__.py
│   ├── stock_tools.py         # Quote, search, candles
│   ├── news_tools.py          # Company & market news
│   ├── fundamentals_tools.py  # Profile, peers, financials
│   └── bark_tools.py          # iOS push notifications
├── services/
│   ├── __init__.py
│   ├── llm_service.py         # LLM service (MiniMax)
│   ├── data_service.py        # Finnhub + yfinance
│   └── skill_loader.py        # Skill utilities
├── skills/                    # ADK Skills
│   ├── warren-buffett/
│   ├── cathie-wood/
│   └── greg-abel/
├── api/
│   ├── __init__.py
│   └── routes.py              # FastAPI routes
└── tests/
    └── test_main.py           # Test suite (21 tests)
```

---

## Expert Agents

Each expert agent:
1. Reads ADK SkillToolset to learn the investment philosophy
2. Uses tools to gather real-time data
3. Applies the skill's framework to analyze
4. Responds in first person, matching the question's language

### ADK Skills

Skills are loaded using Google's official `load_skill_from_dir` and `SkillToolset`:

```python
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset

skill = load_skill_from_dir(Path("skills/warren-buffett"))
skill_toolset = SkillToolset(skills=[skill])

Agent(..., tools=[..., skill_toolset])
```

---

## Data Sources

### Finnhub (Free)

| Feature | Description |
|---------|-------------|
| Stock Quote | Real-time price, change, volume |
| Company News | Company-specific news |
| Market News | General financial news |
| Company Profile | Business info, industry |
| Symbol Search | Search by name/symbol |
| Financial Metrics | Revenue, P/E, ROE, etc. |

### Yahoo Finance (yfinance)

| Feature | Description |
|---------|-------------|
| Candlestick Data | Historical OHLCV data |

---

## Push Notifications (Bark)

```bash
# Configure in .env
BARK_DEVICE_KEY=your-device-key
BARK_SERVER_URL=https://api.day.app
```

---

## Test Results

```
Total: 21 | Passed: 21 | Failed: 0 (100.0%)
```

---

## References

- [Google ADK](https://github.com/google/adk-python)
- [LiteLLM](https://docs.litellm.ai/)
- [MiniMax](https://www.minimax.chat/)
- [Finnhub API](https://finnhub.io/)
- [Yahoo Finance (yfinance)](https://github.com/ranaroussi/yfinance)
- [Bark](https://github.com/Finb/Bark)

---

## License

MIT License
