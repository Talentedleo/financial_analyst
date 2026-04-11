"""
Financial Analyst AI Agent System - Main Entry Point
"""

import os
import asyncio
from google.adk.runners import Runner
from google.genai import types

from services import get_llm_service, get_data_service
from agents import create_agent


async def initialize():
    """Initialize services and agents"""
    # Initialize LLM service
    llm = get_llm_service()
    print(f"✓ LLM Service initialized: {llm.model_name}")
    
    # Initialize data service
    data = get_data_service()
    print("✓ Data Service initialized (Finnhub)")
    
    return llm, data


async def create_agents():
    """Create all agents"""
    # Plan Agent - Root coordinator
    plan_agent = create_agent(
        name="plan_agent",
        description="Coordinates financial analysis requests",
        instruction="""You are a financial analysis coordinator.
        
        You help users analyze stocks and investment opportunities using
        the perspectives of famous investors:
        - Warren Buffett: Value investing, moat analysis, long-term thinking
        - Cathie Wood: Disruptive innovation, growth investing
        - Greg Abel: Operational excellence, Berkshire perspective
        
        When users ask about stocks:
        1. Identify the stock/company
        2. Determine which perspective to use (or all)
        3. Provide analysis using that investor's framework
        
        Be concise but informative."""
    )
    
    return plan_agent


async def run_query(query: str, user_id: str = "user_1"):
    """Run a single query"""
    plan_agent = await create_agents()
    
    session_service = get_llm_service().model  # Placeholder
    
    # Create content
    content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )
    
    print(f"\nQuery: {query}")
    print("-" * 50)
    print("Note: Agent execution requires API keys and running session")
    print("-" * 50)


async def main():
    """Main entry point"""
    print("=" * 60)
    print("Financial Analyst AI Agent System")
    print("=" * 60)
    
    # Initialize services
    await initialize()
    
    # Demo query
    await run_query("Should I invest in Apple using Buffett's framework?")
    
    print("\n" + "=" * 60)
    print("Setup complete. Use FastAPI server for full functionality:")
    print("  uvicorn api.main:app --reload --port 8000")
    print("=" * 60)


if __name__ == "__main__":
    # Check for required API keys
    if not os.environ.get("MINIMAX_API_KEY"):
        print("⚠ Warning: MINIMAX_API_KEY not set")
    
    if not os.environ.get("FINNHUB_API_KEY"):
        print("⚠ Warning: FINNHUB_API_KEY not set")
    
    asyncio.run(main())
