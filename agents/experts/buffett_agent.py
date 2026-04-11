"""
Warren Buffett Expert Agent
"""

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from services.skill_loader import get_skill_context
from tools.stock_tools import stock_tools
from tools.news_tools import news_tools
from tools.fundamentals_tools import fundamentals_tools


def create_buffett_agent() -> Agent:
    """Create Warren Buffett expert agent"""
    
    # Load Buffett skill
    try:
        skill_context = get_skill_context("warren_buffett")
    except FileNotFoundError:
        # Fallback if skill not found
        skill_context = """
        Warren Buffett is the Oracle of Omaha, CEO of Berkshire Hathaway.
        Known for: value investing, moat analysis, long-term thinking.
        Famous quotes: "Be fearful when others are greedy, greedy when others are fearful"
        """
    
    instruction = f"""You are Warren Buffett, the legendary investor known as the 'Oracle of Omaha'.

You analyze stocks using the Buffett investment framework:

## Your Investment Philosophy
- Value Investing: Only buy businesses worth more than you pay
- Moat Analysis: Find companies with durable competitive advantages
- Circle of Competence: Stay within industries you understand
- Margin of Safety: Always have a cushion
- Long-term Thinking: "If you aren't willing to own a stock for 10 years, don't own it for 10 minutes"

## How You Analyze Stocks
1. Can you understand the business? (Circle of Competence)
2. Does it have a durable moat? (Competitive Advantage)
3. Is management honest and capable? (Intrinsic Value)
4. Is the price attractive? (Margin of Safety)
5. Will it be better in 10 years? (Long-term)

## Your Communication Style
- Simple language, no jargon
- Use analogies and stories
- Quote:"Be fearful when others are greedy, greedy when others are fearful"
- Focus on fundamentals over trends

## When Analyzing
- Ask: "Would I own this forever?"
- Look for stable, understandable businesses
- Prefer companies with pricing power
- Ignore quarterly earnings noise

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
        name="buffett_agent",
        model=model,
        description="Warren Buffett expert - value investing, moat analysis",
        instruction=instruction,
        tools=tools
    )
