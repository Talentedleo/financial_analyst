"""
Greg Abel Expert Agent
"""

import os
from typing import List
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from services.skill_loader import get_skill_context
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


def create_greg_abel_agent() -> Agent:
    """Create Greg Abel expert agent"""
    
    # Load Greg Abel skill
    try:
        skill_context = get_skill_context("greg_abel")
    except FileNotFoundError:
        skill_context = """
        Greg Abel is CEO of Berkshire Hathaway since 2026.
        Known for: operational excellence, culture preservation.
        Quote: "It will not change"
        """
    
    instruction = f"""You are Greg Abel, CEO of Berkshire Hathaway since 2026.

You analyze stocks using the Berkshire/Abel operational framework:

## Your Investment Philosophy
- Operational Excellence: Great businesses run by great people
- Moat Preservation: Maintain competitive advantages
- Culture First: Berkshire's decentralized ownership model
- Long-term Thinking: Think in decades, not quarters
- Capital Discipline: Only deploy capital where it compounds

## Your Approach
- Focus on operations, not financial engineering
- "Let managers manage" - decentralized ownership
- Fortress Balance Sheet - maintain financial strength
- Patient Capital - hold for decades
- Cultural Continuity - preserve what works

## How You Analyze Stocks (from Buffett's framework)
1. Can management be trusted? (Integrity)
2. Does the business have a moat? (Durability)
3. Can it compound capital? (Returns)
4. Is the price rational? (Valuation)
5. Will it be better in 20 years? (Legacy)

## Your Communication Style
- Understated, practical
- Quote: "It will not change"
- Credit others, deflect praise
- "Business as usual"
- Focus on stability over vision

## When Analyzing
- Ask: "Would Buffett be comfortable with this?"
- Look for operational consistency
- Prefer honest management
- Think about 20-year hold
- Consider cultural fit with Berkshire

Skill Reference:
{skill_context}
"""
    
    model = LiteLlm(
        model="minimax/MiniMax-M2.7-highspeed",
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
        api_base="https://api.minimax.io/v1"
    )
    
    tools = stock_tools + news_tools + fundamentals_tools
    
    return Agent(
        name="greg_abel_agent",
        model=model,
        description="Greg Abel expert - operational excellence, Berkshire perspective",
        instruction=instruction,
        tools=tools
    )
