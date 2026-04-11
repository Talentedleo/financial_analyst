"""
Financial Analyst AI Agent System
Main entry point
"""

import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Initialize model (MiniMax via LiteLlm)
model = LiteLlm(
    model="minimax/MiniMax-M2.1",
    api_key=os.environ.get("MINIMAX_API_KEY", ""),
    api_base="https://api.minimax.io/v1"
)

# Create session service
session_service = InMemorySessionService()

# Create runner
runner = Runner(
    agent=None,  # Will be set when agents are defined
    app_name="financial_analyst",
    session_service=session_service
)

async def run_agent(query: str, user_id: str = "user_1", session_id: str = "session_001"):
    """Run the agent with user query"""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response():
            return event.content.parts[0].text
    
    return None

if __name__ == "__main__":
    print("Financial Analyst AI Agent System")
    print("Use FastAPI server: uvicorn api.main:app --reload")
