"""
Stock Tools - Finnhub stock data tools for ADK
"""

import os
from typing import Dict, List, Any
from google.adk.tools import FunctionTool

from services.data_service import get_data_service


def get_stock_quote(symbol: str) -> Dict[str, Any]:
    """
    Get real-time stock quote including current price, change, volume.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
    
    Returns:
        Dictionary with price data
    """
    data_service = get_data_service()
    quote = data_service.get_quote(symbol)
    
    return {
        "symbol": symbol.upper(),
        "current_price": quote.get('c'),
        "change": quote.get('d'),
        "percent_change": quote.get('dp'),
        "high": quote.get('h'),
        "low": quote.get('l'),
        "open": quote.get('o'),
        "previous_close": quote.get('pc'),
        "timestamp": quote.get('t')
    }


def get_stock_price_formatted(symbol: str) -> str:
    """Get formatted stock price string"""
    data = get_stock_quote(symbol)
    return (
        f"{data['symbol']}: ${data['current_price']} "
        f"({data['percent_change']:+.2f}%)"
    )


def search_stocks(query: str) -> List[Dict[str, Any]]:
    """
    Search for stocks by company name or symbol.
    
    Args:
        query: Company name or stock symbol
    
    Returns:
        List of matching stocks
    """
    data_service = get_data_service()
    results = data_service.search_symbol(query)
    
    return [
        {
            "symbol": r.get('symbol'),
            "description": r.get('description'),
            "type": r.get('type')
        }
        for r in results
    ]


def get_stock_candles(
    symbol: str,
    timeframe: str = 'D',
    days: int = 30
) -> Dict[str, Any]:
    """
    Get OHLCV candlestick data for a stock.
    
    Args:
        symbol: Stock symbol
        timeframe: 'D' (daily), 'W' (weekly), 'M' (monthly)
        days: Number of days of data
    
    Returns:
        Candlestick data
    """
    data_service = get_data_service()
    candles = data_service.get_candles(symbol, timeframe, days)
    
    return {
        "symbol": symbol.upper(),
        "timeframe": timeframe,
        "c": candles.get('c', []),  # Close prices
        "h": candles.get('h', []),  # High prices
        "l": candles.get('l', []),  # Low prices
        "o": candles.get('o', []),  # Open prices
        "v": candles.get('v', []),  # Volume
        "t": candles.get('t', [])    # Timestamps
    }


# ADK Tool definitions
get_quote_tool = FunctionTool(
    name="get_stock_quote",
    description="Get real-time stock quote including current price, change, and volume",
    parameters={
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "Stock symbol (e.g., 'AAPL', 'GOOGL')"
            }
        },
        "required": ["symbol"]
    },
    function=get_stock_quote
)

search_stocks_tool = FunctionTool(
    name="search_stocks",
    description="Search for stocks by company name or symbol",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Company name or stock symbol to search"
            }
        },
        "required": ["query"]
    },
    function=search_stocks
)

get_candles_tool = FunctionTool(
    name="get_stock_candles",
    description="Get OHLCV candlestick data for stock price history",
    parameters={
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "Stock symbol"},
            "timeframe": {
                "type": "string",
                "description": "Timeframe: 'D' (daily), 'W' (weekly), 'M' (monthly)",
                "enum": ["D", "W", "M"],
                "default": "D"
            },
            "days": {
                "type": "integer",
                "description": "Number of days of data",
                "default": 30
            }
        },
        "required": ["symbol"]
    },
    function=get_stock_candles
)

# Export all tools
stock_tools = [get_quote_tool, search_stocks_tool, get_candles_tool]
