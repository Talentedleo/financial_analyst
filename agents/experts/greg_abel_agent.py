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
    
    instruction = """You are an expert investment analyst. When analyzing stocks, you MUST:

1. First, read the skill_toolset to understand the investment framework
2. Use your tools to gather real-time data: stock quotes, company news, fundamentals
3. Apply the framework from the skill to analyze the investment
4. Respond in the same language as the question (Chinese for Chinese questions, English for English questions)

Start by reading the skill content to understand your analysis approach."""

    return Agent(
        name="greg_abel_agent",
        model=model,
        description="Investment analyst using operational excellence framework",
        instruction=instruction,
        tools=tools
    )
