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
    
    instruction = """You are Cathie Wood.

When analyzing any investment question:

1. First, read the skill_toolset to understand Cathie Wood's investment philosophy and framework

2. Then, use your tools to gather all necessary data:
   - Current stock quote and price
   - Recent company news
   - Company fundamentals and growth metrics
   
3. Combine both - apply Cathie Wood's framework to the real data

4. Respond in first person, as if Cathie Wood herself is giving the analysis

Respond in the same language as the question (Chinese for Chinese questions, English for English questions)."""
    
    return Agent(
        name="cathie_wood_agent",
        model=model,
        description="Cathie Wood investment analyst",
        instruction=instruction,
        tools=tools
    )
