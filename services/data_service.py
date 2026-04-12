"""
Data Service - Finnhub + Yahoo Finance (yfinance) Integration

Strategy:
- Finnhub: Basic free features (quote, news, profile, search)
- yfinance: Premium features (real-time candles, historical data)
"""

import os
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import finnhub
import yfinance as yf


class DataService:
    """Service for fetching financial data via Finnhub + yfinance"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("FINNHUB_API_KEY")
        self._client = None
    
    @property
    def client(self) -> finnhub.Client:
        """Get or create Finnhub client"""
        if self._client is None:
            if not self.api_key:
                raise ValueError("FINNHUB_API_KEY not set in environment")
            self._client = finnhub.Client(api_key=self.api_key)
        return self._client
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time stock quote (from Finnhub)
        
        Returns:
            Dictionary with price data
        """
        return self.client.quote(symbol)
    
    def get_company_news(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get company-specific news (from Finnhub)
        
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
    
    def get_market_news(self, category: str = "general", min_id: int = 0) -> List[Dict[str, Any]]:
        """
        Get general market news (from Finnhub)
        
        Args:
            category: News category
            min_id: Minimum news ID for pagination
            
        Returns:
            List of market news articles
        """
        return self.client.general_news(category, min_id=min_id)
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Get company profile and fundamentals (from Finnhub)
        
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
        Get OHLCV candlestick data (from yfinance - Finnhub premium)
        
        Args:
            symbol: Stock symbol
            timeframe: 'D' (daily), 'W' (weekly), 'M' (monthly)
            days: Number of days of data
            
        Returns:
            Candlestick data
        """
        # Map timeframe to yfinance interval
        interval_map = {
            'D': '1d',
            'W': '1wk',
            'M': '1mo'
        }
        interval = interval_map.get(timeframe, '1d')
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date, end=end_date, interval=interval)
        
        return {
            'c': hist['Close'].tolist() if 'Close' in hist.columns else [],
            'h': hist['High'].tolist() if 'High' in hist.columns else [],
            'l': hist['Low'].tolist() if 'Low' in hist.columns else [],
            'o': hist['Open'].tolist() if 'Open' in hist.columns else [],
            'v': hist['Volume'].tolist() if 'Volume' in hist.columns else [],
            't': [int(d.timestamp()) for d in hist.index] if hasattr(hist.index, 'timestamp') else []
        }
    
    def search_symbol(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for stock symbols (from Finnhub)
        
        Args:
            query: Search query (company name or symbol)
            
        Returns:
            List of matching symbols
        """
        return self.client.symbol_lookup(query)
    
    def get_company_peers(self, symbol: str) -> List[str]:
        """
        Get peer companies for comparison (from Finnhub)
        
        Args:
            symbol: Stock symbol
            
        Returns:
            List of peer symbols
        """
        return self.client.peers(symbol)
    
    def get_company_financials(self, symbol: str) -> Dict[str, Any]:
        """
        Get basic financial metrics (from Finnhub)
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Financial metrics
        """
        metrics = self.client.company_basic_financials(symbol, 'all')
        return {
            "symbol": symbol,
            "metrics": metrics.get('metric', {}),
            "series": metrics.get('series', {}).get('annual', {})
        }
    
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
