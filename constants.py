"""
Central configuration and constants for the DSPy Tweet Optimizer.

This module contains all configuration values, magic numbers, and constants
used throughout the application to improve maintainability.
"""

from typing import Dict, List

# Tweet Configuration
TWEET_MAX_LENGTH = 280
TWEET_TRUNCATION_SUFFIX = "..."
TWEET_TRUNCATION_LENGTH = TWEET_MAX_LENGTH - len(TWEET_TRUNCATION_SUFFIX)

# Score Configuration
MIN_SCORE = 1
MAX_SCORE = 9
DEFAULT_SCORE = 5

# File Paths
CATEGORIES_FILE = "categories.json"
SETTINGS_FILE = "settings.json"
HISTORY_FILE = "input_history.json"

# History Configuration
MAX_HISTORY_ITEMS = 50  # Maximum number of historical inputs to store

# Model Configuration
DEFAULT_MODEL = "openrouter/anthropic/claude-sonnet-4.5"

AVAILABLE_MODELS: Dict[str, str] = {
    "Claude Sonnet 4.5": "openrouter/anthropic/claude-sonnet-4.5",
    "Opus 4.1": "openrouter/anthropic/claude-opus-4.1",
    "Gemini 2.5 Flash": "openrouter/google/gemini-2.5-flash",
    "Gemini 2.5 Flash Lite": "openrouter/google/gemini-2.5-flash-lite",
    "Gemini 2.5 Pro": "openrouter/google/gemini-2.5-pro",
    "GPT-5": "openrouter/openai/gpt-5",
    "Gemma 2 4B": "openrouter/google/gemma-2-4b",  # Cloud-friendly Gemma
    "Gemma 3 4B (Local)": "ollama/gemma3:4b"  # Only works locally
}

# API Configuration
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
OPENROUTER_MAX_TOKENS = 4096
OPENROUTER_TEMPERATURE = 0.7

# Optimization Defaults
DEFAULT_ITERATIONS = 10
DEFAULT_PATIENCE = 5
DEFAULT_USE_CACHE = True

# Default Evaluation Categories
DEFAULT_CATEGORIES: List[str] = [
    "Engagement potential - how likely users are to like, retweet, or reply",
    "Clarity and readability - how easy the tweet is to understand",
    "Emotional impact - how well the tweet evokes feelings or reactions",
    "Relevance to target audience - how well it resonates with intended readers"
]

# UI Theme Colors
COLOR_PRIMARY = "#ff0000"  # Red accent color
COLOR_BACKGROUND_DARK = "#1a1a1a"  # Dark background
COLOR_SUCCESS = "#00ff00"  # Green for improvements
COLOR_FAILURE = "#ff0000"  # Red for declines
COLOR_NEUTRAL = "#ffffff"  # White for no change

# UI Configuration
PAGE_TITLE = "DSPy Tweet Optimizer"
PAGE_LAYOUT = "wide"

# History UI Configuration
HISTORY_RECENT_INDICATOR = "🕐 "  # Icon for recent history items
HISTORY_RECENT_COUNT = 3  # Number of items to mark as recent
HISTORY_TRUNCATE_LENGTH = 75  # Characters to show in history dropdown

# Error Messages
ERROR_PARSING = "Default evaluation due to parsing error"
ERROR_VALIDATION = "Default evaluation due to validation error"
ERROR_GENERATION = "Tweet generation failed"
ERROR_EVALUATION = "Tweet evaluation failed"
ERROR_DSPy_INIT = "DSPy initialization failed"
ERROR_NO_API_KEY = "OPENROUTER_API_KEY environment variable is required"
ERROR_SAVE_CATEGORIES = "Failed to save categories"
ERROR_LOAD_CATEGORIES = "Failed to load categories"
ERROR_SAVE_SETTINGS = "Failed to save settings"
ERROR_LOAD_SETTINGS = "Failed to load settings"
ERROR_SAVE_HISTORY = "Failed to save input history"
ERROR_LOAD_HISTORY = "Failed to load input history"

# Cache Configuration
CACHE_ENABLE_MEMORY = True
CACHE_ENABLE_DISK = True

# UI Element Sizes
SIDEBAR_COL_CATEGORY = 4
SIDEBAR_COL_DELETE = 1
MAIN_COL_INPUT = 2
MAIN_COL_STATS = 1
CHART_HEIGHT = 400
INPUT_HEIGHT = 100

# Iteration Display
ITERATION_SLEEP_TIME = 0.1  # seconds

# Truncation Display
CATEGORY_DISPLAY_MAX_LENGTH = 30
CATEGORY_DISPLAY_TRUNCATION = "..."
CATEGORY_IMPROVEMENT_MAX_LENGTH = 50
