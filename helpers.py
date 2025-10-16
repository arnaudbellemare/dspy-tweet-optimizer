"""
Helper functions for the DSPy Tweet Optimizer.

This module contains reusable utility functions to eliminate code duplication
and improve maintainability.
"""

from typing import Optional, Dict, Any
from models import EvaluationResult
from constants import MAX_SCORE


def format_evaluation_for_generator(evaluation: Optional[EvaluationResult]) -> str:
    """
    Format an evaluation result as text for the generator module.
    
    Args:
        evaluation: The evaluation result to format
        
    Returns:
        Formatted string with category-by-category reasoning and scores
    """
    if not evaluation or not evaluation.evaluations:
        return ""
    
    eval_lines = []
    for eval in evaluation.evaluations:
        eval_lines.append(f"{eval.category} (Score: {eval.score}/{MAX_SCORE}): {eval.reasoning}")
    
    return "\n".join(eval_lines)


def build_settings_dict(
    selected_model: str,
    iterations: int,
    patience: int,
    use_cache: bool
) -> Dict[str, Any]:
    """
    Build a settings dictionary for saving.
    
    Args:
        selected_model: The selected model name
        iterations: Number of optimization iterations
        patience: Patience threshold for early stopping
        use_cache: Whether to use DSPy cache
        
    Returns:
        Dictionary containing all settings
    """
    return {
        "selected_model": selected_model,
        "iterations": iterations,
        "patience": patience,
        "use_cache": use_cache
    }


def truncate_tweet(tweet: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a tweet to the maximum length with a suffix.
    
    Args:
        tweet: The tweet text to truncate
        max_length: Maximum allowed length
        suffix: Suffix to add when truncating (default: "...")
        
    Returns:
        Truncated tweet text
    """
    tweet = tweet.strip()
    if len(tweet) <= max_length:
        return tweet
    
    truncation_point = max_length - len(suffix)
    return tweet[:truncation_point] + suffix


def truncate_category_display(category: str, max_length: int = 30) -> str:
    """
    Truncate a category name for display purposes.
    
    Args:
        category: The category name
        max_length: Maximum display length (default: 30)
        
    Returns:
        Truncated category name with "..." if needed
    """
    if len(category) <= max_length:
        return category
    return category[:max_length] + "..."
