"""
FastAPI Application - Financial Analyst AI Agent

Production deployment should:
1. Set API_MASTER_KEY environment variable
2. Configure CORS allowed origins
3. Use Redis for session storage
"""

import os
import logging
from typing import Optional, Literal, List, Dict
from datetime import datetime
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agents import create_buffett_agent, create_cathie_wood_agent, create_greg_abel_agent
from services import get_data_service


# ============== Authentication ==============

API_MASTER_KEY = os.environ.get("API_MASTER_KEY", "sk-1234")


async def verify_api_key(x_api_key: str = Header(None)) -> str:
    """Verify API key from header"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    if x_api_key != API_MASTER_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key


# ============== Session Management ==============

class SessionManager:
    """Manage conversation sessions per user"""
    
    def __init__(self):
        self._user_sessions: Dict[str, str] = defaultdict(lambda: None)
        self._last_used: Dict[str, float] = {}
        self._session_services: Dict[str, InMemorySessionService] = {}
        self._runners: Dict[str, Runner] = {}
    
    def get_or_create_runner(self, user_id: str, session_id: str, agent_name: str) -> Runner:
        """Get or create a runner for the given user/session/agent combination"""
        key = f"{user_id}:{session_id}:{agent_name}"
        
        if key not in self._runners:
            # Create appropriate agent based on agent_name
            if agent_name == "buffett_agent":
                agent = create_buffett_agent()
            elif agent_name == "cathie_wood_agent":
                agent = create_cathie_wood_agent()
            elif agent_name == "greg_abel_agent":
                agent = create_greg_abel_agent()
            else:
                agent = create_buffett_agent()  # default
            
            session_service = InMemorySessionService()
            self._session_services[key] = session_service
            
            self._runners[key] = Runner(
                agent=agent,
                app_name=agent_name,
                session_service=session_service
            )
        
        return self._runners[key]
    
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
    style: Optional[Literal["buffett", "wood", "abel"]] = Field(default="buffett")
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
    "*"
).split(",")


# ============== FastAPI App ==============

app = FastAPI(
    title="Financial Analyst AI Agent",
    description="Stock analysis with Buffett, Cathie Wood, Greg Abel perspectives",
    version="2.0.0"
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
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    return HealthResponse(
        status="healthy",
        version="2.0.0",
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
        user_id = request.user_id or "default_user"
        
        if request.new_session:
            session_id = f"session_{datetime.now().timestamp()}"
            session_manager.set_session_id(user_id, session_id)
        else:
            existing_session = session_manager.get_session_id(user_id)
            session_id = existing_session if existing_session else f"session_{datetime.now().timestamp()}"
            session_manager.set_session_id(user_id, session_id)
        
        # Determine which agent to use based on style
        agent_name = f"{request.style}_agent"
        
        # Get or create runner for this agent
        runner = session_manager.get_or_create_runner(user_id, session_id, agent_name)
        
        # Create session
        await runner.session_service.create_session(
            app_name=agent_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Run the agent
        from google.genai import types
        content = types.Content(
            role="user",
            parts=[types.Part(text=request.question)]
        )
        
        response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response():
                response_text = event.content.parts[0].text
        
        # Send Bark notification with analysis result (if configured)
        if os.environ.get("BARK_DEVICE_KEY"):
            try:
                from tools.bark_tools import get_bark_client
                bark = get_bark_client()
                stock_symbol = request.question.upper().split()[0] if request.question else "STOCK"
                bark.send_long_message(
                    content=response_text[:5000] if response_text else "Analysis complete",
                    title=f"📊 {stock_symbol} Analysis ({request.style})",
                    group=f"Analysis - {stock_symbol}",
                    sound="bell",
                    markdown=True
                )
            except Exception as bark_error:
                logger.warning(f"Bark notification failed: {bark_error}")
        
        return AnalyzeResponse(
            answer=response_text or f"Analysis of: {request.question}",
            stock_identified=None,
            sources=[],
            agents_used=[agent_name],
            timestamp=datetime.now().isoformat(),
            style=request.style or "buffett",
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
        ]
    )
