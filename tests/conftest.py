"""Pytest configuration and shared fixtures."""

import pytest
from typing import List, Dict, Any
from models import CategoryEvaluation, EvaluationResult


@pytest.fixture
def sample_categories() -> List[str]:
    """Sample evaluation categories for testing."""
    return [
        "Engagement potential",
        "Clarity and readability",
        "Emotional impact"
    ]


@pytest.fixture
def sample_category_evaluation() -> CategoryEvaluation:
    """Sample category evaluation for testing."""
    return CategoryEvaluation(
        category="Engagement potential",
        reasoning="This tweet is highly engaging with a clear call to action",
        score=8
    )


@pytest.fixture
def sample_evaluation_result(sample_category_evaluation) -> EvaluationResult:
    """Sample evaluation result for testing."""
    return EvaluationResult(
        evaluations=[
            sample_category_evaluation,
            CategoryEvaluation(
                category="Clarity",
                reasoning="Very clear and easy to understand",
                score=9
            ),
            CategoryEvaluation(
                category="Impact",
                reasoning="Strong emotional resonance",
                score=7
            )
        ]
    )


@pytest.fixture
def sample_settings() -> Dict[str, Any]:
    """Sample settings dictionary for testing."""
    return {
        "selected_model": "openrouter/anthropic/claude-sonnet-4.5",
        "iterations": 10,
        "patience": 5,
        "use_cache": True
    }


@pytest.fixture
def sample_tweet() -> str:
    """Sample tweet text for testing."""
    return "Building amazing AI applications with DSPy is so rewarding! The structured approach makes LLM development much more reliable and maintainable. #AI #DSPy"


@pytest.fixture
def long_tweet() -> str:
    """Sample long tweet that exceeds character limit."""
    return "a" * 300  # 300 characters, exceeds 280 limit
