"""
Warren Buffett Expert Agent - Using ADK Skills
"""

from pathlib import Path
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.skill_toolset import SkillToolset
from google.adk.skills import load_skill_from_dir

from services.llm_service import get_llm_service
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


def create_buffett_agent() -> Agent:
    """Create Warren Buffett expert agent using ADK Skills"""
    
    # Load skill using ADK's load_skill_from_dir
    skill_path = Path(__file__).parent.parent.parent / "skills" / "warren-buffett"
    warren_skill = load_skill_from_dir(skill_path)
    
    # Create SkillToolset
    skill_toolset = SkillToolset(skills=[warren_skill])
    
    model = get_llm_service().model
    
    # Agent tools = data tools + skill toolset
    tools = stock_tools + news_tools + fundamentals_tools + [skill_toolset]
    
    return Agent(
        name="buffett_agent",
        model=model,
        description="Warren Buffett expert - value investing, moat analysis",
        instruction="You are Warren Buffett, the legendary investor known as the 'Oracle of Omaha'. Analyze stocks using the Buffett investment framework: value investing, moat analysis, circle of competence, margin of safety, and long-term thinking.",
        tools=tools
    )
