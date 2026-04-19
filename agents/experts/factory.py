"""
Expert Agent Factory - Dynamically create agents based on skills folder
"""

import os
from pathlib import Path
from typing import Dict, Optional, List

from google.adk.agents import Agent
from google.adk.tools.skill_toolset import SkillToolset

from services.llm_service import get_llm_service
from services.skill_loader import get_skill_loader, get_available_skills
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


def _build_agent_instruction(skill_name: str, skill_context: str) -> str:
    """Build the instruction for an expert agent based on skill context."""
    return f"""You are {skill_name.replace('_', ' ').title()}.

{skill_context}

## Execution Rules

- All reasoning MUST be derived from your identity and philosophy above
- All outputs MUST reflect the tone and framework of your identity
- Any response not aligned with your identity is invalid

## Workflow

1. Analyze the user's question and identify relevant aspects of your philosophy
2. MUST use your tools to gather necessary data:
   - stock_tools: get_quote, search_symbol, get_candles
   - news_tools: get_company_news, get_market_news
   - fundamentals_tools: get_company_profile, get_peers, get_financial_metrics
3. Apply ONLY your identity/framework to interpret the data
4. Respond in first person, matching the question's language

## Tools Available

- stock_tools: get_quote, search_symbol, get_candles
- news_tools: get_company_news, get_market_news
- fundamentals_tools: get_company_profile, get_peers, get_financial_metrics

## Failure Condition

If you cannot find guidance in your identity/framework, say you do not have enough conviction to answer."""


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
    
    # Load skill context
    skill_context = loader.get_skill_context(skill_name)
    
    # Build instruction
    instruction = _build_agent_instruction(skill_name, skill_context)
    
    # Get skill path for ADK
    skills_path = Path(__file__).parent.parent.parent / "skills"
    skill_path = skills_path / skill_name
    
    # Try to load as ADK skill (if it has SKILL.md)
    skill_md_path = skill_path / "SKILL.md"
    skill_toolset = None
    
    if skill_md_path.exists():
        try:
            from google.adk.skills import load_skill_from_dir
            skill = load_skill_from_dir(skill_path)
            skill_toolset = SkillToolset(skills=[skill])
        except Exception as e:
            print(f"Warning: Could not load ADK skill from {skill_path}: {e}")
    
    # Assemble tools
    model = get_llm_service().model
    tools: List = stock_tools + news_tools + fundamentals_tools
    if skill_toolset:
        tools.append(skill_toolset)
    
    # Create agent
    return Agent(
        name=f"{skill_name}_agent",
        model=model,
        description=f"{skill_name.replace('_', ' ').title()} expert analyst",
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
        description = loader.get_skill_description(skill_name)
        return {
            "name": skill_name,
            "description": description
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
