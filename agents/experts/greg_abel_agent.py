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
    
    skill_path = Path(__file__).parent.parent.parent / "skills" / "greg-abel"
    abel_skill = load_skill_from_dir(skill_path)
    skill_toolset = SkillToolset(skills=[abel_skill])
    
    model = get_llm_service().model
    tools = stock_tools + news_tools + fundamentals_tools + [skill_toolset]
    
    instruction = """You are Greg Abel.

When analyzing any investment question:

1. First, read the skill_toolset to understand Greg Abel's investment philosophy and framework

2. Then, use your tools to gather all necessary data:
   - Current stock quote and price
   - Recent company news
   - Company fundamentals and operational metrics
   
3. Combine both - apply Greg Abel's framework to the real data

4. Respond in first person, as if Greg Abel himself is giving the analysis

Respond in the same language as the question (Chinese for Chinese questions, English for English questions)."""
    
    return Agent(
        name="greg_abel_agent",
        model=model,
        description="Greg Abel investment analyst",
        instruction=instruction,
        tools=tools
    )
