"""
Expert Agent Factory - Dynamic agent creation using ADK Skills

Each skill folder contains:
- SKILL.md: ADK skill definition with YAML frontmatter (name, description, triggers)
- references/: Additional reference documents

Factory scans skills folder, reads SKILL.md to get the skill's name,
then creates agents using ADK's load_skill_from_dir + SkillToolset.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from google.adk.agents import Agent
from google.adk.tools.skill_toolset import SkillToolset
from google.adk.skills import load_skill_from_dir

from services.llm_service import get_llm_service
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


def _discover_skills(skills_base_path: Path) -> Dict[str, Dict]:
    """Discover all skills by scanning folders and reading SKILL.md names.
    
    Returns:
        Dict mapping skill_name (from SKILL.md) -> {folder_path, skill_name, description}
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
        
        # Read SKILL.md to get the skill's name
        content = skill_md_path.read_text(encoding='utf-8')
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            continue
        
        import yaml
        try:
            meta = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        
        skill_name = meta.get('name')  # e.g., 'warren-buffett'
        if not skill_name:
            continue
        
        skills[skill_name] = {
            'folder_path': folder,
            'skill_name': skill_name,
            'description': meta.get('description', ''),
            'triggers': meta.get('triggers', []),
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
    """Get list of available agent names (from SKILL.md names)."""
    return sorted(_get_skills_map().keys())


def get_agent_info(skill_name: str) -> Dict[str, str]:
    """Get info about an agent by skill name."""
    skills = _get_skills_map()
    if skill_name not in skills:
        return {"name": skill_name, "description": ""}
    return {
        "name": skill_name,
        "description": skills[skill_name].get('description', '')[:100]
    }


def list_all_agents() -> Dict[str, Dict[str, str]]:
    """List all available agents."""
    skills = _get_skills_map()
    return {
        name: {"name": info['skill_name'], "description": info.get('description', '')[:100]}
        for name, info in skills.items()
    }


def create_expert_agent(skill_name: str) -> Agent:
    """
    Create an expert agent by skill name.
    
    Args:
        skill_name: Name from SKILL.md, e.g., 'warren-buffett', 'cathie-wood'
    
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
    folder_path = skill_info['folder_path']
    
    # Use ADK's official skill loading
    try:
        skill = load_skill_from_dir(folder_path)
        skill_toolset = SkillToolset(skills=[skill])
    except Exception as e:
        raise RuntimeError(f"Failed to load skill from {folder_path}: {e}")
    
    model = get_llm_service().model
    tools: List = stock_tools + news_tools + fundamentals_tools + [skill_toolset]
    
    # Extract display name for instruction
    display_name = skill_name.replace('-', ' ').title()
    
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
    
    # Create agent with folder name as agent name identifier
    agent_name = skill_name.replace('-', '_') + '_agent'
    
    return Agent(
        name=agent_name,
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
