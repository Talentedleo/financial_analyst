# Financial Analyst AI Agent System

> Multi-agent system using Google ADK + LiteLLM + MiniMax for professional-grade stock analysis with celebrity investor perspectives

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-green.svg)](https://adk.dev/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-Proxy-orange.svg)](https://docs.litellm.ai/)
[![MiniMax](https://img.shields.io/badge/MiniMax-M2.7--highspeed-red.svg)](https://www.minimax.chat/)

---

## Features

- **Multi-Agent Architecture**: Plan Agent + 3 Expert Agents (Buffett, Cathie Wood, Greg Abel)
- **Hybrid Data Sources**: Finnhub (free) + Yahoo Finance (premium) for comprehensive market data
- **Real-Time Data**: Stock quotes, news, company profiles, financial metrics
- **Flexible Analysis**: Ask any stock or financial question naturally
- **Celebrity Perspectives**: Get insights from legendary investors' frameworks
- **REST API**: FastAPI-powered endpoints with session management
- **Push Notifications**: Bark integration for iOS push notifications

---

## Requirements

- **Python 3.12+** (required for Google ADK and MCP support)

---

## Quick Start

### 1. Install Python 3.12

```bash
# macOS with Homebrew
brew install python@3.12

# Verify
python3.12 --version
```

### 2. Create Virtual Environment

```bash
cd ~/Desktop/sandbox/financial_analyst

# Create venv with Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Verify Python version
python --version  # Should show 3.12.x
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy and edit .env file
cp .env.example .env

# Edit .env with your API keys
# MINIMAX_API_KEY=your-minimax-api-key
# FINNHUB_API_KEY=your-finnhub-api-key
# BARK_API_KEY=your-bark-push-key (optional, for iOS notifications)
```

### 5. Run Tests

```bash
python tests/test_main.py
```

### 6. Start the API Server

```bash
python main.py

# With custom port (default: 8000)
python main.py --port 9000
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
| `/clear-session` | POST | Clear conversation session |

### Example Requests

```bash
# Analyze stock with Buffett style
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"question": "Should I invest in Apple?", "style": "buffett"}'

# Analyze with all experts
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"question": "What do you think about Tesla?", "style": "all"}'

# Search for stock
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"query": "AAPL"}'
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
│  Buffett Agent │ Cathie Wood     │ Greg Abel     │
│  (Value)       │ (Growth)        │ (Operations)  │
└─────────────────┴─────────────────┴──────────────┘
    ↓                    ↓                    ↓
┌─────────────────────────────────────────────────┐
│              Data Service                        │
├─────────────────┬─────────────────┬────────────┤
│  Finnhub        │ Yahoo Finance   │ Tools       │
│  (Quote/News)  │ (Candles)       │ (ADK)       │
└─────────────────┴─────────────────┴────────────┘
    ↓
LiteLlm → MiniMax-M2.7-highspeed
    ↓
JSON Response + Push Notification (Bark)
```

---

## Project Structure

```
financial_analyst/
├── main.py                    # Entry point (starts API server)
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class
│   ├── plan_agent.py          # Root coordinator
│   └── experts/
│       ├── __init__.py
│       ├── buffett_agent.py    # Warren Buffett
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
│   ├── data_service.py        # Finnhub + yfinance wrapper
│   └── skill_loader.py        # Celebrity skills loader
├── skills/                    # Celebrity Skills (embedded)
│   ├── warren_buffett/
│   ├── cathie_wood/
│   └── greg_abel/
├── api/
│   ├── __init__.py
│   └── routes.py              # FastAPI routes
└── tests/
    └── test_main.py           # Test suite (23 tests)
```

---

## Celebrity Skills (Embedded)

Expert perspectives from legendary investors:

| Expert | Philosophy | Key Questions |
|--------|------------|---------------|
| **Warren Buffett** | Value investing, moat analysis | "Would I own this forever?" |
| **Cathie Wood** | Disruptive innovation, 5-year horizon | "Will this transform an industry?" |
| **Greg Abel** | Operational excellence, Berkshire model | "Would Buffett be comfortable?" |

---

## Data Sources

### Finnhub (Free Tier)

| Feature | Description |
|---------|-------------|
| Stock Quote | Real-time price, change, volume |
| Company News | Company-specific news articles |
| Market News | General financial news |
| Company Profile | Business info, industry, description |
| Symbol Search | Search by company name or symbol |
| Peer Companies | Competitors comparison |
| Financial Metrics | Revenue, earnings, P/E ratios |

### Yahoo Finance (yfinance)

| Feature | Description |
|---------|-------------|
| Candlestick Data | Historical OHLCV data (premium on Finnhub) |

---

## Push Notifications (Bark)

The system supports iOS push notifications via Bark with Markdown and long message splitting.

### Setup

1. Install [Bark](https://github.com/Finb/Bark) iOS app
2. Get your Device Key from the app
3. Add to `.env`:
   ```
   BARK_DEVICE_KEY=your-device-key
   BARK_SERVER_URL=https://api.day.app
   ```

### Features

- **Markdown Support**: Full Markdown formatting in notifications
- **Auto-Splitting**: Long messages (>2000 chars) automatically split into chunks
- **Custom Sounds**: 24 notification sounds available
- **Priority Levels**: active, passive, timeSensitive

### Notification Functions

| Function | Description |
|----------|-------------|
| `send_notification` | Send general push notification with Markdown |
| `send_analysis_notification` | Send stock analysis result (auto-split) |
| `send_market_alert` | Send urgent market alert (auto-split) |

### Available Sounds

`alarm`, `anticipate`, `bell`, `birdsong`, `bloom`, `calypso`, `chime`, `complete`, `descent`, `electric`, `fanfare`, `glass`, `horns`, `ladder`, `minuet`, `newsflash`, `noir`, `sherwoodforest`, `spell`, `suspense`, `telegraph`, `tiptoes`, `typewriters`, `update`, `None`

---

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Test Results

```
Total: 23 | Passed: 23 | Failed: 0 (100.0%)
```

---

## References

- [Google ADK](https://github.com/google/adk-python)
- [LiteLLM](https://docs.litellm.ai/)
- [MiniMax](https://www.minimax.chat/)
- [Finnhub API](https://finnhub.io/)
- [Yahoo Finance (yfinance)](https://github.com/ranaroussi/yfinance)
- [Bark](https://github.com/Finb/Bark) - iOS Push Notifications

---

## License

MIT License
