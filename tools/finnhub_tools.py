"""
Finnhub API Tools for Financial Analysis
"""

import os
from typing import Optional
import finnhub

class FinnhubTools:
    """Tools for fetching financial data via Finnhub API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("FINNHUB_API_KEY")
        if not self.api_key:
            raise ValueError("FINNHUB_API_KEY not set")
        self.client = finnhub.Client(api_key=self.api_key)
    
    def get_quote(self, symbol: str) -> dict:
        """
        Get real-time stock quote
        
        Returns: {'c': current, 'd': change, 'dp': percent change, ...}
        """
        return self.client.quote(symbol)
    
    def get_company_news(self, symbol: str, days: int = 7) -> list:
        """
        Get company-specific news
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            days: Number of days to look back
        
        Returns: List of news articles
        """
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.client.company_news(
            symbol,
            _from=start_date.strftime("%Y-%m-%d"),
            to=end_date.strftime("%Y-%m-%d")
        )
    
    def get_market_news(self) -> list:
        """
        Get general market news
        """
        return self.client.general_news('general', min_id=0)
    
    def get_company_profile(self, symbol: str) -> dict:
        """
        Get company profile and fundamentals
        """
        return self.client.company_profile2(symbol=symbol)
    
    def get_candles(self, symbol: str, timeframe: str = 'D') -> dict:
        """
        Get OHLCV candlestick data
        
        Args:
            symbol: Stock symbol
            timeframe: 'D' (daily), 'W' (weekly), 'M' (monthly)
        """
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        return self.client.stock_candles(
            symbol, timeframe,
            start_date.strftime('%s'),
            end_date.strftime('%s')
        )
    
    def search_symbol(self, query: str) -> list:
        """
        Search for stock symbols
        """
        return self.client.symbol_search(query)


# Tool instances for ADK
def get_finnhub_tools() -> list:
    """Get Finnhub tools for ADK agent"""
    tools = FinnhubTools()
    
    return [
        {
            "name": "get_stock_quote",
            "description": "Get real-time stock quote for a given symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol, e.g., AAPL"}
                },
                "required": ["symbol"]
            }
        },
        {
            "name": "get_company_news",
            "description": "Get recent news articles about a company",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol, e.g., AAPL"},
                    "days": {"type": "integer", "description": "Number of days to look back", "default": 7}
                },
                "required": ["symbol"]
            }
        },
        {
            "name": "get_market_news",
            "description": "Get general market news",
            "parameters": {}
        }
    ]


# ADK Tool Handlers
async def handle_get_quote(symbol: str) -> str:
    """Handler for get_stock_quote tool"""
    tools = FinnhubTools()
    quote = tools.get_quote(symbol)
    return f"{symbol}: ${quote['c']} ({quote['dp']}%)"

async def handle_get_company_news(symbol: str, days: int = 7) -> str:
    """Handler for get_company_news tool"""
    tools = FinnhubTools()
    news = tools.get_company_news(symbol, days)
    if not news:
        return f"No news found for {symbol}"
    
    result = [f"Recent news for {symbol}:"]
    for i, article in enumerate(news[:5], 1):
        result.append(f"{i}. {article['headline']}")
        result.append(f"   Source: {article['source']} | {article['datetime']}")
    return "\n".join(result)

async def handle_get_market_news() -> str:
    """Handler for get_market_news tool"""
    tools = FinnhubTools()
    news = tools.get_market_news()
    if not news:
        return "No market news found"
    
    result = ["General Market News:"]
    for i, article in enumerate(news[:5], 1):
        result.append(f"{i}. {article['headline']}")
        result.append(f"   Source: {article['source']}")
    return "\n".join(result)
