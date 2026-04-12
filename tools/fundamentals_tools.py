"""
Fundamentals Tools - Finnhub fundamental data for ADK
"""

from typing import Dict, Any
from google.adk.tools import FunctionTool

from services.data_service import get_data_service


def get_company_profile(symbol: str) -> Dict[str, Any]:
    """
    Get company profile including industry, description, executives.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL')
    
    Returns:
        Company profile data
    """
    data_service = get_data_service()
    profile = data_service.get_company_profile(symbol)
    
    return {
        "name": profile.get('name'),
        "ticker": profile.get('ticker'),
        "exchange": profile.get('exchange'),
        "industry": profile.get('finnhubIndustry'),
        "logo": profile.get('logo'),
        "weburl": profile.get('weburl'),
        "country": profile.get('country'),
        "currency": profile.get('currency'),
        "description": profile.get('description', '')[:500]
    }


def get_company_financials(symbol: str) -> Dict[str, Any]:
    """
    Get basic financial metrics for a company.
    
    Args:
        symbol: Stock symbol
    
    Returns:
        Basic financial data
    """
    data_service = get_data_service()
    client = data_service.client
    
    metrics = client.company_basic_financials(symbol, 'all')
    
    return {
        "symbol": symbol,
        "metrics": metrics.get('metric', {}),
        "series": metrics.get('series', {}).get('annual', {})
    }


def get_company_peers(symbol: str) -> Dict[str, Any]:
    """
    Get peer companies for comparison.
    
    Args:
        symbol: Stock symbol
    
    Returns:
        List of peer symbols
    """
    data_service = get_data_service()
    client = data_service.client
    
    peers = client.peers(symbol)
    
    return {
        "symbol": symbol,
        "peers": peers
    }


# ADK Tool definitions - new API
get_company_profile_tool = FunctionTool(func=get_company_profile)
get_company_peers_tool = FunctionTool(func=get_company_peers)
get_company_financials_tool = FunctionTool(func=get_company_financials)

# Export all tools
fundamentals_tools = [
    get_company_profile_tool,
    get_company_peers_tool,
    get_company_financials_tool
]
