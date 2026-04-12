"""
Data Service - Yahoo Finance API (yfinance) Wrapper
"""

import os
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import yfinance as yf


class DataService:
    """Service for fetching financial data via Yahoo Finance (yfinance)"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time stock quote
        
        Returns:
            Dictionary with price data
        """
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            'c': info.get('currentPrice') or info.get('regularMarketPrice'),
            'd': info.get('regularMarketChange'),
            'dp': info.get('regularMarketChangePercent'),
            'h': info.get('dayHigh'),
            'l': info.get('dayLow'),
            'o': info.get('open'),
            'pc': info.get('previousClose'),
            't': int(datetime.now().timestamp())
        }
    
    def get_company_news(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get company-specific news
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            days: Number of days to look back
            
        Returns:
            List of news articles
        """
        ticker = yf.Ticker(symbol)
        news = ticker.news or []
        
        result = []
        for article in news:
            result.append({
                'headline': article.get('title', ''),
                'summary': article.get('summary', ''),
                'source': article.get('publisher', ''),
                'url': article.get('link', ''),
                'datetime': article.get('providerPublishTime', 0)
            })
        
        return result
    
    def get_market_news(self, category: str = "general") -> List[Dict[str, Any]]:
        """
        Get general market news.
        Note: yfinance doesn't support category filtering, returns general news.
        
        Args:
            category: News category (ignored for yfinance)
            
        Returns:
            List of market news articles
        """
        # yfinance doesn't have a general news endpoint separate from ticker news
        # Return tech/growth focused news via major indices
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
        all_news = []
        
        for symbol in tickers[:3]:  # Limit to 3 tickers
            ticker = yf.Ticker(symbol)
            news = ticker.news or []
            all_news.extend(news)
        
        # Sort by time
        all_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
        
        result = []
        for article in all_news[:20]:
            result.append({
                'headline': article.get('title', ''),
                'summary': article.get('summary', ''),
                'source': article.get('publisher', ''),
                'url': article.get('link', ''),
                'category': 'general'
            })
        
        return result
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Get company profile and fundamentals
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Company profile data
        """
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            'name': info.get('shortName', ''),
            'ticker': symbol,
            'exchange': info.get('exchange', ''),
            'finnhubIndustry': info.get('industry', ''),
            'logo': '',
            'weburl': info.get('website', ''),
            'country': info.get('country', ''),
            'currency': info.get('currency', 'USD'),
            'description': info.get('longBusinessSummary', '')[:500]
        }
    
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
            timeframe: 'D' (daily), 'W' (weekly), 'M' (monthly) - mapped to yfinance interval
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
        Search for stock symbols
        
        Args:
            query: Search query (company name or symbol)
            
        Returns:
            List of matching symbols
        """
        # yfinance doesn't have a direct search API
        # Use common tickers as fallback for demo
        search_lower = query.lower()
        
        # Try direct ticker first
        try:
            ticker = yf.Ticker(query.upper())
            info = ticker.info
            if info.get('regularMarketPrice'):
                return [{
                    'symbol': query.upper(),
                    'description': info.get('shortName', info.get('longName', query)),
                    'type': 'Equity'
                }]
        except Exception:
            pass
        
        # Return common tech stocks as demo results
        common_tickers = {
            'apple': ('AAPL', 'Apple Inc.'),
            'google': ('GOOGL', 'Alphabet Inc.'),
            'microsoft': ('MSFT', 'Microsoft Corporation'),
            'amazon': ('AMZN', 'Amazon.com Inc.'),
            'meta': ('META', 'Meta Platforms Inc.'),
            'tesla': ('TSLA', 'Tesla Inc.'),
            'nvidia': ('NVDA', 'NVIDIA Corporation'),
        }
        
        results = []
        for name, (symbol, full_name) in common_tickers.items():
            if search_lower in name or search_lower in full_name.lower():
                results.append({
                    'symbol': symbol,
                    'description': full_name,
                    'type': 'Equity'
                })
        
        return results
    
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
