"""
Base Agent - Foundation for all agents
"""

import os
from typing import Optional, List, Dict, Any
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService


class BaseAgent:
    """Base class for all agents in the Financial Analyst system"""
    
    def __init__(
        self,
        name: str,
        description: str,
        instruction: str,
        model_name: str = "minimax/MiniMax-M2.1",
        tools: Optional[List] = None,
        sub_agents: Optional[List['BaseAgent']] = None
    ):
        self.name = name
        self.description = description
        self.instruction = instruction
        self.model_name = model_name
        self.tools = tools or []
        self.sub_agents = sub_agents or []
        self._agent = None
        self._session_service = None
    
    def _create_model(self) -> LiteLlm:
        """Create LLM model"""
        return LiteLlm(
            model=self.model_name,
            api_key=os.environ.get("MINIMAX_API_KEY", ""),
            api_base="https://api.minimax.io/v1"
        )
    
    @property
    def agent(self) -> Agent:
        """Get or create ADK Agent"""
        if self._agent is None:
            # Convert sub-agents if they are BaseAgent instances
            adk_sub_agents = None
            if self.sub_agents:
                adk_sub_agents = [
                    sa.agent if isinstance(sa, BaseAgent) else sa
                    for sa in self.sub_agents
                ]
            
            self._agent = Agent(
                name=self.name,
                model=self._create_model(),
                description=self.description,
                instruction=self.instruction,
                tools=self.tools,
                sub_agents=adk_sub_agents
            )
        return self._agent
    
    @property
    def session_service(self) -> InMemorySessionService:
        """Get session service"""
        if self._session_service is None:
            self._session_service = InMemorySessionService()
        return self._session_service
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent config to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "model": self.model_name,
            "tools_count": len(self.tools),
            "sub_agents_count": len(self.sub_agents)
        }


def create_agent(
    name: str,
    description: str,
    instruction: str,
    model_name: str = "minimax/MiniMax-M2.1",
    tools: Optional[List] = None
) -> Agent:
    """
    Factory function to create an agent quickly
    
    Args:
        name: Agent name
        description: Agent description
        instruction: System instruction
        model_name: Model to use
        tools: List of tools
        
    Returns:
        Configured ADK Agent
    """
    model = LiteLlm(
        model=model_name,
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
        api_base="https://api.minimax.io/v1"
    )
    
    return Agent(
        name=name,
        model=model,
        description=description,
        instruction=instruction,
        tools=tools or []
    )
