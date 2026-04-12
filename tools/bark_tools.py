"""
Bark Notification Tools - Send push notifications to iOS devices

Bark is a simple iOS notification service that allows sending push notifications
via HTTP requests. Configure BARK_API_KEY and BARK_SERVER_URL in .env

Usage:
    1. Install Bark app on your iOS device
    2. Get your Bark push key from the app
    3. Configure BARK_API_KEY in .env (your device push key)
    4. Configure BARK_SERVER_URL in .env (default: https://api.day.app)
"""

import os
from typing import Optional
from google.adk.tools import FunctionTool


class BarkNotifier:
    """Service for sending push notifications via Bark"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        server_url: Optional[str] = None
    ):
        self.api_key = api_key or os.environ.get("BARK_API_KEY")
        self.server_url = server_url or os.environ.get("BARK_SERVER_URL", "https://api.day.app")
        
        if not self.api_key:
            raise ValueError("BARK_API_KEY not set in environment")
    
    def send(
        self,
        title: str,
        content: str,
        group: str = "Financial Analyst",
        sound: str = "alarm",
        icon: str = "https://img.icons8.com/ios-filled/100/000000/demo.png",
        url: str = "",
        level: str = "active"
    ) -> dict:
        """
        Send a push notification via Bark
        
        Args:
            title: Notification title (max 50 chars recommended)
            content: Notification body content
            group: Notification group/category (default: "Financial Analyst")
            sound: Notification sound (default: "alarm")
            icon: Notification icon URL
            url: URL to open when notification is tapped
            level: Interruption level - "passive", "active", "timeSensitive"
        
        Returns:
            dict with 'code' (0 = success) and 'message'
        """
        import requests
        
        endpoint = f"{self.server_url}/{self.api_key}"
        
        payload = {
            "title": title,
            "body": content,
            "group": group,
            "sound": sound,
            "icon": icon,
            "url": url,
            "level": level
        }
        
        response = requests.post(endpoint, json=payload)
        return response.json()
    
    def send_analysis(
        self,
        stock_symbol: str,
        analysis_result: str,
        style: str = "buffett"
    ) -> dict:
        """
        Send a stock analysis result as notification
        
        Args:
            stock_symbol: Stock symbol (e.g., "AAPL")
            analysis_result: Analysis summary to send
            style: Analysis style (buffett/wood/abel/all)
        
        Returns:
            dict with 'code' (0 = success) and 'message'
        """
        title = f"📈 {stock_symbol} Analysis ({style.upper()})"
        content = analysis_result[:500] + "..." if len(analysis_result) > 500 else analysis_result
        
        return self.send(
            title=title,
            content=content,
            group=f"Stock Analysis - {stock_symbol}",
            sound="alarm"
        )
    
    def send_alert(
        self,
        title: str,
        message: str,
        level: str = "timeSensitive"
    ) -> dict:
        """
        Send an urgent alert notification
        
        Args:
            title: Alert title
            message: Alert message
            level: Interruption level - "passive", "active", "timeSensitive"
        
        Returns:
            dict with 'code' (0 = success) and 'message'
        """
        return self.send(
            title=f"🚨 {title}",
            content=message,
            group="Alerts",
            sound="alarm",
            level=level
        )
    
    def send_daily_summary(
        self,
        summary: str,
        top_movers: list = None
    ) -> dict:
        """
        Send a daily market summary notification
        
        Args:
            summary: Daily summary text
            top_movers: List of top moving stocks
        
        Returns:
            dict with 'code' (0 = success) and 'message'
        """
        content = summary
        if top_movers:
            content += "\n\n📊 Top Movers:\n"
            for mover in top_movers[:5]:
                content += f"• {mover}\n"
        
        return self.send(
            title="📋 Daily Market Summary",
            content=content,
            group="Daily Summary",
            sound="morning"
        )


# Singleton instance
_notifier: Optional[BarkNotifier] = None


def get_bark_notifier() -> BarkNotifier:
    """Get or create global Bark notifier instance"""
    global _notifier
    if _notifier is None:
        _notifier = BarkNotifier()
    return _notifier


# ========== ADK Tool Functions ==========

def send_notification(
    title: str,
    content: str,
    group: str = "Financial Analyst",
    sound: str = "alarm",
    level: str = "active"
) -> dict:
    """
    Send a push notification to your iOS device via Bark.
    
    Use this tool to send notifications when:
    - A stock analysis is complete
    - You want to be alerted about important market events
    - A long-running analysis has finished
    
    Args:
        title: Notification title (keep it short, max 50 chars)
        content: Notification body content
        group: Notification group (default: "Financial Analyst")
        sound: Sound name - "alarm", "anticipate", "bell", "bird", etc.
        level: Interruption level - "passive", "active", "timeSensitive"
    
    Returns:
        dict with 'code' (0 = success) and 'message'
    """
    notifier = get_bark_notifier()
    return notifier.send(
        title=title,
        content=content,
        group=group,
        sound=sound,
        level=level
    )


def send_analysis_notification(
    stock_symbol: str,
    analysis_summary: str,
    style: str = "buffett"
) -> dict:
    """
    Send a stock analysis result as a push notification.
    
    Use this to receive analysis results directly on your phone.
    
    Args:
        stock_symbol: Stock symbol (e.g., "AAPL", "GOOGL")
        analysis_summary: Brief summary of the analysis (will be truncated to 500 chars)
        style: Analysis style used - "buffett", "wood", "abel", or "all"
    
    Returns:
        dict with 'code' (0 = success) and 'message'
    """
    notifier = get_bark_notifier()
    return notifier.send_analysis(
        stock_symbol=stock_symbol,
        analysis_result=analysis_summary,
        style=style
    )


def send_market_alert(
    title: str,
    message: str,
    urgent: bool = False
) -> dict:
    """
    Send an urgent market alert notification.
    
    Use this for time-sensitive alerts like:
    - Major market moves
    - Breaking financial news
    - Price alerts
    
    Args:
        title: Alert title
        message: Alert content
        urgent: If True, uses "timeSensitive" level for immediate delivery
    
    Returns:
        dict with 'code' (0 = success) and 'message'
    """
    notifier = get_bark_notifier()
    return notifier.send_alert(
        title=title,
        message=message,
        level="timeSensitive" if urgent else "active"
    )


# ========== ADK Tool Definitions ==========

send_notification_tool = FunctionTool(func=send_notification)
send_analysis_notification_tool = FunctionTool(func=send_analysis_notification)
send_market_alert_tool = FunctionTool(func=send_market_alert)

# Export all tools
bark_tools = [
    send_notification_tool,
    send_analysis_notification_tool,
    send_market_alert_tool
]
