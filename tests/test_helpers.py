"""Tests for helper functions."""

import pytest
from helpers import (
    format_evaluation_for_generator,
    build_settings_dict,
    truncate_tweet,
    truncate_category_display
)
from models import CategoryEvaluation, EvaluationResult
from constants import MAX_SCORE


class TestFormatEvaluationForGenerator:
    """Tests for format_evaluation_for_generator function."""
    
    def test_format_with_valid_evaluation(self):
        """Test formatting a valid evaluation result."""
        result = EvaluationResult(
            evaluations=[
                CategoryEvaluation(
                    category="Engagement",
                    reasoning="Very engaging content",
                    score=8
                ),
                CategoryEvaluation(
                    category="Clarity",
                    reasoning="Clear and concise",
                    score=9
                )
            ]
        )
        formatted = format_evaluation_for_generator(result)
        
        assert "Engagement (Score: 8/9): Very engaging content" in formatted
        assert "Clarity (Score: 9/9): Clear and concise" in formatted
        assert "\n" in formatted  # Should be multiline
    
    def test_format_with_none(self):
        """Test formatting with None evaluation."""
        formatted = format_evaluation_for_generator(None)
        assert formatted == ""
    
    def test_format_with_empty_evaluations(self):
        """Test formatting with empty evaluations."""
        result = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="Test", reasoning="Test", score=5)
            ]
        )
        result.evaluations = []  # Force empty (bypasses validation)
        formatted = format_evaluation_for_generator(result)
        assert formatted == ""


class TestBuildSettingsDict:
    """Tests for build_settings_dict function."""
    
    def test_build_settings_dict(self):
        """Test building settings dictionary."""
        settings = build_settings_dict(
            selected_model="openrouter/anthropic/claude-sonnet-4.5",
            iterations=15,
            patience=7,
            use_cache=True
        )
        
        assert settings["selected_model"] == "openrouter/anthropic/claude-sonnet-4.5"
        assert settings["iterations"] == 15
        assert settings["patience"] == 7
        assert settings["use_cache"] is True
    
    def test_build_settings_dict_with_cache_disabled(self):
        """Test building settings with cache disabled."""
        settings = build_settings_dict(
            selected_model="test/model",
            iterations=10,
            patience=5,
            use_cache=False
        )
        
        assert settings["use_cache"] is False


class TestTruncateTweet:
    """Tests for truncate_tweet function."""
    
    def test_truncate_short_tweet(self):
        """Test that short tweets are not truncated."""
        tweet = "This is a short tweet"
        result = truncate_tweet(tweet, 280)
        assert result == tweet
    
    def test_truncate_long_tweet(self):
        """Test that long tweets are truncated."""
        tweet = "a" * 300
        result = truncate_tweet(tweet, 280)
        assert len(result) == 280
        assert result.endswith("...")
    
    def test_truncate_exact_length(self):
        """Test tweet at exact max length."""
        tweet = "a" * 280
        result = truncate_tweet(tweet, 280)
        assert result == tweet
        assert len(result) == 280
    
    def test_truncate_with_custom_suffix(self):
        """Test truncation with custom suffix."""
        tweet = "a" * 100
        result = truncate_tweet(tweet, 50, suffix="[...]")
        assert len(result) == 50
        assert result.endswith("[...]")
    
    def test_truncate_strips_whitespace(self):
        """Test that whitespace is stripped."""
        tweet = "   test tweet   "
        result = truncate_tweet(tweet, 280)
        assert result == "test tweet"


class TestTruncateCategoryDisplay:
    """Tests for truncate_category_display function."""
    
    def test_short_category(self):
        """Test that short categories are not truncated."""
        category = "Short"
        result = truncate_category_display(category, 30)
        assert result == category
    
    def test_long_category_default_length(self):
        """Test truncation with default max length (30)."""
        category = "This is a very long category name that should be truncated"
        result = truncate_category_display(category)
        assert len(result) <= 33  # 30 + "..."
        assert result.endswith("...")
    
    def test_long_category_custom_length(self):
        """Test truncation with custom max length."""
        category = "This is a long category"
        result = truncate_category_display(category, 10)
        assert len(result) == 13  # 10 + "..."
        assert result.endswith("...")
    
    def test_exact_length_category(self):
        """Test category at exact max length."""
        category = "a" * 30
        result = truncate_category_display(category, 30)
        assert result == category
