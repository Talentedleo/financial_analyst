# Financial Analyst AI Agent System

> Multi-agent system using Google ADK + LiteLLM + MiniMax for professional-grade stock analysis with celebrity investor perspectives

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-green.svg)](https://adk.dev/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-Proxy-orange.svg)](https://docs.litellm.ai/)
[![MiniMax](https://img.shields.io/badge/MiniMax-M2.1-red.svg)](https://www.minimax.io/)

---

## Features

- **Multi-Agent Architecture**: Plan Agent + 3 Expert Agents (Buffett, Cathie Wood, Greg Abel)
- **Real-Time Data**: Finnhub API for stock quotes, news, and fundamentals
- **Flexible Analysis**: Ask any stock or financial question
- **Celebrity Perspectives**: Get insights from legendary investors' frameworks
- **REST API**: FastAPI-powered endpoints for easy integration

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export MINIMAX_API_KEY="your-minimax-api-key"
export FINNHUB_API_KEY="your-finnhub-api-key"
```

### 3. Run the API Server

```bash
uvicorn api.main:app --reload --port 8000
```

### 4. Test the API

```bash
# Analyze any stock question
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I invest in Apple?", "style": "all"}'

# Search for stock data
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "AAPL"}'
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/agents` | GET | List available expert agents |
| `/analyze` | POST | Analyze any stock/financial question |
| `/search` | POST | Search stock data and news |

### Example Questions

```json
{
  "question": "Should I invest in Apple?",
  "style": "all"
}
```

```json
{
  "question": "What do you think about Tesla from Cathie Wood's perspective?",
  "style": "wood"
}
```

```json
{
  "question": "Is Nvidia overvalued using Buffett's framework?",
  "style": "buffett"
}
```

### Analysis Styles

| Style | Expert | Description |
|-------|--------|-------------|
| `buffett` | Warren Buffett | Value investing, moat analysis |
| `wood` | Cathie Wood | Disruptive innovation, high-growth |
| `abel` | Greg Abel | Operational excellence, Berkshire |
| `all` | All Experts | Multi-perspective analysis |

---

## Architecture

```
User Question (any stock/financial question)
    ↓
Plan Agent (automatic stock identification + routing)
    ↓
┌─────────────────────────────────────────────────┐
│              Expert Agents                       │
├─────────────────┬─────────────────┬──────────────┤
│  Buffett Agent │ Cathie Wood     │ Greg Abel    │
│  (Value)       │ (Growth)        │ (Operations) │
└─────────────────┴─────────────────┴──────────────┘
    ↓                    ↓                    ↓
┌─────────────────────────────────────────────────┐
│              Finnhub Tools                      │
├─────────────┬─────────────┬────────────────────┤
│ Stock Quote │ News        │ Fundamentals       │
└─────────────┴─────────────┴────────────────────┘
    ↓
LiteLlm → MiniMax-M2.1
    ↓
JSON Response
```

---

## Project Structure

```
financial_analyst/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class
│   ├── plan_agent.py          # Root coordinator
│   └── experts/
│       ├── __init__.py
│       ├── buffett_agent.py   # Warren Buffett
│       ├── cathie_wood_agent.py
│       └── greg_abel_agent.py
├── tools/
│   ├── __init__.py
│   ├── stock_tools.py         # Quote, search, candles
│   ├── news_tools.py          # Company & market news
│   └── fundamentals_tools.py  # Profile, peers
├── services/
│   ├── __init__.py
│   ├── llm_service.py         # LLM service
│   ├── data_service.py        # Finnhub wrapper
│   └── skill_loader.py       # Celebrity skills loader
├── api/
│   └── main.py                # FastAPI app
├── main.py                    # Entry point
└── requirements.txt
```

---

## Celebrity Skills

This project integrates [Celebrity Skills](https://github.com/Talentedleo/celebrity_skills) to provide authentic expert perspectives:

| Expert | Philosophy | Key Questions |
|--------|------------|---------------|
| **Warren Buffett** | Value investing, moat analysis | "Would I own this forever?" |
| **Cathie Wood** | Disruptive innovation, 5-year horizon | "Will this transform an industry?" |
| **Greg Abel** | Operational excellence, Berkshire model | "Would Buffett be comfortable?" |

---

## Data Source: Finnhub API

| Endpoint | Usage |
|----------|-------|
| `/quote` | Real-time stock price, change, volume |
| `/company-news` | Company-specific news |
| `/general-news` | Market news |
| `/stock/candle` | OHLCV candlestick data |
| `/stock/profile2` | Company profile |
| `/peers` | Peer companies |

---

## Development

### Run Locally

```bash
cd ~/Desktop/sandbox/openclaw_project/src/financial_analyst

# Install dependencies
pip install -r requirements.txt

# Set environment
export MINIMAX_API_KEY="your-key"
export FINNHUB_API_KEY="your-key"

# Run server
uvicorn api.main:app --reload --port 8000
```

### API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## References

- [Google ADK](https://github.com/google/adk-python)
- [LiteLLM](https://docs.litellm.ai/)
- [MiniMax](https://www.minimax.io/)
- [Finnhub API](https://finnhub.io/)

---

## License

MIT License
