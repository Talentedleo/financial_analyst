"""
News Tools - Finnhub news tools for ADK
"""

from typing import Dict, List, Any
from google.adk.tools import FunctionTool

from services.data_service import get_data_service


def get_company_news(symbol: str, days: int = 7) -> List[Dict[str, Any]]:
    """
    Get recent news articles about a specific company.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        days: Number of days to look back (default 7)
    
    Returns:
        List of news articles
    """
    data_service = get_data_service()
    news = data_service.get_company_news(symbol, days)
    
    return [
        {
            "headline": article.get('headline'),
            "summary": article.get('summary'),
            "source": article.get('source'),
            "url": article.get('url'),
            "datetime": article.get('datetime')
        }
        for article in news[:10]  # Limit to 10 most recent
    ]


def get_market_news() -> List[Dict[str, Any]]:
    """
    Get general market news.
    
    Returns:
        List of market news articles
    """
    data_service = get_data_service()
    news = data_service.get_market_news()
    
    return [
        {
            "headline": article.get('headline'),
            "summary": article.get('summary'),
            "source": article.get('source'),
            "url": article.get('url'),
            "category": article.get('category')
        }
        for article in news[:10]
    ]


def format_news_as_text(news: List[Dict]) -> str:
    """Format news list as readable text"""
    if not news:
        return "No news found."
    
    lines = []
    for i, article in enumerate(news, 1):
        lines.append(f"{i}. {article.get('headline', 'No title')}")
        if article.get('source'):
            lines.append(f"   Source: {article['source']}")
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
            }
        },
        "required": ["symbol"]
    },
    function=get_company_news
)

get_market_news_tool = FunctionTool(
    name="get_market_news",
    description="Get general market news and financial headlines",
    parameters={},
    function=get_market_news
)

# Export all tools
news_tools = [get_company_news_tool, get_market_news_tool]
