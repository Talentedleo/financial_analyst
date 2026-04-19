"""
Expert Agents Module - Dynamic factory by celebrity name

Usage:
    from agents import create_expert_agent, get_available_celebrities
    
    agent = create_expert_agent("warren_buffett")
    agents = get_available_celebrities()
"""

from .experts.factory import (
    create_expert_agent,
    get_available_celebrities,
    list_all_expert_agents,
)

__all__ = [
    "create_expert_agent",
    "get_available_celebrities",
    "list_all_expert_agents",
]
