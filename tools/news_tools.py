"""
News Tools - Finnhub news tools for ADK
"""

from typing import Dict, List, Any, Optional
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
    
    # Apply pagination
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
    
    # Apply pagination
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


def format_news_as_text(news: List[Dict], show_summary: bool = False) -> str:
    """Format news list as readable text"""
    if not news:
        return "No news found."
    
    lines = []
    for i, article in enumerate(news, 1):
        lines.append(f"{i}. {article.get('headline', 'No title')}")
        if article.get('source'):
            lines.append(f"   Source: {article['source']}")
        if show_summary and article.get('summary'):
            lines.append(f"   Summary: {article['summary']}")
        if article.get('url'):
            lines.append(f"   URL: {article['url']}")
        lines.append("")
    
    return "\n".join(lines)


# ADK Tool definitions
get_company_news_tool = FunctionTool(
    name="get_company_news",
    description="Get recent news articles about a specific company",
    parameters={
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "Stock symbol (e.g., 'AAPL', 'GOOGL')"
            },
            "days": {
                "type": "integer",
                "description": "Number of days to look back",
                "default": 7
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of articles to return",
                "default": 10
            },
            "offset": {
                "type": "integer",
                "description": "Offset for pagination",
                "default": 0
            }
        },
        "required": ["symbol"]
    },
    function=get_company_news
)

get_market_news_tool = FunctionTool(
    name="get_market_news",
    description="Get general market news and financial headlines",
    parameters={
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "News category: 'general', 'forex', 'crypto', 'merger'",
                "default": "general"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of articles to return",
                "default": 10
            },
            "offset": {
                "type": "integer",
                "description": "Offset for pagination",
                "default": 0
            }
        },
        "required": []
    },
    function=get_market_news
)

# Export all tools
news_tools = [get_company_news_tool, get_market_news_tool]
