"""
FastAPI Application - Financial Analyst AI Agent

Production deployment should:
1. Set API_MASTER_KEY environment variable
2. Configure CORS allowed origins
3. Use Redis for session storage
"""

import os
import asyncio
from typing import Optional, Literal, List, Dict
from datetime import datetime
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Body, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents.plan_agent import get_plan_agent
from services import get_data_service


# ============== Authentication ==============

API_MASTER_KEY = os.environ.get("API_MASTER_KEY", "sk-1234")  # Change in production


async def verify_api_key(x_api_key: str = Header(None)) -> str:
    """Verify API key from header"""
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing X-API-Key header. Set API_MASTER_KEY environment variable."
        )
    if x_api_key != API_MASTER_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key


# ============== Session Management ==============

class SessionManager:
    """Manage conversation sessions per user"""
    
    def __init__(self):
        self._user_sessions: Dict[str, str] = defaultdict(lambda: None)
        self._last_used: Dict[str, float] = {}
    
    def get_session_id(self, user_id: str) -> str:
        return self._user_sessions[user_id]
    
    def set_session_id(self, user_id: str, session_id: str) -> None:
        self._user_sessions[user_id] = session_id
        self._last_used[session_id] = datetime.now().timestamp()
    
    def clear_session(self, user_id: str) -> None:
        session_id = self._user_sessions.get(user_id)
        if session_id and session_id in self._last_used:
            del self._last_used[session_id]
        if user_id in self._user_sessions:
            del self._user_sessions[user_id]


session_manager = SessionManager()


# ============== Request/Response Models ==============

class AnalyzeRequest(BaseModel):
    question: str = Field(..., description="Any stock or financial question")
    style: Optional[Literal["buffett", "wood", "abel", "all"]] = Field(default="all")
    user_id: Optional[str] = Field(default="default_user")
    new_session: Optional[bool] = Field(default=False)


class AnalyzeResponse(BaseModel):
    answer: str
    stock_identified: Optional[str] = None
    sources: List[dict] = Field(default_factory=list)
    agents_used: List[str]
    timestamp: str
    style: str
    session_id: str


class SearchRequest(BaseModel):
    query: str = Field(..., description="Stock symbol or company name")


class SearchResponse(BaseModel):
    results: List[dict]
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str


class AgentInfo(BaseModel):
    name: str
    description: str


class AgentsListResponse(BaseModel):
    agents: List[AgentInfo]


# ============== CORS Configuration ==============

ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "*"  # Configure for production (e.g., "https://yourdomain.com")
).split(",")


# ============== FastAPI App ==============

app = FastAPI(
    title="Financial Analyst AI Agent",
    description="Multi-agent stock analysis with Buffett, Cathie Wood, Greg Abel perspectives",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Endpoints ==============

@app.get("/", response_model=dict)
async def root():
    return {
        "name": "Financial Analyst AI Agent",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
async def analyze(
    request: AnalyzeRequest,
    _api_key: str = Depends(verify_api_key)
):
    """
    Analyze any stock or financial question.
    
    Requires X-API-Key header.
    Use same user_id for conversation continuity.
    """
    try:
        plan_agent = get_plan_agent()
        user_id = request.user_id or "default_user"
        
        if request.new_session:
            session_id = f"session_{datetime.now().timestamp()}"
            session_manager.set_session_id(user_id, session_id)
        else:
            existing_session = session_manager.get_session_id(user_id)
            session_id = existing_session if existing_session else f"session_{datetime.now().timestamp()}"
            session_manager.set_session_id(user_id, session_id)
        
        answer = await plan_agent.run(
            query=request.question,
            user_id=user_id,
            session_id=session_id
        )
        
        agents_used = ["plan_agent"]
        if request.style == "all" or request.style is None:
            agents_used.extend(["buffett_agent", "cathie_wood_agent", "greg_abel_agent"])
        elif request.style == "buffett":
            agents_used.append("buffett_agent")
        elif request.style == "wood":
            agents_used.append("cathie_wood_agent")
        elif request.style == "abel":
            agents_used.append("greg_abel_agent")
        
        return AnalyzeResponse(
            answer=answer or f"Analysis of: {request.question}",
            stock_identified=None,
            sources=[],
            agents_used=agents_used,
            timestamp=datetime.now().isoformat(),
            style=request.style or "all",
            session_id=session_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear-session", tags=["System"])
async def clear_session(
    user_id: str = "default_user",
    _api_key: str = Depends(verify_api_key)
):
    """Clear conversation session for a user"""
    session_manager.clear_session(user_id)
    return {"message": f"Session cleared for user {user_id}"}


@app.post("/search", response_model=SearchResponse, tags=["Search"])
async def search(
    request: SearchRequest,
    _api_key: str = Depends(verify_api_key)
):
    """Search for stock data and news"""
    try:
        data_service = get_data_service()
        query = request.query.strip()
        results = []
        
        if len(query) <= 5 and query.replace('.', '').isalnum():
            try:
                quote = data_service.get_quote(query.upper())
                if quote.get('c', 0) > 0:
                    results.append({
                        "type": "quote",
                        "symbol": query.upper(),
                        "price": quote.get('c'),
                        "change": quote.get('d'),
                        "percent_change": quote.get('dp'),
                        "high": quote.get('h'),
                        "low": quote.get('l')
                    })
            except Exception:
                pass
        
        if len(results) > 0:
            symbol = results[0].get('symbol')
            try:
                news = data_service.get_company_news(symbol, days=7)
                for article in news[:5]:
                    results.append({
                        "type": "news",
                        "headline": article.get('headline'),
                        "source": article.get('source'),
                        "url": article.get('url')
                    })
            except Exception:
                pass
        else:
            search_results = data_service.search_symbol(query)
            # Finnhub returns {'count': N, 'result': [...]}
            result_list = search_results.get('result', search_results) if isinstance(search_results, dict) else search_results
            for r in result_list[:5]:
                symbol = r.get('symbol')
                try:
                    quote = data_service.get_quote(symbol)
                    results.append({
                        "type": "symbol",
                        "symbol": symbol,
                        "description": r.get('description'),
                        "price": quote.get('c'),
                        "change": quote.get('d'),
                        "percent_change": quote.get('dp')
                    })
                except Exception:
                    results.append({
                        "type": "symbol",
                        "symbol": symbol,
                        "description": r.get('description')
                    })
        
        return SearchResponse(
            results=results,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents", response_model=AgentsListResponse, tags=["System"])
async def list_agents(
    _api_key: str = Depends(verify_api_key)
):
    """List available expert agents"""
    return AgentsListResponse(
        agents=[
            AgentInfo(name="buffett_agent", description="Warren Buffett - Value investing"),
            AgentInfo(name="cathie_wood_agent", description="Cathie Wood - Disruptive innovation"),
            AgentInfo(name="greg_abel_agent", description="Greg Abel - Operational excellence"),
            AgentInfo(name="plan_agent", description="Plan Agent - Coordinator")
        ]
    )


