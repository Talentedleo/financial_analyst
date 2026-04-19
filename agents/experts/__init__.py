"""
Expert Agents Module - Dynamic factory pattern

Old individual agent files (warren_buffett_agent.py, cathie_wood_agent.py, greg_abel_agent.py)
are deprecated. Use create_expert_agent(skill_name) instead.
"""

from .factory import (
    create_expert_agent,
    get_all_expert_agents,
    get_expert_agent_info,
    list_all_expert_agents,
)

__all__ = [
    "create_expert_agent",
    "get_all_expert_agents",
    "get_expert_agent_info",
    "list_all_expert_agents",
]
