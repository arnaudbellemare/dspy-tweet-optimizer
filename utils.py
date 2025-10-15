import json
import os
import streamlit as st
import dspy
from typing import List, Dict, Any

CATEGORIES_FILE = "categories.json"
SETTINGS_FILE = "settings.json"

def save_categories(categories: List[str]) -> None:
    """Save categories to JSON file."""
    try:
        with open(CATEGORIES_FILE, 'w') as f:
            json.dump(categories, f, indent=2)
    except Exception as e:
        st.error(f"Failed to save categories: {str(e)}")

def load_categories() -> List[str]:
    """Load categories from JSON file."""
    try:
        if os.path.exists(CATEGORIES_FILE):
            with open(CATEGORIES_FILE, 'r') as f:
                categories = json.load(f)
                return categories if isinstance(categories, list) else []
        else:
            # Default categories if file doesn't exist
            default_categories = [
                "Engagement potential - how likely users are to like, retweet, or reply",
                "Clarity and readability - how easy the tweet is to understand",
                "Emotional impact - how well the tweet evokes feelings or reactions",
                "Relevance to target audience - how well it resonates with intended readers"
            ]
            save_categories(default_categories)
            return default_categories
    except Exception as e:
        st.error(f"Failed to load categories: {str(e)}")
        return []

@st.cache_resource
def get_dspy_lm(model_name: str):
    """Get a DSPy LM instance for the specified model (cached per model)."""
    try:
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        lm = dspy.LM(
            model=model_name,
            api_key=openrouter_key,
            api_base="https://openrouter.ai/api/v1",
            max_tokens=4096,
            temperature=0.7
        )
        return lm
    except Exception as e:
        raise Exception(f"Failed to create LM: {str(e)}")

def initialize_dspy(model_name: str = "openrouter/anthropic/claude-sonnet-4.5"):
    """Initialize DSPy with OpenRouter and selected model."""
    # Only configure DSPy once globally
    if not hasattr(dspy, '_replit_configured'):
        try:
            # Get the LM for the default model
            default_lm = get_dspy_lm(model_name)
            dspy.configure(lm=default_lm)
            dspy._replit_configured = True
        except Exception as e:
            raise Exception(f"DSPy initialization failed: {str(e)}")
    
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
    return bool(cleaned_tweet) and len(cleaned_tweet) <= 280

def save_settings(settings: Dict[str, Any]) -> None:
    """Save settings to JSON file."""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        st.error(f"Failed to save settings: {str(e)}")

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
        st.error(f"Failed to load settings: {str(e)}")
        return get_default_settings()

def get_default_settings() -> Dict[str, Any]:
    """Get default settings."""
    return {
        "selected_model": "openrouter/anthropic/claude-sonnet-4.5",
        "iterations": 10,
        "patience": 5
    }
