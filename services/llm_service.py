"""
LLM Service - LiteLlm + MiniMax Integration
"""

import os
from typing import Optional
from google.adk.models.lite_llm import LiteLlm


class LLMService:
    """Service for managing LLM models via LiteLlm"""
    
    def __init__(
        self,
        model_name: str = "minimax/MiniMax-M2.7-highspeed",
        api_key: Optional[str] = None,
        api_base: str = "https://api.minimax.chat/v1"
    ):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        self.api_base = api_base or os.environ.get("MINIMAX_API_BASE", "https://api.minimax.chat/v1")
        
        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY not set in environment")
        
        self._model = None
    
    @property
    def model(self) -> LiteLlm:
        """Get or create LLM model instance"""
        if self._model is None:
            self._model = LiteLlm(
                model=self.model_name,
                api_key=self.api_key,
                api_base=self.api_base
            )
        return self._model
    
    def create_model(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.15,
        max_tokens: int = 2048
    ) -> LiteLlm:
        """
        Create a new model instance with custom parameters
        
        Args:
            model_name: Model name (default: minimax/MiniMax-M2.7-highspeed)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            LiteLlm model instance
        """
        return LiteLlm(
            model=model_name or self.model_name,
            api_key=self.api_key,
            api_base=self.api_base,
            temperature=temperature,
            max_tokens=max_tokens
        )


# Global singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create global LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def init_llm_service(
    model_name: str = "minimax/MiniMax-M2.7-highspeed",
    api_key: Optional[str] = None,
    api_base: Optional[str] = None
) -> LLMService:
    """Initialize global LLM service with custom settings"""
    global _llm_service
    _llm_service = LLMService(
        model_name=model_name,
        api_key=api_key,
        api_base=api_base
    )
    return _llm_service
