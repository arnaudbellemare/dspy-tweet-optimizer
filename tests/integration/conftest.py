"""Shared fixtures for integration tests."""

import pytest
import os
import json
import tempfile
from typing import Dict, Any


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_categories():
    """Sample evaluation categories."""
    return ["Clarity", "Engagement", "Professionalism"]


@pytest.fixture
def sample_settings():
    """Sample settings dictionary."""
    return {
        "model": "anthropic/claude-3.5-sonnet",
        "iterations": 5,
        "patience": 2,
        "use_cache": True
    }


@pytest.fixture
def sample_input_text():
    """Sample input text for tweet generation."""
    return "Just launched our new product! It's amazing and everyone should try it."


@pytest.fixture
def mock_lm_response():
    """Mock LLM response generator."""
    def _generate_response(response_type: str = "tweet", score: int = 7):
        """Generate mock LLM responses."""
        if response_type == "tweet":
            return "Excited to announce our new product launch! 🚀 Try it today and experience the difference."
        elif response_type == "evaluation":
            return {
                "evaluations": [
                    {
                        "category": "Clarity",
                        "reasoning": "Message is clear and direct",
                        "score": score
                    },
                    {
                        "category": "Engagement", 
                        "reasoning": "Good use of emoji and call to action",
                        "score": score + 1
                    },
                    {
                        "category": "Professionalism",
                        "reasoning": "Maintains professional tone",
                        "score": score
                    }
                ]
            }
        return None
    
    return _generate_response


@pytest.fixture
def create_test_files(temp_dir):
    """Create test JSON files in temporary directory."""
    def _create_files(categories=None, settings=None, history=None):
        files = {}
        
        if categories is not None:
            cat_file = os.path.join(temp_dir, "categories.json")
            with open(cat_file, 'w') as f:
                json.dump(categories, f)
            files['categories'] = cat_file
        
        if settings is not None:
            settings_file = os.path.join(temp_dir, "settings.json")
            with open(settings_file, 'w') as f:
                json.dump(settings, f)
            files['settings'] = settings_file
        
        if history is not None:
            history_file = os.path.join(temp_dir, "input_history.json")
            with open(history_file, 'w') as f:
                json.dump(history, f)
            files['history'] = history_file
        
        return files
    
    return _create_files
