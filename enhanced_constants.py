"""
Enhanced constants and configuration for advanced LLM integration.

This module extends the original constants to support:
- Multiple LLM providers
- Advanced optimization strategies
- Web search capabilities
- GEPA-ACE configuration
"""

from typing import Dict, List
from constants import *

# Advanced LLM Provider Configuration
ADVANCED_MODELS: Dict[str, Dict[str, str]] = {
    "Ollama Gemma 3 4B": {
        "provider": "ollama",
        "model": "gemma3:4b",
        "capabilities": ["text_generation", "local_processing", "fast_inference"]
    },
    "Ollama Code Llama": {
        "provider": "ollama", 
        "model": "codellama:latest",
        "capabilities": ["text_generation", "code_generation", "local_processing"]
    },
    "Ollama Mistral": {
        "provider": "ollama",
        "model": "mistral:latest", 
        "capabilities": ["text_generation", "reasoning", "local_processing"]
    },
    "Perplexity Sonar Small": {
        "provider": "perplexity",
        "model": "llama-3.1-sonar-small-128k-online",
        "capabilities": ["web_search", "real_time_info", "text_generation"]
    },
    "Perplexity Sonar Large": {
        "provider": "perplexity",
        "model": "llama-3.1-sonar-large-128k-online", 
        "capabilities": ["web_search", "real_time_info", "advanced_reasoning"]
    },
    "Claude Sonnet 4.5": {
        "provider": "openrouter",
        "model": "openrouter/anthropic/claude-sonnet-4.5",
        "capabilities": ["text_generation", "advanced_reasoning", "creative_writing"]
    }
}

# Optimization Strategies
OPTIMIZATION_STRATEGIES = {
    "local_fast": {
        "name": "Local Fast",
        "description": "Use local Ollama models for fast, private processing",
        "providers": ["ollama"],
        "use_web_search": False,
        "use_context_optimization": True
    },
    "web_enhanced": {
        "name": "Web Enhanced", 
        "description": "Use Perplexity for real-time web information and context",
        "providers": ["perplexity"],
        "use_web_search": True,
        "use_context_optimization": True
    },
    "hybrid_balanced": {
        "name": "Hybrid Balanced",
        "description": "Automatically select best provider based on task requirements",
        "providers": ["ollama", "perplexity", "openrouter"],
        "use_web_search": True,
        "use_context_optimization": True
    },
    "creative_mode": {
        "name": "Creative Mode",
        "description": "Use Claude for creative and engaging tweet generation",
        "providers": ["openrouter"],
        "use_web_search": False,
        "use_context_optimization": True
    }
}

# GEPA-ACE Configuration
GEPA_ACE_CONFIG = {
    "max_context_length": 2000,
    "compression_ratio": 0.7,
    "cache_size": 100,
    "optimization_threshold": 0.8
}

# Web Search Configuration
WEB_SEARCH_CONFIG = {
    "max_search_results": 3,
    "search_timeout": 10,
    "cache_duration": 3600,  # 1 hour
    "min_keyword_length": 3,
    "max_keywords": 5
}

# Ax LLM Configuration
AX_LLM_CONFIG = {
    "performance_tracking": True,
    "auto_routing": True,
    "fallback_provider": "ollama_gemma3_4b",
    "max_retries": 3,
    "timeout": 30
}

# Enhanced UI Configuration
ENHANCED_UI_CONFIG = {
    "show_provider_status": True,
    "show_optimization_stats": True,
    "show_web_context": True,
    "show_performance_metrics": True,
    "provider_selector": True,
    "strategy_selector": True
}

# Advanced Error Messages
ADVANCED_ERROR_MESSAGES = {
    "OLLAMA_NOT_AVAILABLE": "Ollama is not running. Please start Ollama or use a different provider.",
    "PERPLEXITY_API_ERROR": "Perplexity API error. Check your API key and internet connection.",
    "WEB_SEARCH_FAILED": "Web search failed. Continuing without web context.",
    "CONTEXT_OPTIMIZATION_FAILED": "Context optimization failed. Using original context.",
    "HYBRID_ROUTING_FAILED": "Hybrid routing failed. Using fallback provider.",
    "NO_PROVIDERS_AVAILABLE": "No LLM providers are available. Please check your configuration."
}

# Performance Metrics Configuration
PERFORMANCE_METRICS = {
    "track_response_time": True,
    "track_success_rate": True,
    "track_token_usage": True,
    "track_cost": True,
    "metrics_history_size": 100
}

# Enhanced Categories for Web-Enhanced Evaluation
ENHANCED_CATEGORIES = [
    "Engagement potential - how likely users are to like, retweet, or reply based on current trends",
    "Clarity and readability - how easy the tweet is to understand and digest quickly",
    "Emotional impact - how well the tweet evokes feelings or reactions from the audience",
    "Relevance to target audience - how well it resonates with intended readers and current discussions",
    "Timeliness and trend awareness - how well it incorporates current events and trending topics",
    "Viral potential - likelihood of being shared widely based on current social media patterns"
]

# Provider-Specific Settings
PROVIDER_SETTINGS = {
    "ollama": {
        "base_url": "http://localhost:11434",
        "timeout": 30,
        "temperature": 0.7,
        "max_tokens": 4096
    },
    "perplexity": {
        "api_base": "https://api.perplexity.ai/chat/completions",
        "timeout": 15,
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 0.9
    },
    "openrouter": {
        "api_base": "https://openrouter.ai/api/v1",
        "timeout": 30,
        "temperature": 0.7,
        "max_tokens": 4096
    }
}

# Advanced Feature Flags
FEATURE_FLAGS = {
    "enable_web_search": True,
    "enable_context_optimization": True,
    "enable_hybrid_routing": True,
    "enable_performance_tracking": True,
    "enable_advanced_categories": True,
    "enable_provider_switching": True,
    "enable_strategy_selection": True
}

# Cache Configuration
CACHE_CONFIG = {
    "web_search_cache": True,
    "context_optimization_cache": True,
    "model_response_cache": True,
    "cache_ttl": 3600,  # 1 hour
    "max_cache_size": 1000
}

# Integration Status Messages
INTEGRATION_STATUS = {
    "ollama_connected": "🟢 Ollama connected - Local models available",
    "ollama_disconnected": "🔴 Ollama disconnected - Install and start Ollama for local processing",
    "perplexity_connected": "🟢 Perplexity connected - Web search available", 
    "perplexity_disconnected": "🔴 Perplexity disconnected - Add API key for web search",
    "openrouter_connected": "🟢 OpenRouter connected - Cloud models available",
    "openrouter_disconnected": "🔴 OpenRouter disconnected - Add API key for cloud models",
    "hybrid_mode_enabled": "🟢 Hybrid mode enabled - Automatic provider selection active",
    "hybrid_mode_disabled": "🟡 Hybrid mode disabled - Using single provider"
}
