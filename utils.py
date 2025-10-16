import json
import os
import streamlit as st
import dspy
from typing import List, Dict, Any
from constants import (
    CATEGORIES_FILE,
    SETTINGS_FILE,
    HISTORY_FILE,
    DEFAULT_CATEGORIES,
    DEFAULT_MODEL,
    DEFAULT_ITERATIONS,
    DEFAULT_PATIENCE,
    DEFAULT_USE_CACHE,
    MAX_HISTORY_ITEMS,
    OPENROUTER_API_BASE,
    OPENROUTER_MAX_TOKENS,
    OPENROUTER_TEMPERATURE,
    ERROR_NO_API_KEY,
    ERROR_SAVE_CATEGORIES,
    ERROR_LOAD_CATEGORIES,
    ERROR_SAVE_SETTINGS,
    ERROR_LOAD_SETTINGS,
    ERROR_SAVE_HISTORY,
    ERROR_LOAD_HISTORY,
    ERROR_DSPy_INIT,
    TWEET_MAX_LENGTH
)

def save_categories(categories: List[str]) -> None:
    """Save categories to JSON file."""
    try:
        with open(CATEGORIES_FILE, 'w') as f:
            json.dump(categories, f, indent=2)
    except Exception as e:
        st.error(f"{ERROR_SAVE_CATEGORIES}: {str(e)}")

def load_categories() -> List[str]:
    """Load categories from JSON file."""
    try:
        if os.path.exists(CATEGORIES_FILE):
            with open(CATEGORIES_FILE, 'r') as f:
                categories = json.load(f)
                return categories if isinstance(categories, list) else []
        else:
            save_categories(DEFAULT_CATEGORIES)
            return DEFAULT_CATEGORIES
    except Exception as e:
        st.error(f"{ERROR_LOAD_CATEGORIES}: {str(e)}")
        return []

@st.cache_resource
def get_dspy_lm(model_name: str):
    """Get a DSPy LM instance for the specified model (cached per model)."""
    try:
        # Check if it's an Ollama model
        if model_name.startswith("ollama/"):
            # Extract the actual model name (remove "ollama/" prefix)
            actual_model = model_name.replace("ollama/", "")
            
            lm = dspy.LM(
                model=actual_model,
                api_base="http://localhost:11434",
                max_tokens=4096,
                temperature=0.7
            )
            return lm
        else:
            # Handle OpenRouter models
            openrouter_key = os.getenv("OPENROUTER_API_KEY")
            if not openrouter_key:
                raise ValueError(ERROR_NO_API_KEY)
            
            lm = dspy.LM(
                model=model_name,
                api_key=openrouter_key,
                api_base=OPENROUTER_API_BASE,
                max_tokens=OPENROUTER_MAX_TOKENS,
                temperature=OPENROUTER_TEMPERATURE
            )
            return lm
    except Exception as e:
        raise Exception(f"Failed to create LM: {str(e)}")

def initialize_dspy(model_name: str = DEFAULT_MODEL, use_cache: bool = DEFAULT_USE_CACHE) -> bool:
    """Initialize DSPy with OpenRouter and selected model."""
    # Configure cache settings
    try:
        dspy.configure_cache(
            enable_memory_cache=use_cache,
            enable_disk_cache=use_cache
        )
    except Exception:
        # Cache configuration might fail in some environments, continue anyway
        pass
    
    # Only configure DSPy once globally
    if not hasattr(dspy, '_replit_configured'):
        try:
            # Get the LM for the default model
            default_lm = get_dspy_lm(model_name)
            dspy.configure(lm=default_lm)
            dspy._replit_configured = True  # type: ignore
        except Exception as e:
            raise Exception(f"{ERROR_DSPy_INIT}: {str(e)}")
    
    return True

def format_tweet_for_display(tweet: str) -> str:
    """Format tweet text for better display."""
    return tweet.strip()

def calculate_tweet_length(tweet: str) -> int:
    """Calculate tweet length."""
    return len(tweet.strip())

def is_valid_tweet(tweet: str) -> bool:
    """Check if tweet is valid (not empty and within character limit)."""
    cleaned_tweet = tweet.strip()
    return bool(cleaned_tweet) and len(cleaned_tweet) <= TWEET_MAX_LENGTH

def save_settings(settings: Dict[str, Any]) -> None:
    """Save settings to JSON file."""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        st.error(f"{ERROR_SAVE_SETTINGS}: {str(e)}")

def load_settings() -> Dict[str, Any]:
    """Load settings from JSON file."""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                return settings if isinstance(settings, dict) else get_default_settings()
        else:
            # Return default settings if file doesn't exist
            default_settings = get_default_settings()
            save_settings(default_settings)
            return default_settings
    except Exception as e:
        st.error(f"{ERROR_LOAD_SETTINGS}: {str(e)}")
        return get_default_settings()

def get_default_settings() -> Dict[str, Any]:
    """Get default settings."""
    return {
        "selected_model": DEFAULT_MODEL,
        "iterations": DEFAULT_ITERATIONS,
        "patience": DEFAULT_PATIENCE,
        "use_cache": DEFAULT_USE_CACHE
    }

def save_input_history(history: List[str]) -> None:
    """Save input history to JSON file."""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        st.error(f"{ERROR_SAVE_HISTORY}: {str(e)}")

def load_input_history() -> List[str]:
    """Load input history from JSON file."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                return history if isinstance(history, list) else []
        else:
            return []
    except Exception as e:
        st.error(f"{ERROR_LOAD_HISTORY}: {str(e)}")
        return []

def add_to_input_history(history: List[str], new_input: str) -> List[str]:
    """
    Add a new input to history, maintaining max size and avoiding duplicates.
    
    Args:
        history: Current history list
        new_input: New input text to add
        
    Returns:
        Updated history list with new input at the beginning
    """
    # Strip whitespace from input
    new_input = new_input.strip()
    
    # Don't add empty strings
    if not new_input:
        return history
    
    # Remove duplicate if it exists
    if new_input in history:
        history.remove(new_input)
    
    # Add to beginning of list
    updated_history = [new_input] + history
    
    # Trim to max size
    if len(updated_history) > MAX_HISTORY_ITEMS:
        updated_history = updated_history[:MAX_HISTORY_ITEMS]
    
    return updated_history
