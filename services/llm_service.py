"""
LLM Service - LiteLlm + Multi-Provider Integration

Supports:
- MiniMax (default)
- DeepSeek

Provider priority (when both available): MiniMax > DeepSeek
"""

import os
from typing import Optional
from google.adk.models.lite_llm import LiteLlm


class LLMService:
    """Service for managing LLM models via LiteLlm with multi-provider support"""
    
    # Provider configurations
    PROVIDERS = {
        "minimax": {
            "model": "minimax/MiniMax-M2.7-highspeed",
            "api_key_env": "MINIMAX_API_KEY",
            "api_base_env": "MINIMAX_API_BASE",
            "default_base": "https://api.minimax.chat/v1"
        },
        "deepseek": {
            "model": "deepseek/deepseek-chat",
            "api_key_env": "DEEPSEEK_API_KEY",
            "api_base_env": "DEEPSEEK_API_BASE",
            "default_base": "https://api.deepseek.com/v1"
        }
    }
    
    def __init__(
        self,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None
    ):
        # Auto-detect provider if not specified
        if provider is None:
            provider = self._detect_provider()
        
        self.provider = provider
        config = self.PROVIDERS.get(provider, self.PROVIDERS["minimax"])
        
        self.model_name = model_name or config["model"]
        self.api_key = api_key or os.environ.get(config["api_key_env"])
        self.api_base = api_base or os.environ.get(
            config["api_base_env"], 
            config["default_base"]
        )
        
        if not self.api_key:
            raise ValueError(f"{config['api_key_env']} not set in environment")
        
        self._model = None
    
    @staticmethod
    def _detect_provider() -> str:
        """
        Detect which provider to use based on available API keys.
        Priority: MiniMax > DeepSeek
        """
        if os.environ.get("MINIMAX_API_KEY"):
            return "minimax"
        if os.environ.get("DEEPSEEK_API_KEY"):
            return "deepseek"
        raise ValueError("No LLM API key available (MINIMAX_API_KEY or DEEPSEEK_API_KEY)")
    
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
        temperature: float = 0.15
    ) -> LiteLlm:
        """
        Create a new model instance with custom parameters
        
        Args:
            model_name: Model name (default: current provider's default model)
            temperature: Sampling temperature
            
        Returns:
            LiteLlm model instance
        """
        return LiteLlm(
            model=model_name or self.model_name,
            api_key=self.api_key,
            api_base=self.api_base,
            temperature=temperature
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
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None
) -> LLMService:
    """Initialize global LLM service with custom settings"""
    global _llm_service
    _llm_service = LLMService(
        provider=provider,
        model_name=model_name,
        api_key=api_key,
        api_base=api_base
    )
    return _llm_service
