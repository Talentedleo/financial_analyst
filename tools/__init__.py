"""
Tools Module - All ADK tools
"""

from .finnhub_tools import (
    FinnhubTools,
    handle_get_quote,
    handle_get_company_news,
    handle_get_market_news
)

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

# All tools combined
ALL_TOOLS = stock_tools + news_tools + fundamentals_tools

__all__ = [
    # Finnhub wrapper
    "FinnhubTools",
    "handle_get_quote",
    "handle_get_company_news",
    "handle_get_market_news",
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
    # Combined
    "ALL_TOOLS",
]
