"""
FastAPI Application - Financial Analyst AI Agent
"""

import os
import asyncio
from typing import Optional, Literal, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents.plan_agent import get_plan_agent
from services import get_data_service


# ============== Request/Response Models ==============

class AnalyzeRequest(BaseModel):
    """Request to analyze a stock or investment question"""
    question: str = Field(
        ...,
        description="Any stock or financial question (e.g., 'Should I invest in Apple?', 'What do you think about Tesla?', 'Analyze Bitcoin')"
    )
    style: Optional[Literal["buffett", "wood", "abel", "all"]] = Field(
        default="all",
        description="Analysis style: buffett (value), wood (growth), abel (operational), or all"
    )


class AnalyzeResponse(BaseModel):
    """Response from analysis"""
    answer: str = Field(..., description="Analysis from the expert perspective(s)")
    stock_identified: Optional[str] = Field(None, description="Stock/company identified from question")
    sources: List[dict] = Field(default_factory=list, description="Data sources used")
    agents_used: List[str] = Field(..., description="Expert agents used in analysis")
    timestamp: str = Field(default_factory=datetime.now().isoformat)
    style: str = Field(..., description="Analysis style applied")


class SearchRequest(BaseModel):
    """Request to search for financial data"""
    query: str = Field(
        ...,
        description="Any question, stock symbol, or company name (e.g., 'AAPL', 'Apple', 'Tesla stock price')"
    )


class SearchResponse(BaseModel):
    """Response from search"""
    results: List[dict] = Field(..., description="Search results")
    timestamp: str = Field(default_factory=datetime.now().isoformat)


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str


class AgentInfo(BaseModel):
    """Agent information"""
    name: str
    description: str


class AgentsListResponse(BaseModel):
    """List of available agents"""
    agents: List[AgentInfo]


# ============== FastAPI App ==============

app = FastAPI(
    title="Financial Analyst AI Agent",
    description="""
    **Multi-Agent Financial Analysis System**
    
    Ask any stock or financial question and get expert analysis from:
    - **Warren Buffett**: Value investing, moat analysis
    - **Cathie Wood**: Disruptive innovation, high-growth
    - **Greg Abel**: Operational excellence, Berkshire perspective
    
    ## Example Questions
    
    - "Should I invest in Apple?"
    - "What do you think about Tesla's robotaxi?"
    - "Analyze Bitcoin as an investment"
    - "Compare Nvidia using all perspectives"
    - "Is Amazon overvalued?"
    - "What would Buffett think of this stock?"
    
    Just ask naturally - the system will identify the stock and apply the right expert perspective!
    """,
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Endpoints ==============

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Financial Analyst AI Agent",
        "version": "1.0.0",
        "description": "Multi-expert stock analysis with Buffett, Cathie Wood, Greg Abel perspectives",
        "docs": "/docs",
        "endpoints": {
            "POST /analyze": "Analyze any stock/financial question",
            "POST /search": "Search stock data and news",
            "GET /agents": "List available expert agents",
            "GET /health": "Health check"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
async def analyze(request: AnalyzeRequest):
    """
    **Analyze any stock or financial question**
    
    Simply ask your question naturally! Examples:
    - "Should I invest in Apple?"
    - "What do you think about Tesla?"
    - "Analyze Bitcoin as an investment"
    - "Is Nvidia overvalued?"
    - "What would Buffett think of this?"
    
    The system will:
    1. Identify the stock/company from your question
    2. Get real-time data via Finnhub
    3. Apply the expert perspective(s) you requested
    """
    try:
        plan_agent = get_plan_agent()
        
        # Run the analysis
        answer = await plan_agent.run(
            query=request.question,
            user_id="api_user",
            session_id=f"session_{datetime.now().timestamp()}"
        )
        
        # Determine agents used
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
            stock_identified=None,  # Would be extracted by agent
            sources=[],  # Sources from tool calls
            agents_used=agents_used,
            timestamp=datetime.now().isoformat(),
            style=request.style or "all"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse, tags=["Search"])
async def search(request: SearchRequest):
    """
    **Search for stock data and news**
    
    Enter any stock symbol, company name, or financial query:
    - "AAPL" - Get Apple stock data
    - "Apple" - Search for Apple
    - "Tesla news" - Get Tesla news
    - "Nvidia stock price" - Get Nvidia data
    
    Returns stock quotes, news, and company information.
    """
    try:
        data_service = get_data_service()
        query = request.query.strip()
        
        results = []
        
        # Check if it looks like a stock symbol
        if len(query) <= 5 and query.replace('.', '').isalnum():
            # Treat as symbol
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
        
        # Get company news if symbol found or search
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
            # Search for the company
            search_results = data_service.search_symbol(query)
            for r in search_results[:5]:
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
async def list_agents():
    """List available expert agents"""
    return AgentsListResponse(
        agents=[
            AgentInfo(
                name="buffett_agent",
                description="Warren Buffett - Value investing, moat analysis, long-term thinking"
            ),
            AgentInfo(
                name="cathie_wood_agent",
                description="Cathie Wood - Disruptive innovation, high-growth, Big Ideas"
            ),
            AgentInfo(
                name="greg_abel_agent",
                description="Greg Abel - Operational excellence, Berkshire perspective"
            ),
            AgentInfo(
                name="plan_agent",
                description="Plan Agent - Automatically routes to appropriate expert(s)"
            )
        ]
    )


# ============== Run Server ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
