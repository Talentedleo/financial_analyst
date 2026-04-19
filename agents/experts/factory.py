"""
Expert Agent Factory - Dynamic agent creation by celebrity name

Usage:
    agent = create_expert_agent("warren_buffett")
    agent = create_expert_agent("cathie_wood")  # folder name = celebrity_name
    
The celebrity_name directly maps to skills folder name.
Falls back to warren_buffett if not found.
"""

from pathlib import Path
from typing import Dict, List, Optional

from google.adk.agents import Agent

from services.llm_service import get_llm_service
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


# Global skills folder path
SKILLS_FOLDER = Path(__file__).parent.parent.parent / "skills"
DEFAULT_CELEBRITY = "warren_buffett"


def _get_skill_path(celebrity_name: str) -> Path:
    """Get the skill folder path for a celebrity name."""
    return SKILLS_FOLDER / celebrity_name


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
    
    Args:
        celebrity_name: Folder name in skills/, e.g., 'warren_buffett', 'cathie_wood'
    
    Returns:
        Configured Agent instance
        
    If celebrity_name not found, defaults to warren_buffett.
    """
    # Fallback to default if not found
    skill_path = _get_skill_path(celebrity_name)
    if not skill_path.exists() or not (skill_path / "SKILL.md").exists():
        if celebrity_name != DEFAULT_CELEBRITY:
            print(f"Warning: Skill '{celebrity_name}' not found, using '{DEFAULT_CELEBRITY}'")
        celebrity_name = DEFAULT_CELEBRITY
        skill_path = _get_skill_path(celebrity_name)
    
    # Read SKILL.md content
    skill_md_path = skill_path / "SKILL.md"
    skill_content = skill_md_path.read_text(encoding='utf-8')
    
    # Extract name for display
    display_name = celebrity_name.replace('_', ' ').title()
    
    model = get_llm_service().model
    tools: List = stock_tools + news_tools + fundamentals_tools
    
    instruction = f"""You are {display_name}.

The skill defines your identity, thinking process, and communication style.
Read the SKILL.md content below carefully — it is the source of truth.

## SKILL.md Content

{skill_content}

## Execution Rules

- All reasoning MUST be derived from the skill content above
- All outputs MUST reflect the tone and framework of the skill
- Any response not aligned with the skill is invalid

## Workflow

1. Identify relevant rules from the skill
2. MUST use your tools to gather necessary data:
   - stock_tools: get real-time stock quotes and prices
   - news_tools: get company news and market news
   - fundamentals_tools: get company profile and financial metrics
3. Apply ONLY the skill logic to interpret the data
4. Respond in first person, matching the question's language

## Tools Available

- stock_tools: get_stock_quote, search_stocks, get_stock_candles
- news_tools: get_company_news, get_market_news
- fundamentals_tools: get_company_profile, get_company_peers, get_company_financials

## Failure Condition

If you cannot find guidance in the skill, say you do not have enough conviction to answer."""

    return Agent(
        name=f"{celebrity_name}_agent",
        model=model,
        description=f"{display_name} investment analyst",
        instruction=instruction,
        tools=tools
    )


def list_all_expert_agents() -> Dict[str, str]:
    """List all available expert agents (name -> description)."""
    celebrities = get_available_celebrities()
    return {name: name.replace('_', ' ').title() for name in celebrities}
