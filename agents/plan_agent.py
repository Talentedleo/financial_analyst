"""
Plan Agent - Root coordinator for financial analysis
"""

import os
from typing import Optional, Literal
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agents.experts import (
    create_buffett_agent,
    create_cathie_wood_agent,
    create_greg_abel_agent
)


class PlanAgent:
    """
    Root coordinator agent that routes user requests to appropriate expert agents.
    
    Detects user intent and style preference, then delegates to:
    - buffett_agent: Value investing, moat analysis
    - cathie_wood_agent: Disruptive innovation, growth
    - greg_abel_agent: Operational excellence, Berkshire perspective
    """
    
    def __init__(self):
        self._agent: Optional[Agent] = None
        self._runner: Optional[Runner] = None
        self._session_service: Optional[InMemorySessionService] = None
        self._expert_agents = {}
    
    def _create_model(self) -> LiteLlm:
        """Create LLM model"""
        return LiteLlm(
            model="minimax/MiniMax-M2.1",
            api_key=os.environ.get("MINIMAX_API_KEY", ""),
            api_base="https://api.minimax.io/v1"
        )
    
    @property
    def agent(self) -> Agent:
        """Get or create plan agent"""
        if self._agent is None:
            # Create expert agents
            buffett = create_buffett_agent()
            cathie_wood = create_cathie_wood_agent()
            greg_abel = create_greg_abel_agent()
            
            self._expert_agents = {
                "buffett": buffett,
                "cathie_wood": cathie_wood,
                "greg_abel": greg_abel
            }
            
            instruction = """You are a financial analysis coordinator.

Your job is to understand user requests and provide multi-perspective analysis using three expert investors:

## Three Expert Perspectives

### 1. Warren Buffett (buffett_agent)
- Value investing, moat analysis
- Quote: "Be fearful when others are greedy"
- Focus: Stable businesses, long-term holding

### 2. Cathie Wood (cathie_wood_agent)
- Disruptive innovation, high-growth
- Quote: "We're being punished for being early and right"
- Focus: Transformative technologies, 5-year horizon

### 3. Greg Abel (greg_abel_agent)
- Operational excellence, Berkshire perspective
- Quote: "It will not change"
- Focus: Culture, management, long-term thinking

## How to Route Requests

**User says:** "Should I invest in Tesla?"
- Detect: Stock analysis request
- Determine style: If not specified, use ALL three perspectives
- Route to appropriate expert(s)

**Style preferences:**
- "buffett" → Use Warren Buffett perspective only
- "wood" → Use Cathie Wood perspective only  
- "abel" → Use Greg Abel perspective only
- "all" or unspecified → Use ALL three perspectives

## Response Format

Always structure your response with:
1. Quick summary (2-3 sentences)
2. Buffett perspective (if requested)
3. Cathie Wood perspective (if requested)
4. Greg Abel perspective (if requested)
5. Conclusion

Be concise but informative. Use the expert agents' tools to get current data.
"""
            
            self._agent = Agent(
                name="plan_agent",
                model=self._create_model(),
                description="Financial analysis coordinator",
                instruction=instruction,
                sub_agents=[buffett, cathie_wood, greg_abel]
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
        """Get or create session service"""
        if self._session_service is None:
            self._session_service = InMemorySessionService()
        return self._session_service
    
    async def run(self, query: str, user_id: str = "user_1", session_id: str = "session_001"):
        """Run the agent with user query"""
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
    
    def get_expert_agent(self, style: str) -> Optional[Agent]:
        """Get specific expert agent by style"""
        return self._expert_agents.get(style)


# Singleton instance
_plan_agent: Optional[PlanAgent] = None


def get_plan_agent() -> PlanAgent:
    """Get or create global plan agent"""
    global _plan_agent
    if _plan_agent is None:
        _plan_agent = PlanAgent()
    return _plan_agent
