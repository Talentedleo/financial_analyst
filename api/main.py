"""
FastAPI Application - Financial Analyst AI Agent
"""

import os
import asyncio
from typing import Optional, Literal
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents.plan_agent import get_plan_agent
from services import get_data_service


# Request/Response models
class AnalyzeRequest(BaseModel):
    question: str = Field(..., description="The investment question to analyze")
    style: Optional[Literal["buffett", "wood", "abel", "all"]] = Field(
        default="all",
        description="Analysis style: buffett, wood, abel, or all"
    )
    user_id: Optional[str] = Field(default="user_1")
    session_id: Optional[str] = Field(default=None)


class AnalyzeResponse(BaseModel):
    answer: str
    sources: list[dict]
    agents_used: list[str]
    timestamp: str
    style: str


class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")


class SearchResponse(BaseModel):
    results: list[dict]
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str


# Create FastAPI app
app = FastAPI(
    title="Financial Analyst AI Agent",
    description="Multi-agent system for professional-grade stock analysis using celebrity investor perspectives",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "name": "Financial Analyst AI Agent",
        "version": "1.0.0",
        "description": "Multi-agent system using Buffett, Cathie Wood, and Greg Abel perspectives"
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Analyze a stock or investment question.
    
    Uses the Plan Agent to route to appropriate expert agents
    (Buffett, Cathie Wood, Greg Abel) based on the style parameter.
    """
    try:
        # Get plan agent
        plan_agent = get_plan_agent()
        
        # Create session ID if not provided
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        # Run analysis
        answer = await plan_agent.run(
            query=request.question,
            user_id=request.user_id,
            session_id=session_id
        )
        
        # Determine which agents were used
        agents_used = ["plan_agent"]
        if request.style == "all":
            agents_used.extend(["buffett_agent", "cathie_wood_agent", "greg_abel_agent"])
        elif request.style == "buffett":
            agents_used.append("buffett_agent")
        elif request.style == "wood":
            agents_used.append("cathie_wood_agent")
        elif request.style == "abel":
            agents_used.append("greg_abel_agent")
        
        return AnalyzeResponse(
            answer=answer or "Analysis completed",
            sources=[],  # Sources from tool calls would go here
            agents_used=agents_used,
            timestamp=datetime.now().isoformat(),
            style=request.style or "all"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Search for real-time stock data and news.
    """
    try:
        data_service = get_data_service()
        
        # Try to determine if it's a symbol or company name
        query = request.query.strip().upper()
        
        # Check if it looks like a stock symbol
        if len(query) <= 5 and query.isalpha():
            # Treat as symbol
            quote = data_service.get_quote(query)
            news = data_service.get_company_news(query, days=7)
            
            results = [
                {
                    "type": "quote",
                    "symbol": query,
                    "price": quote.get('c'),
                    "change": quote.get('d'),
                    "percent_change": quote.get('dp')
                }
            ]
            
            for article in news[:5]:
                results.append({
                    "type": "news",
                    "headline": article.get('headline'),
                    "source": article.get('source'),
                    "url": article.get('url')
                })
        else:
            # Search for symbols
            search_results = data_service.search_symbol(query)
            results = [
                {
                    "type": "symbol",
                    "symbol": r.get('symbol'),
                    "description": r.get('description')
                }
                for r in search_results[:10]
            ]
        
        return SearchResponse(
            results=results,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents", response_model=dict)
async def list_agents():
    """List available agents"""
    return {
        "agents": [
            {
                "name": "plan_agent",
                "description": "Root coordinator"
            },
            {
                "name": "buffett_agent",
                "description": "Warren Buffett - Value investing"
            },
            {
                "name": "cathie_wood_agent",
                "description": "Cathie Wood - Disruptive innovation"
            },
            {
                "name": "greg_abel_agent",
                "description": "Greg Abel - Operational excellence"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
