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
        "description": profile.get('description', '')[:500]  # Limit length
    }


def get_company_financials(symbol: str) -> Dict[str, Any]:
    """
    Get basic financial metrics for a company.
    
    Args:
        symbol: Stock symbol
    
    Returns:
        Basic financial data
    """
    import finnhub
    
    data_service = get_data_service()
    client = data_service.client
    
    # Get basic financial metrics
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


def format_profile_text(profile: Dict) -> str:
    """Format company profile as readable text"""
    return (
        f"Company: {profile.get('name', 'N/A')}\n"
        f"Industry: {profile.get('industry', 'N/A')}\n"
        f"Exchange: {profile.get('exchange', 'N/A')}\n"
        f"Country: {profile.get('country', 'N/A')}\n"
        f"Website: {profile.get('weburl', 'N/A')}\n"
        f"\nDescription:\n{profile.get('description', 'N/A')[:300]}..."
    )


# ADK Tool definitions
get_company_profile_tool = FunctionTool(
    name="get_company_profile",
    description="Get company profile including industry, description, and basic info",
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
    function=get_company_profile
)

get_company_peers_tool = FunctionTool(
    name="get_company_peers",
    description="Get peer companies for comparison",
    parameters={
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "Stock symbol"
            }
        },
        "required": ["symbol"]
    },
    function=get_company_peers
)

# Export all tools
fundamentals_tools = [get_company_profile_tool, get_company_peers_tool]
