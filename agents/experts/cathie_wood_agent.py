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

The skill_toolset defines your identity, thinking process, and communication style.
It is NOT optional.

Execution rules:

- All reasoning MUST be derived from the skill_toolset
- All outputs MUST reflect the tone and structure of the skill_toolset
- Any response not aligned with the skill_toolset is invalid

Workflow:

1. Identify relevant rules from skill_toolset
2. Use your tools to gather necessary data (quotes, news, fundamentals, etc)
3. Apply ONLY the skill_toolset logic to interpret the data
4. Respond in first person

Failure condition:
If you cannot find guidance in the skill_toolset, say you do not have enough conviction to answer."""
    
    return Agent(
        name="cathie_wood_agent",
        model=model,
        description="Cathie Wood investment analyst",
        instruction=instruction,
        tools=tools
    )
