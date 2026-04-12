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
    
    # Load skill using ADK's load_skill_from_dir
    skill_path = Path(__file__).parent.parent.parent / "skills" / "cathie-wood"
    wood_skill = load_skill_from_dir(skill_path)
    
    # Create SkillToolset
    skill_toolset = SkillToolset(skills=[wood_skill])
    
    model = get_llm_service().model
    
    # Agent tools = data tools + skill toolset
    tools = stock_tools + news_tools + fundamentals_tools + [skill_toolset]
    
    return Agent(
        name="cathie_wood_agent",
        model=model,
        description="Cathie Wood expert - disruptive innovation, high-growth investing",
        instruction="You are Cathie Wood, founder and CEO of ARK Invest, known for concentrated bets on transformative technologies. Analyze stocks focusing on: disruptive innovation, 5-year compounding thesis, technology platforms, and high-growth potential.",
        tools=tools
    )
