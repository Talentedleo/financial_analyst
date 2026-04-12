"""
News Tools - Finnhub news tools for ADK
"""

from typing import Dict, List, Any
from google.adk.tools import FunctionTool

from services.data_service import get_data_service


def get_company_news(
    symbol: str,
    days: int = 7,
    limit: int = 10,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get recent news articles about a specific company.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        days: Number of days to look back (default 7)
        limit: Maximum number of articles to return (default 10)
        offset: Offset for pagination (default 0)
    
    Returns:
        List of news articles
    """
    data_service = get_data_service()
    news = data_service.get_company_news(symbol, days)
    
    paginated = news[offset:offset + limit]
    
    return [
        {
            "headline": article.get('headline'),
            "summary": article.get('summary', '')[:200],
            "source": article.get('source'),
            "url": article.get('url'),
            "datetime": article.get('datetime')
        }
        for article in paginated
    ]


def get_market_news(
    category: str = "general",
    limit: int = 10,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get general market news.
    
    Args:
        category: News category - 'general', 'forex', 'crypto', 'merger'
        limit: Maximum number of articles to return (default 10)
        offset: Offset for pagination (default 0)
    
    Returns:
        List of market news articles
    """
    data_service = get_data_service()
    news = data_service.get_market_news(category)
    
    paginated = news[offset:offset + limit]
    
    return [
        {
            "headline": article.get('headline'),
            "summary": article.get('summary', '')[:200],
            "source": article.get('source'),
            "url": article.get('url'),
            "category": article.get('category')
        }
        for article in paginated
    ]


# ADK Tool definitions - new API
get_company_news_tool = FunctionTool(func=get_company_news)
get_market_news_tool = FunctionTool(func=get_market_news)

# Export all tools
news_tools = [get_company_news_tool, get_market_news_tool]
