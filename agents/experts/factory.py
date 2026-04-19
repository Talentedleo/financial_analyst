"""
Expert Agent Factory - Dynamically create agents based on skills folder

Each skill folder contains:
- SKILL.md: Rich agent definition with identity, examples, mental models
- references/: Additional reference documents

The factory reads SKILL.md directly and injects its content into the agent instruction.
"""

from pathlib import Path
from typing import Dict, List

from google.adk.agents import Agent

from services.llm_service import get_llm_service
from services.skill_loader import get_skill_loader, get_available_skills
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


def create_expert_agent(skill_name: str) -> Agent:
    """
    Create an expert agent dynamically based on skill name.
    
    Args:
        skill_name: Name of the skill folder (e.g., 'warren_buffett', 'cathie_wood')
    
    Returns:
        Configured Agent instance
    
    Raises:
        ValueError: If skill is not found or invalid
    """
    loader = get_skill_loader()
    available = loader.get_available_skills()
    
    if skill_name not in available:
        raise ValueError(
            f"Skill '{skill_name}' not found. Available skills: {available}"
        )
    
    # Load the full skill content from SKILL.md
    skill_context = loader.get_skill_context(skill_name)
    
    # Get skill meta for name/description
    skill = loader.load_skill(skill_name)
    meta = skill.get("meta", {})
    skill_display_name = meta.get('name', skill_name).replace('-', ' ').title()
    
    # Build the agent instruction
    instruction = f"""You are {skill_display_name}.

Your identity, thinking process, and communication style are defined in the skill content below.
Read it carefully — it is the source of truth for who you are and how you think.

## Your Skill Content

{skill_context}

## Execution Rules

- You MUST use your identity and philosophy from the skill content above
- All reasoning MUST be derived from the skill content
- All outputs MUST reflect the tone, framework, and examples in the skill content
- Any response not aligned with the skill content is invalid

## Workflow

1. Analyze the user's question
2. Identify relevant aspects of your philosophy from the skill content
3. MUST use your tools to gather necessary data:
   - stock_tools: get_quote, search_symbol, get_candles
   - news_tools: get_company_news, get_market_news
   - fundamentals_tools: get_company_profile, get_peers, get_financial_metrics
4. Apply ONLY your identity/framework from the skill content
5. Respond in first person, matching the question's language
6. Use the Expression DNA patterns (how you speak) from the skill content

## Tools Available

- stock_tools: get_stock_quote, search_stocks, get_stock_candles
- news_tools: get_company_news, get_market_news
- fundamentals_tools: get_company_profile, get_company_peers, get_company_financials

## Failure Condition

If the question falls outside your circle of competence as defined in the skill content, 
say so clearly and redirect to what you do know."""

    # Assemble tools
    model = get_llm_service().model
    tools: List = stock_tools + news_tools + fundamentals_tools
    
    # Create agent
    return Agent(
        name=f"{skill_name}_agent",
        model=model,
        description=f"{skill_display_name} expert analyst",
        instruction=instruction,
        tools=tools
    )


def get_all_expert_agents() -> Dict[str, Agent]:
    """Get all available expert agents dynamically."""
    agents = {}
    for skill_name in get_available_skills():
        try:
            agents[skill_name] = create_expert_agent(skill_name)
        except Exception as e:
            print(f"Warning: Could not create agent for skill '{skill_name}': {e}")
    return agents


def get_expert_agent_info(skill_name: str) -> Dict[str, str]:
    """Get basic info about an expert agent."""
    loader = get_skill_loader()
    try:
        skill = loader.load_skill(skill_name)
        meta = skill.get("meta", {})
        description = meta.get('description', '')[:100]
        return {
            "name": skill_name,
            "description": description or skill_name.replace('_', ' ').title()
        }
    except Exception:
        return {
            "name": skill_name,
            "description": skill_name.replace('_', ' ').title()
        }


def list_all_expert_agents() -> Dict[str, Dict[str, str]]:
    """List info for all available expert agents."""
    info = {}
    for skill_name in get_available_skills():
        info[skill_name] = get_expert_agent_info(skill_name)
    return info
