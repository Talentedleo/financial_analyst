"""
Expert Agent Factory - Dynamic agent creation using ADK Skills

Usage:
    agent = create_expert_agent("warren_buffett")
    
The celebrity_name maps directly to skills folder name.
Falls back to warren_buffett if not found.
"""

from pathlib import Path
from typing import List

from google.adk.agents import Agent
from google.adk.tools.skill_toolset import SkillToolset
from google.adk.skills import load_skill_from_dir

from services.llm_service import get_llm_service
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


# Enable snake_case skill name support (allows underscore folder names)
from google.adk.features import override_feature_enabled, FeatureName
override_feature_enabled(FeatureName.SNAKE_CASE_SKILL_NAME, True)


SKILLS_FOLDER = Path(__file__).parent.parent.parent / "skills"
DEFAULT_CELEBRITY = "warren_buffett"


def get_available_celebrities() -> List[str]:
    """Get list of available celebrity names (folder names with SKILL.md)."""
    if not SKILLS_FOLDER.exists():
        return []
    return sorted([
        d.name for d in SKILLS_FOLDER.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    ])


def create_expert_agent(celebrity_name: str) -> Agent:
    """
    Create an expert agent by celebrity name (folder name).
    Uses ADK's load_skill_from_dir + SkillToolset.
    """
    # Fallback to default if not found
    skill_path = SKILLS_FOLDER / celebrity_name
    if not skill_path.exists() or not (skill_path / "SKILL.md").exists():
        if celebrity_name != DEFAULT_CELEBRITY:
            print(f"Warning: Skill '{celebrity_name}' not found, using '{DEFAULT_CELEBRITY}'")
        celebrity_name = DEFAULT_CELEBRITY
        skill_path = SKILLS_FOLDER / celebrity_name
    
    # Load skill using ADK
    skill = load_skill_from_dir(skill_path)
    skill_toolset = SkillToolset(skills=[skill])
    
    model = get_llm_service().model
    tools: List = stock_tools + news_tools + fundamentals_tools + [skill_toolset]
    
    display_name = celebrity_name.replace('_', ' ').title()
    
    instruction = f"""You are {display_name}.

The skill_toolset defines your identity, thinking process, and communication style.
It is NOT optional.

Execution rules:

- All reasoning MUST be derived from the skill_toolset
- All outputs MUST reflect the tone and structure of the skill_toolset
- Any response not aligned with the skill_toolset is invalid

Workflow:

1. Identify relevant rules from skill_toolset
2. MUST use your tools to gather necessary data:
   - stock_tools: get real-time stock quotes and prices
   - news_tools: get company news and market news
   - fundamentals_tools: get company profile and financial metrics
3. Apply ONLY the skill_toolset logic to interpret the data
4. Respond in first person, matching the question's language

Failure condition:
If you cannot find guidance in the skill_toolset, say you do not have enough conviction to answer."""

    return Agent(
        name=f"{celebrity_name}_agent",
        model=model,
        description=f"{display_name} investment analyst",
        instruction=instruction,
        tools=tools
    )


def list_all_expert_agents() -> dict:
    """List all available expert agents."""
    celebrities = get_available_celebrities()
    return {name: {"description": name.replace('_', ' ').title()} for name in celebrities}
