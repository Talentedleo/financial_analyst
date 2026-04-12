---
name: financial-analyst-api
description: Financial Analyst AI Agent API endpoints for stock analysis, search, and system management
---

# Financial Analyst API Endpoints

## Overview

This API provides stock analysis with expert investor perspectives (Warren Buffett, Cathie Wood, Greg Abel). Each expert uses their investment philosophy and real-time market data.

## Authentication

All endpoints (except `/health`) require `X-API-Key` header:
```
X-API-Key: your-api-key
```

Default key for development: `sk-1234`

---

## Endpoints

### POST /analyze

Analyze a stock or investment question with an expert perspective.

**Request:**
```json
{
  "question": "NVDA 值得购买吗？",
  "style": "warren_buffett",
  "user_id": "default_user",
  "new_session": true
}
```

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `question` | string | ✅ | - | Stock/financial question (any language) |
| `style` | string | ❌ | `warren_buffett` | Expert style (see below) |
| `user_id` | string | ❌ | `default_user` | User identifier for session continuity |
| `new_session` | boolean | ❌ | `false` | Force new session if true |

**Expert Styles:**

| Style | Expert | Description |
|-------|--------|-------------|
| `warren_buffett` | Warren Buffett | Value investing, moat analysis |
| `cathie_wood` | Cathie Wood | Disruptive innovation, high-growth |
| `greg_abel` | Greg Abel | Operational excellence, Berkshire |

**Response:**
```json
{
  "answer": "...",
  "stock_identified": null,
  "sources": [],
  "agents_used": ["buffett_agent"],
  "timestamp": "2026-04-12T16:29:00.000000",
  "style": "warren_buffett",
  "session_id": "session_xxx"
}
```

---

### POST /search

Search for stock data and news.

**Request:**
```json
{
  "query": "AAPL"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | ✅ | Stock symbol (e.g., "AAPL") or company name |

**Response:**
```json
{
  "results": [
    {
      "type": "quote",
      "symbol": "AAPL",
      "price": 260.48,
      "change": -0.01,
      "percent_change": -0.0038,
      "high": 262.19,
      "low": 259.02
    },
    {
      "type": "news",
      "headline": "TSMC's Record Q1 AI Revenue...",
      "source": "Yahoo",
      "url": "https://..."
    }
  ],
  "timestamp": "2026-04-12T16:29:00.000000"
}
```

---

### GET /agents

List available expert agents.

**Response:**
```json
{
  "agents": [
    {"name": "buffett_agent", "description": "Warren Buffett - Value investing"},
    {"name": "cathie_wood_agent", "description": "Cathie Wood - Disruptive innovation"},
    {"name": "greg_abel_agent", "description": "Greg Abel - Operational excellence"}
  ]
}
```

---

### POST /clear-session

Clear conversation session for a user.

**Query Parameters:**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `user_id` | string | ❌ | `default_user` | User identifier |

**Response:**
```json
{
  "message": "Session cleared for user default_user"
}
```

---

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2026-04-12T16:29:00.000000"
}
```

---

## Usage Examples

### cURL

```bash
# Analyze with Warren Buffett
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"question": "TSLA 值得购买吗？", "style": "warren_buffett"}'

# Search stock
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-1234" \
  -d '{"query": "NVDA"}'
```

### Python

```python
import requests

headers = {"X-API-Key": "sk-1234"}

# Analyze
resp = requests.post(
    "http://localhost:8000/analyze",
    json={"question": "AAPL 值得购买吗？", "style": "warren_buffett"},
    headers=headers
)
print(resp.json()["answer"])

# Search
resp = requests.post(
    "http://localhost:8000/search",
    json={"query": "TSLA"},
    headers=headers
)
print(resp.json()["results"])
```

---

## Important Notes

1. **Language Matching**: The expert will respond in the same language as your question
   - Chinese question → Chinese response
   - English question → English response

2. **Session Continuity**: Use same `user_id` across requests for conversation continuity

3. **New Session**: Set `new_session: true` to start fresh analysis

4. **Bark Notifications**: If `BARK_DEVICE_KEY` is configured, analysis results are sent to your iOS device

5. **Rate Limits**: No strict rate limits, but be reasonable to avoid API overload
