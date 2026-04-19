"""
Expert Agent Factory - Dynamic agent creation

Scans skills/ folder, reads SKILL.md directly for each skill,
and creates agents with skill content injected into instruction.
No ADK skill loading validation - supports any folder name.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from google.adk.agents import Agent

from services.llm_service import get_llm_service
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


def _discover_skills(skills_base_path: Path) -> Dict[str, Dict]:
    """Discover all skills by scanning folders and reading SKILL.md.
    
    Returns:
        Dict mapping skill_name (folder name) -> {folder_path, skill_md_content}
    """
    skills = {}
    
    if not skills_base_path.exists():
        return skills
    
    for folder in skills_base_path.iterdir():
        if not folder.is_dir():
            continue
        
        skill_md_path = folder / "SKILL.md"
        if not skill_md_path.exists():
            continue
        
        skill_name = folder.name  # Use folder name directly
        skill_md_content = skill_md_path.read_text(encoding='utf-8')
        
        skills[skill_name] = {
            'folder_path': folder,
            'skill_name': skill_name,
            'skill_md_content': skill_md_content,
        }
    
    return skills


# Global skills cache
_skills_cache: Optional[Dict[str, Dict]] = None


def _get_skills_map() -> Dict[str, Dict]:
    """Get or create the skills discovery map."""
    global _skills_cache
    if _skills_cache is None:
        skills_path = Path(__file__).parent.parent.parent / "skills"
        _skills_cache = _discover_skills(skills_path)
    return _skills_cache


def get_available_agents() -> List[str]:
    """Get list of available agent names (folder names)."""
    return sorted(_get_skills_map().keys())


def get_agent_info(skill_name: str) -> Dict[str, str]:
    """Get info about an agent by skill name."""
    skills = _get_skills_map()
    if skill_name not in skills:
        return {"name": skill_name, "description": ""}
    
    content = skills[skill_name].get('skill_md_content', '')
    # Extract description from frontmatter
    match = re.search(r'^---\s*\n.*?description:\s*(.+?)\n', content, re.DOTALL)
    description = match.group(1) if match else ""
    return {
        "name": skill_name,
        "description": description[:100] if description else skill_name
    }


def list_all_agents() -> Dict[str, Dict[str, str]]:
    """List all available agents."""
    skills = _get_skills_map()
    return {
        name: {"name": info['skill_name'], "description": info.get('description', '')}
        for name, info in skills.items()
    }


def create_expert_agent(skill_name: str) -> Agent:
    """
    Create an expert agent by skill name (folder name).
    
    Args:
        skill_name: Folder name, e.g., 'warren_buffett', 'cathie_wood'
    
    Returns:
        Configured Agent instance
    
    Raises:
        ValueError: If skill not found
    """
    skills = _get_skills_map()
    
    if skill_name not in skills:
        available = list(skills.keys())
        raise ValueError(
            f"Skill '{skill_name}' not found. Available: {available}"
        )
    
    skill_info = skills[skill_name]
    skill_md_content = skill_info['skill_md_content']
    
    # Extract name from frontmatter for display
    name_match = re.search(r'^---\s*\n.*?name:\s*(.+?)\n', skill_md_content, re.DOTALL)
    display_name = name_match.group(1).replace('-', ' ').replace('_', ' ').title() if name_match else skill_name.replace('_', ' ').title()
    
    # Extract skill content (after frontmatter)
    content_match = re.search(r'^---\s*\n.*?\n---\s*\n(.*)$', skill_md_content, re.DOTALL)
    skill_content = content_match.group(1).strip() if content_match else skill_md_content
    
    model = get_llm_service().model
    tools: List = stock_tools + news_tools + fundamentals_tools
    
    instruction = f"""You are {display_name}.

Your identity, thinking process, and communication style are defined in the skill content below.
Read it carefully — it is the source of truth for who you are and how you think.

## Your Skill Content

{skill_content}

## Execution Rules

- You MUST use your identity and philosophy from the skill content above
- All reasoning MUST be derived from the skill content
- All outputs MUST reflect the tone, framework, and examples in the skill content
- Any response not aligned with the skill content is invalid

## Workflow

1. Analyze the user's question
2. Identify relevant aspects of your philosophy from the skill content
3. MUST use your tools to gather necessary data:
   - stock_tools: get real-time stock quotes and prices
   - news_tools: get company news and market news
   - fundamentals_tools: get company profile and financial metrics
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
    
    return Agent(
        name=f"{skill_name}_agent",
        model=model,
        description=f"{display_name} investment analyst",
        instruction=instruction,
        tools=tools
    )


def create_all_agents() -> Dict[str, Agent]:
    """Create all available expert agents."""
    agents = {}
    for skill_name in get_available_agents():
        try:
            agents[skill_name] = create_expert_agent(skill_name)
        except Exception as e:
            print(f"Warning: Could not create agent for '{skill_name}': {e}")
    return agents
