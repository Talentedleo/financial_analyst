"""
Greg Abel Expert Agent - Using ADK Skills
"""

from pathlib import Path
from google.adk.agents import Agent
from google.adk.tools.skill_toolset import SkillToolset
from google.adk.skills import load_skill_from_dir

from services.llm_service import get_llm_service
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


def create_greg_abel_agent() -> Agent:
    """Create Greg Abel expert agent using ADK Skills"""
    
    # Load skill using ADK's load_skill_from_dir
    skill_path = Path(__file__).parent.parent.parent / "skills" / "greg-abel"
    abel_skill = load_skill_from_dir(skill_path)
    
    # Create SkillToolset
    skill_toolset = SkillToolset(skills=[abel_skill])
    
    model = get_llm_service().model
    
    # Agent tools = data tools + skill toolset
    tools = stock_tools + news_tools + fundamentals_tools + [skill_toolset]
    
    return Agent(
        name="greg_abel_agent",
        model=model,
        description="Greg Abel expert - operational excellence, Berkshire perspective",
        instruction="You are Greg Abel, successor to Warren Buffett at Berkshire Hathaway and CEO of Berkshire Hathaway Energy. Analyze stocks focusing on: operational excellence, long-term thinking, culture, management quality, and Berkshire's investment criteria.",
        tools=tools
    )
