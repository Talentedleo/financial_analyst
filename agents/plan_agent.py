"""
Plan Agent - Root coordinator for financial analysis

Handles arbitrary user questions about stocks and investments.
Automatically identifies the stock/company and routes to appropriate expert agents.
"""

import os
import re
from typing import Optional, List, Dict, Any
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from services.llm_service import get_llm_service
from agents.experts import (
    create_buffett_agent,
    create_cathie_wood_agent,
    create_greg_abel_agent
)


class PlanAgent:
    """
    Root coordinator agent.
    
    Handles arbitrary user questions like:
    - "Should I invest in Apple?"
    - "What do you think about Tesla?"
    - "Analyze Bitcoin"
    - "Is Nvidia overvalued?"
    
    Automatically:
    1. Identifies stock/company from question
    2. Gets real-time data (if symbol found)
    3. Applies requested expert perspective(s)
    """
    
    def __init__(self):
        self._agent: Optional[Agent] = None
        self._runner: Optional[Runner] = None
        self._session_service: Optional[InMemorySessionService] = None
        self._expert_agents: Dict[str, Agent] = {}
    
    @property
    def agent(self) -> Agent:
        """Get or create plan agent"""
        if self._agent is None:
            # Create expert agents
            self._expert_agents = {
                "buffett": create_buffett_agent(),
                "cathie_wood": create_cathie_wood_agent(),
                "greg_abel": create_greg_abel_agent()
            }
            
            instruction = """You are a financial analysis coordinator.

You help users analyze stocks and investments by applying expert perspectives.

## Your Job

When a user asks a question like:
- "Should I invest in Apple?"
- "What do you think about Tesla?"
- "Analyze Bitcoin"
- "Is Nvidia overvalued?"

You should:
1. **Identify the stock/company** from their question
2. **Get relevant data** using your tools
3. **Apply expert perspective(s)** based on their request

## Available Expert Perspectives

### Warren Buffett (buffett)
- Value investing, moat analysis
- Key question: "Would I own this forever?"
- Look for: Stable businesses, pricing power, honest management

### Cathie Wood (cathie_wood)  
- Disruptive innovation, high-growth
- Key question: "Will this transform an industry?"
- Look for: Technology platforms, 5-year compounding

### Greg Abel (abel)
- Operational excellence, Berkshire perspective
- Key question: "Would Buffett be comfortable with this?"
- Look for: Culture, management, long-term thinking

## Style Preference

User may specify:
- "buffett" → Use Buffett perspective only
- "wood" → Use Cathie Wood perspective only
- "abel" → Use Greg Abel perspective only
- "all" or nothing → Use ALL perspectives

## How to Respond

Structure your response:

1. **Quick Summary** - 2-3 sentences on the stock
2. **Stock Identification** - Confirm what you identified
3. **Perspective Analysis** (based on style):
   - Buffett: Moat, intrinsic value, management
   - Wood: Innovation, TAM, 5-year thesis
   - Abel: Operations, culture, long-term viability
4. **Key Risks**
5. **Conclusion**

## Important

- Always try to get current stock data
- Be specific with numbers when available
- Match the expert's communication style
- Be honest about limitations

Use tools to get real data before analyzing!"""
            
            self._agent = Agent(
                name="plan_agent",
                model=get_llm_service().model,
                description="Financial analysis coordinator - handles arbitrary stock questions",
                instruction=instruction,
                sub_agents=list(self._expert_agents.values())
            )
        
        return self._agent
    
    @property
    def runner(self) -> Runner:
        """Get or create runner"""
        if self._runner is None:
            self._runner = Runner(
                agent=self.agent,
                app_name="financial_analyst",
                session_service=self.session_service
            )
        return self._runner
    
    @property
    def session_service(self) -> InMemorySessionService:
        """Get session service"""
        if self._session_service is None:
            self._session_service = InMemorySessionService()
        return self._session_service
    
    async def run(
        self,
        query: str,
        user_id: str = "user_1",
        session_id: str = "session_001"
    ) -> str:
        """Run analysis with user question"""
        from google.genai import types
        
        content = types.Content(
            role="user",
            parts=[types.Part(text=query)]
        )
        
        response_text = ""
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response():
                response_text = event.content.parts[0].text
        
        return response_text
    
    def get_expert(self, style: str) -> Optional[Agent]:
        """Get specific expert agent"""
        return self._expert_agents.get(style)


# Singleton
_plan_agent: Optional[PlanAgent] = None


def get_plan_agent() -> PlanAgent:
    """Get global plan agent instance"""
    global _plan_agent
    if _plan_agent is None:
        _plan_agent = PlanAgent()
    return _plan_agent
