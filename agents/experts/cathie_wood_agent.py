"""
Cathie Wood Expert Agent - Using ADK Skills
"""

from pathlib import Path
from google.adk.agents import Agent
from google.adk.tools.skill_toolset import SkillToolset
from google.adk.skills import load_skill_from_dir

from services.llm_service import get_llm_service
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


def create_cathie_wood_agent() -> Agent:
    """Create Cathie Wood expert agent using ADK Skills"""
    
    skill_path = Path(__file__).parent.parent.parent / "skills" / "cathie-wood"
    wood_skill = load_skill_from_dir(skill_path)
    skill_toolset = SkillToolset(skills=[wood_skill])
    
    model = get_llm_service().model
    tools = stock_tools + news_tools + fundamentals_tools + [skill_toolset]
    
    instruction = """You are Cathie Wood. Follow this workflow:

1. Read the skill_toolset to learn the investment philosophy and communication style
2. Use your tools to gather necessary data (quotes, news, fundamentals)
3. Apply the skill's philosophy to analyze
4. Respond in first person, fully embracing the expert identity from the skill

Always follow the skill's guidance on how to analyze and communicate."""
    
    return Agent(
        name="cathie_wood_agent",
        model=model,
        description="Cathie Wood investment analyst",
        instruction=instruction,
        tools=tools
    )
