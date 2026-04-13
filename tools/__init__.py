"""
Tools Module - All ADK tools
"""

from .stock_tools import (
    get_stock_quote,
    search_stocks,
    get_stock_candles,
    stock_tools
)

from .news_tools import (
    get_company_news,
    get_market_news,
    news_tools
)

from .fundamentals_tools import (
    get_company_profile,
    get_company_peers,
    fundamentals_tools
)

from .bark_tools import (
    send_notification,
    send_analysis_notification,
    send_market_alert,
    bark_tools
)

# All tools combined
ALL_TOOLS = stock_tools + news_tools + fundamentals_tools + bark_tools

__all__ = [
    # Stock tools
    "get_stock_quote",
    "search_stocks",
    "get_stock_candles",
    "stock_tools",
    # News tools
    "get_company_news",
    "get_market_news",
    "news_tools",
    # Fundamentals tools
    "get_company_profile",
    "get_company_peers",
    "fundamentals_tools",
    # Bark notification tools
    "send_notification",
    "send_analysis_notification",
    "send_market_alert",
    "bark_tools",
    # Combined
    "ALL_TOOLS",
]
