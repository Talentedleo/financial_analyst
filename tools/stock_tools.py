"""
Stock Tools - Finnhub stock data tools for ADK
"""

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
        "c": candles.get('c', []),
        "h": candles.get('h', []),
        "l": candles.get('l', []),
        "o": candles.get('o', []),
        "v": candles.get('v', []),
        "t": candles.get('t', [])
    }


# ADK Tool definitions - new API
get_quote_tool = FunctionTool(func=get_stock_quote)
search_stocks_tool = FunctionTool(func=search_stocks)
get_candles_tool = FunctionTool(func=get_stock_candles)

# Export all tools
stock_tools = [get_quote_tool, search_stocks_tool, get_candles_tool]
