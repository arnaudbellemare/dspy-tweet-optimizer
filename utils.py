import json
import os
import streamlit as st
import dspy
from typing import List

CATEGORIES_FILE = "categories.json"

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

def initialize_dspy():
    """Initialize DSPy with OpenRouter and Claude Sonnet 4.5."""
    try:
        # Get OpenRouter API key from environment
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        # Configure DSPy with OpenRouter
        lm = dspy.OpenAI(
            model="anthropic/claude-3.5-sonnet",
            api_key=openrouter_key,
            api_base="https://openrouter.ai/api/v1",
            model_type="chat"
        )
        
        dspy.settings.configure(lm=lm)
        
    except Exception as e:
        raise Exception(f"DSPy initialization failed: {str(e)}")

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
