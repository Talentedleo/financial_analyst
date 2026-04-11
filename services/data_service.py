"""
Data Service - Finnhub API Wrapper
"""

import os
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import finnhub


class DataService:
    """Service for fetching financial data via Finnhub API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("FINNHUB_API_KEY")
        if not self.api_key:
            raise ValueError("FINNHUB_API_KEY not set in environment")
        self._client = None
    
    @property
    def client(self) -> finnhub.Client:
        """Get or create Finnhub client"""
        if self._client is None:
            self._client = finnhub.Client(api_key=self.api_key)
        return self._client
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time stock quote
        
        Returns:
            {'c': current, 'd': change, 'dp': percent change, ...}
        """
        return self.client.quote(symbol)
    
    def get_company_news(
        self,
        symbol: str,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Get company-specific news
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            days: Number of days to look back
            
        Returns:
            List of news articles
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.client.company_news(
            symbol,
            _from=start_date.strftime("%Y-%m-%d"),
            to=end_date.strftime("%Y-%m-%d")
        )
    
    def get_market_news(self, min_id: int = 0) -> List[Dict[str, Any]]:
        """
        Get general market news
        
        Args:
            min_id: Minimum news ID (for pagination)
            
        Returns:
            List of market news articles
        """
        return self.client.general_news('general', min_id=min_id)
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Get company profile and fundamentals
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Company profile data
        """
        return self.client.profile2(symbol=symbol)
    
    def get_candles(
        self,
        symbol: str,
        timeframe: str = 'D',
        days: int = 365
    ) -> Dict[str, Any]:
        """
        Get OHLCV candlestick data
        
        Args:
            symbol: Stock symbol
            timeframe: 'D' (daily), 'W' (weekly), 'M' (monthly)
            days: Number of days of data
            
        Returns:
            Candlestick data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.client.stock_candles(
            symbol, timeframe,
            int(start_date.timestamp()),
            int(end_date.timestamp())
        )
    
    def search_symbol(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for stock symbols
        
        Args:
            query: Search query (company name or symbol)
            
        Returns:
            List of matching symbols
        """
        return self.client.symbol_search(query)
    
    def format_quote(self, symbol: str) -> str:
        """Format quote as readable string"""
        quote = self.get_quote(symbol)
        return (
            f"{symbol}: ${quote['c']} "
            f"(Change: {quote['d']:.2f} / {quote['dp']:.2f}%)"
        )
    
    def format_news(self, news: List[Dict]) -> str:
        """Format news articles as readable string"""
        if not news:
            return "No news found."
        
        result = []
        for i, article in enumerate(news[:5], 1):
            result.append(
                f"{i}. {article.get('headline', 'No title')}\n"
                f"   Source: {article.get('source', 'Unknown')} | "
                f"URL: {article.get('url', 'N/A')}"
            )
        return "\n".join(result)


# Global singleton
_data_service: Optional[DataService] = None


def get_data_service() -> DataService:
    """Get or create global data service instance"""
    global _data_service
    if _data_service is None:
        _data_service = DataService()
    return _data_service
