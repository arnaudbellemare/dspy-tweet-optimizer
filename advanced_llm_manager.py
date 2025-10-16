"""
Advanced LLM Manager for integrating multiple AI frameworks.

This module provides a unified interface for:
- Local LLMs (via Ollama)
- Perplexity API integration
- GEPA-ACE context optimization
- Ax LLM framework
- Hybrid model selection and routing
"""

import os
import json
import requests
import dspy
from typing import Dict, List, Optional, Union, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Supported LLM providers."""
    OLLAMA = "ollama"
    PERPLEXITY = "perplexity"
    OPENROUTER = "openrouter"
    LOCAL_OLLAMA = "local_ollama"

@dataclass
class LLMConfig:
    """Configuration for LLM providers."""
    provider: LLMProvider
    model_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 30

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available."""
        pass

class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.base_url = config.base_url or "http://localhost:11434"
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Ollama."""
        try:
            payload = {
                "model": self.config.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "num_predict": kwargs.get("max_tokens", self.config.max_tokens)
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """List available Ollama models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except:
            return []

class PerplexityProvider(BaseLLMProvider):
    """Perplexity API provider with web search capabilities."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_key = config.api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("Perplexity API key is required")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Perplexity with web search."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.config.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides accurate, up-to-date information using web search when needed."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                "temperature": kwargs.get("temperature", self.config.temperature),
                "top_p": 0.9,
                "stream": False
            }
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Perplexity generation failed: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Perplexity API is available."""
        return bool(self.api_key)

class GEPAACEOptimizer:
    """GEPA-ACE (Generalized Pre-trained Encoder Architecture - Adaptive Contextual Embedding) optimizer."""
    
    def __init__(self):
        self.context_cache = {}
        self.optimization_history = []
    
    def optimize_context(self, prompt: str, context: str, target_length: int = 1000) -> str:
        """
        Optimize context using GEPA-ACE principles.
        
        Args:
            prompt: The main prompt
            context: Additional context to optimize
            target_length: Target length for optimized context
            
        Returns:
            Optimized context string
        """
        # Simple implementation - in practice, this would use more sophisticated
        # context optimization algorithms
        if len(context) <= target_length:
            return context
        
        # Cache optimization results
        cache_key = f"{hash(prompt)}_{hash(context)}_{target_length}"
        if cache_key in self.context_cache:
            return self.context_cache[cache_key]
        
        # Basic optimization: extract key sentences and maintain coherence
        sentences = context.split('. ')
        optimized_sentences = []
        current_length = 0
        
        for sentence in sentences:
            if current_length + len(sentence) <= target_length:
                optimized_sentences.append(sentence)
                current_length += len(sentence)
            else:
                break
        
        optimized_context = '. '.join(optimized_sentences)
        self.context_cache[cache_key] = optimized_context
        
        # Track optimization history
        self.optimization_history.append({
            "original_length": len(context),
            "optimized_length": len(optimized_context),
            "compression_ratio": len(optimized_context) / len(context)
        })
        
        return optimized_context
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization statistics."""
        if not self.optimization_history:
            return {"total_optimizations": 0}
        
        avg_compression = sum(h["compression_ratio"] for h in self.optimization_history) / len(self.optimization_history)
        return {
            "total_optimizations": len(self.optimization_history),
            "average_compression_ratio": avg_compression,
            "total_original_length": sum(h["original_length"] for h in self.optimization_history),
            "total_optimized_length": sum(h["optimized_length"] for h in self.optimization_history)
        }

class AxLLMManager:
    """Ax LLM framework manager for advanced model orchestration."""
    
    def __init__(self):
        self.model_registry = {}
        self.routing_rules = {}
        self.performance_metrics = {}
    
    def register_model(self, name: str, provider: BaseLLMProvider, capabilities: List[str]):
        """Register a model with its capabilities."""
        self.model_registry[name] = {
            "provider": provider,
            "capabilities": capabilities,
            "usage_count": 0,
            "avg_response_time": 0.0
        }
    
    def route_request(self, prompt: str, required_capabilities: List[str] = None) -> str:
        """
        Route request to best available model based on capabilities and performance.
        
        Args:
            prompt: The prompt to process
            required_capabilities: Required model capabilities
            
        Returns:
            Name of selected model
        """
        available_models = []
        
        for name, model_info in self.model_registry.items():
            if not model_info["provider"].is_available():
                continue
            
            if required_capabilities:
                if not all(cap in model_info["capabilities"] for cap in required_capabilities):
                    continue
            
            available_models.append((name, model_info))
        
        if not available_models:
            raise RuntimeError("No available models with required capabilities")
        
        # Simple routing: select model with best performance score
        best_model = min(available_models, key=lambda x: x[1]["avg_response_time"])
        return best_model[0]
    
    def update_performance(self, model_name: str, response_time: float, success: bool):
        """Update model performance metrics."""
        if model_name in self.model_registry:
            model_info = self.model_registry[model_name]
            model_info["usage_count"] += 1
            
            # Update average response time
            current_avg = model_info["avg_response_time"]
            count = model_info["usage_count"]
            model_info["avg_response_time"] = (current_avg * (count - 1) + response_time) / count
            
            # Track success rate
            if model_name not in self.performance_metrics:
                self.performance_metrics[model_name] = {"successes": 0, "failures": 0}
            
            if success:
                self.performance_metrics[model_name]["successes"] += 1
            else:
                self.performance_metrics[model_name]["failures"] += 1

class AdvancedLLMManager:
    """Main manager for advanced LLM integration."""
    
    def __init__(self):
        self.providers = {}
        self.gepa_ace = GEPAACEOptimizer()
        self.ax_manager = AxLLMManager()
        self.default_provider = None
        self.hybrid_mode = False
    
    def add_provider(self, name: str, provider: BaseLLMProvider, capabilities: List[str] = None):
        """Add a new LLM provider."""
        self.providers[name] = provider
        if capabilities:
            self.ax_manager.register_model(name, provider, capabilities)
        
        if not self.default_provider:
            self.default_provider = name
    
    def set_hybrid_mode(self, enabled: bool):
        """Enable/disable hybrid mode for automatic provider selection."""
        self.hybrid_mode = enabled
    
    def generate(self, prompt: str, provider: str = None, use_context_optimization: bool = True, **kwargs) -> str:
        """
        Generate text using specified or best available provider.
        
        Args:
            prompt: The prompt to generate from
            provider: Specific provider to use (optional)
            use_context_optimization: Whether to use GEPA-ACE optimization
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text
        """
        import time
        start_time = time.time()
        
        try:
            # Select provider
            if provider and provider in self.providers:
                selected_provider = self.providers[provider]
            elif self.hybrid_mode:
                # Use Ax LLM routing
                model_name = self.ax_manager.route_request(prompt)
                selected_provider = self.providers[model_name]
            else:
                selected_provider = self.providers.get(self.default_provider)
            
            if not selected_provider:
                raise RuntimeError("No available LLM provider")
            
            # Apply context optimization if enabled
            if use_context_optimization and hasattr(kwargs, 'context'):
                kwargs['context'] = self.gepa_ace.optimize_context(
                    prompt, kwargs['context']
                )
            
            # Generate response
            response = selected_provider.generate(prompt, **kwargs)
            
            # Update performance metrics
            response_time = time.time() - start_time
            provider_name = provider or self.default_provider
            self.ax_manager.update_performance(provider_name, response_time, True)
            
            return response
            
        except Exception as e:
            # Update failure metrics
            response_time = time.time() - start_time
            provider_name = provider or self.default_provider
            self.ax_manager.update_performance(provider_name, response_time, False)
            logger.error(f"Generation failed: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all providers and optimizers."""
        status = {
            "providers": {},
            "gepa_ace_stats": self.gepa_ace.get_optimization_stats(),
            "ax_manager_stats": {
                "registered_models": len(self.ax_manager.model_registry),
                "performance_metrics": self.ax_manager.performance_metrics
            },
            "hybrid_mode": self.hybrid_mode
        }
        
        for name, provider in self.providers.items():
            status["providers"][name] = {
                "available": provider.is_available(),
                "type": type(provider).__name__
            }
        
        return status

# Global instance
advanced_llm_manager = AdvancedLLMManager()

def setup_advanced_llm_system():
    """Set up the complete advanced LLM system."""
    
    # Add Ollama provider if available
    ollama_config = LLMConfig(
        provider=LLMProvider.OLLAMA,
        model_name="gemma3:4b",  # Default model - Gemma 3:4b
        base_url="http://localhost:11434"
    )
    
    try:
        ollama_provider = OllamaProvider(ollama_config)
        if ollama_provider.is_available():
            advanced_llm_manager.add_provider(
                "ollama_gemma3_4b",
                ollama_provider,
                capabilities=["text_generation", "local_processing"]
            )
            logger.info("Ollama provider added successfully")
    except Exception as e:
        logger.warning(f"Could not add Ollama provider: {e}")
    
    # Add Perplexity provider if API key is available
    if os.getenv("PERPLEXITY_API_KEY"):
        try:
            perplexity_config = LLMConfig(
                provider=LLMProvider.PERPLEXITY,
                model_name="llama-3.1-sonar-small-128k-online",
                api_key=os.getenv("PERPLEXITY_API_KEY")
            )
            
            perplexity_provider = PerplexityProvider(perplexity_config)
            advanced_llm_manager.add_provider(
                "perplexity_sonar",
                perplexity_provider,
                capabilities=["web_search", "real_time_info", "text_generation"]
            )
            logger.info("Perplexity provider added successfully")
        except Exception as e:
            logger.warning(f"Could not add Perplexity provider: {e}")
    
    # Enable hybrid mode
    advanced_llm_manager.set_hybrid_mode(True)
    
    return advanced_llm_manager

def create_dspy_lm_from_advanced_manager(provider_name: str = None):
    """Create a DSPy LM instance using the advanced LLM manager."""
    
    class AdvancedDSPyLM(dspy.LM):
        """Custom DSPy LM that uses the advanced LLM manager."""
        
        def __init__(self, provider_name: str = None):
            self.provider_name = provider_name
            self.manager = advanced_llm_manager
        
        def generate(self, prompt: str, **kwargs) -> str:
            """Generate using advanced LLM manager."""
            return self.manager.generate(
                prompt=prompt,
                provider=self.provider_name,
                **kwargs
            )
        
        def __call__(self, prompt: str, **kwargs) -> str:
            """Make the LM callable."""
            return self.generate(prompt, **kwargs)
    
    return AdvancedDSPyLM(provider_name)
