"""
Bark Notification Tools - Send push notifications to iOS devices

Bark is an iOS notification service that supports:
- Markdown formatting (using 'markdown' field)
- Long message splitting (automatic chunking)
- Custom sounds, levels, icons, groups
- Time-sensitive notifications

Configure BARK_DEVICE_KEY and BARK_SERVER_URL in .env

Usage:
    1. Install Bark app on your iOS device
    2. Get your device key from the app
    3. Configure BARK_DEVICE_KEY in .env
    4. Configure BARK_SERVER_URL in .env (default: https://api.day.app)
"""

import os
import json
import logging
from enum import Enum
from typing import Optional, Union, List, Dict, Any
from google.adk.tools import FunctionTool

import requests


class BarkSound(Enum):
    """Bark supported notification sounds"""
    ALARM = "alarm"
    ANTICIPATE = "anticipate"
    BELL = "bell"
    BIRDSONG = "birdsong"
    BLOOM = "bloom"
    CALYPSO = "calypso"
    CHIME = "chime"
    COMPLETE = "complete"
    DESCENT = "descent"
    ELECTRIC = "electric"
    FANFARE = "fanfare"
    GLASS = "glass"
    HORNS = "horns"
    LADDER = "ladder"
    MINUET = "minuet"
    NEWSFLASH = "newsflash"
    NOIR = "noir"
    SHERWOODFOREST = "sherwoodforest"
    SPELL = "spell"
    SUSPENSE = "suspense"
    TELEGRAPH = "telegraph"
    TIPTOES = "tiptoes"
    TYPEWRITERS = "typewriters"
    UPDATE = "update"
    NONE = "None"  # Silent


class BarkLevel(Enum):
    """Message level (affects notification behavior)"""
    ACTIVE = "active"  # Default, lights up screen
    PASSIVE = "passive"  # Notification list only, no screen light
    TIME_SENSITIVE = "timeSensitive"  # Delivered during Focus mode


class BarkClient:
    """
    Bark message push client
    
    Supports Markdown mode and automatic long message splitting.
    """
    
    def __init__(
        self,
        device_key: Optional[str] = None,
        base_url: str = "https://api.day.app"
    ):
        self.device_key = device_key or os.environ.get("BARK_DEVICE_KEY")
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/{self.device_key}"
        
        if not self.device_key:
            raise ValueError("BARK_DEVICE_KEY not set in environment")
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json; charset=utf-8"
        })
    
    def _send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to Bark API"""
        try:
            response = self.session.post(
                self.endpoint,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Bark request failed: {e}")
            return {"code": 500, "message": f"Request failed: {str(e)}"}
        except json.JSONDecodeError as e:
            self.logger.error(f"Bark response parsing failed: {e}")
            return {"code": 500, "message": "Response parsing failed"}
    
    def send_message(
        self,
        body: str,
        title: Optional[str] = None,
        sound: Optional[Union[BarkSound, str]] = None,
        icon: Optional[str] = None,
        group: Optional[str] = None,
        url: Optional[str] = None,
        level: Optional[Union[BarkLevel, str]] = None,
        copy: Optional[str] = None,
        is_archive: Optional[bool] = None,
        badge: Optional[int] = None,
        markdown: bool = True
    ) -> Dict[str, Any]:
        """
        Send push notification message.
        
        Args:
            body: Message body (supports Markdown when markdown=True)
            title: Notification title
            sound: Notification sound (BarkSound enum or string)
            icon: Icon URL
            group: Notification group
            url: URL to open when tapped
            level: Notification level (BarkLevel enum or string)
            copy: Content to copy to clipboard
            is_archive: Auto-archive flag
            badge: Badge number
            markdown: If True, use 'markdown' field (recommended for formatting)
        
        Returns:
            API response with 'code' and 'message'
        """
        # Use markdown field for formatted content
        if markdown:
            payload = {"markdown": body}
        else:
            payload = {"body": body}
        
        if title:
            payload["title"] = title
        if sound:
            payload["sound"] = sound.value if isinstance(sound, BarkSound) else sound
        if icon:
            payload["icon"] = icon
        if group:
            payload["group"] = group
        if url:
            payload["url"] = url
        if level:
            payload["level"] = level.value if isinstance(level, BarkLevel) else level
        if copy:
            payload["copy"] = copy
        if is_archive is not None:
            payload["isArchive"] = 1 if is_archive else 0
        if badge is not None:
            payload["badge"] = badge
        
        mode = "markdown" if markdown else "body"
        self.logger.info(f"Sending Bark message ({mode}): {title}")
        
        return self._send_request(payload)
    
    def send_long_message(
        self,
        content: str,
        title: str,
        max_length: int = 2000,
        group: str = "long-message",
        sound: Optional[Union[BarkSound, str]] = None,
        markdown: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Send long messages by automatically splitting into chunks.
        
        Args:
            content: Full content to send
            title: Base title for all chunks
            max_length: Maximum characters per chunk (default 2000)
            group: Notification group
            sound: Sound for first chunk (silent for rest)
            markdown: Use markdown formatting
        
        Returns:
            List of API responses for each chunk
        """
        if len(content) <= max_length:
            return [self.send_message(
                body=content,
                title=title,
                sound=sound or BarkSound.BELL,
                group=group,
                markdown=markdown
            )]
        
        results = []
        chunks = [content[i:i + max_length] for i in range(0, len(content), max_length)]
        
        for i, chunk in enumerate(chunks):
            result = self.send_message(
                body=chunk,
                title=f"{title} ({i + 1}/{len(chunks)})",
                sound=sound if i == 0 else BarkSound.NONE,
                group=group,
                markdown=markdown
            )
            results.append(result)
        
        self.logger.info(f"Long message split into {len(chunks)} chunks")
        return results
    
    def send_alert(
        self,
        body: str,
        title: str = "Alert",
        sound: Union[BarkSound, str] = BarkSound.ALARM,
        level: Union[BarkLevel, str] = BarkLevel.TIME_SENSITIVE,
        markdown: bool = True
    ) -> Dict[str, Any]:
        """Send alert notification"""
        return self.send_message(
            body=body,
            title=title,
            sound=sound,
            level=level,
            markdown=markdown
        )
    
    def send_info(
        self,
        body: str,
        title: str = "Information",
        sound: Union[BarkSound, str] = BarkSound.BELL,
        level: Union[BarkLevel, str] = BarkLevel.ACTIVE,
        markdown: bool = True
    ) -> Dict[str, Any]:
        """Send regular information notification"""
        return self.send_message(
            body=body,
            title=title,
            sound=sound,
            level=level,
            markdown=markdown
        )


# Singleton instance
_bark_client: Optional[BarkClient] = None


def get_bark_client() -> BarkClient:
    """Get or create global Bark client instance"""
    global _bark_client
    if _bark_client is None:
        _bark_client = BarkClient()
    return _bark_client


# ========== ADK Tool Functions ==========

def send_notification(
    title: str,
    content: str,
    group: str = "Financial Analyst",
    sound: str = "bell",
    level: str = "active"
) -> dict:
    """
    Send a push notification to your iOS device via Bark.
    
    Supports Markdown formatting. Long content will be automatically split.
    
    Args:
        title: Notification title (short, max 50 chars)
        content: Message content (supports Markdown, will be split if > 2000 chars)
        group: Notification group (default: "Financial Analyst")
        sound: Sound name - "alarm", "bell", "birdsong", "calypso", etc.
        level: "active", "passive", or "timeSensitive"
    
    Returns:
        dict with 'code' (200 = success) and 'message'
    """
    client = get_bark_client()
    
    return client.send_message(
        body=content,
        title=title,
        group=group,
        sound=BarkSound(sound) if sound in [s.value for s in BarkSound] else sound,
        level=BarkLevel(level) if level in [l.value for l in BarkLevel] else level,
        markdown=True
    )


def send_analysis_notification(
    stock_symbol: str,
    analysis_summary: str,
    style: str = "buffett"
) -> dict:
    """
    Send a stock analysis result as a push notification.
    
    Automatically splits long content into multiple notifications.
    
    Args:
        stock_symbol: Stock symbol (e.g., "AAPL", "GOOGL")
        analysis_summary: Full analysis result (will be split if too long)
        style: Analysis style - "buffett", "wood", "abel", or "all"
    
    Returns:
        dict with 'code' (200 = success) and 'message'
    """
    client = get_bark_client()
    title = f"📈 {stock_symbol} ({style.upper()}) Analysis"
    
    return client.send_long_message(
        content=analysis_summary,
        title=title,
        group=f"Stock - {stock_symbol}",
        sound=BarkSound.ALARM,
        markdown=True
    )


def send_market_alert(
    title: str,
    message: str,
    urgent: bool = False
) -> dict:
    """
    Send an urgent market alert notification.
    
    Automatically splits long content into multiple notifications.
    
    Args:
        title: Alert title
        message: Alert content (supports Markdown, will be split if > 2000 chars)
        urgent: If True, uses "timeSensitive" level for immediate delivery
    
    Returns:
        dict with 'code' (200 = success) and 'message'
    """
    client = get_bark_client()
    
    return client.send_long_message(
        content=message,
        title=f"🚨 {title}",
        group="Alerts",
        sound=BarkSound.ALARM if urgent else BarkSound.BELL,
        markdown=True
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
