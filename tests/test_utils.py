"""Tests for utility functions."""

import pytest
import json
import os
from unittest.mock import patch, mock_open, MagicMock
from utils import (
    save_categories,
    load_categories,
    save_settings,
    load_settings,
    add_to_input_history,
    format_tweet_for_display,
    calculate_tweet_length
)
from constants import (
    DEFAULT_CATEGORIES,
    DEFAULT_MODEL,
    DEFAULT_ITERATIONS,
    DEFAULT_PATIENCE,
    DEFAULT_USE_CACHE,
    MAX_HISTORY_ITEMS
)


class TestCategoryFunctions:
    """Tests for category save/load functions."""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('utils.st')
    def test_save_categories(self, mock_st, mock_file):
        """Test saving categories to file."""
        categories = ["Cat1", "Cat2", "Cat3"]
        save_categories(categories)
        
        # Verify file was opened for writing
        mock_file.assert_called_once_with('categories.json', 'w')
        
        # Verify JSON was written
        handle = mock_file()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        assert "Cat1" in written_data
        assert "Cat2" in written_data
    
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='["Cat1", "Cat2"]')
    @patch('utils.st')
    def test_load_categories_existing_file(self, mock_st, mock_file, mock_exists):
        """Test loading categories from existing file."""
        mock_exists.return_value = True
        
        categories = load_categories()
        
        assert categories == ["Cat1", "Cat2"]
        mock_file.assert_called_once_with('categories.json', 'r')
    
    @patch('os.path.exists')
    @patch('utils.save_categories')
    @patch('utils.st')
    def test_load_categories_no_file_creates_default(self, mock_st, mock_save, mock_exists):
        """Test that loading with no file creates default categories."""
        mock_exists.return_value = False
        
        categories = load_categories()
        
        assert categories == DEFAULT_CATEGORIES
        mock_save.assert_called_once_with(DEFAULT_CATEGORIES)


class TestSettingsFunctions:
    """Tests for settings save/load functions."""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('utils.st')
    def test_save_settings(self, mock_st, mock_file):
        """Test saving settings to file."""
        settings = {
            "selected_model": "test/model",
            "iterations": 15,
            "patience": 7,
            "use_cache": True
        }
        save_settings(settings)
        
        mock_file.assert_called_once_with('settings.json', 'w')
    
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"iterations": 20}')
    @patch('utils.st')
    def test_load_settings_existing_file(self, mock_st, mock_file, mock_exists):
        """Test loading settings from existing file."""
        mock_exists.return_value = True
        
        settings = load_settings()
        
        assert settings == {"iterations": 20}
    
    @patch('os.path.exists')
    @patch('utils.st')
    def test_load_settings_no_file_returns_defaults(self, mock_st, mock_exists):
        """Test that loading with no file returns defaults."""
        mock_exists.return_value = False
        
        settings = load_settings()
        
        assert settings["selected_model"] == DEFAULT_MODEL
        assert settings["iterations"] == DEFAULT_ITERATIONS
        assert settings["patience"] == DEFAULT_PATIENCE
        assert settings["use_cache"] == DEFAULT_USE_CACHE


class TestInputHistory:
    """Tests for input history functions."""
    
    def test_add_to_empty_history(self):
        """Test adding to empty history."""
        history = []
        new_input = "Test input"
        
        result = add_to_input_history(history, new_input)
        
        assert result == ["Test input"]
    
    def test_add_to_existing_history(self):
        """Test adding to existing history (most recent first)."""
        history = ["Old input 1", "Old input 2"]
        new_input = "New input"
        
        result = add_to_input_history(history, new_input)
        
        assert result[0] == "New input"
        assert result[1] == "Old input 1"
        assert result[2] == "Old input 2"
    
    def test_remove_duplicate(self):
        """Test that duplicates are removed."""
        history = ["Input 1", "Input 2", "Input 3"]
        new_input = "Input 2"
        
        result = add_to_input_history(history, new_input)
        
        # "Input 2" should be moved to the front, not duplicated
        assert result[0] == "Input 2"
        assert result.count("Input 2") == 1
        assert len(result) == 3
    
    def test_ignore_empty_input(self):
        """Test that empty inputs are ignored."""
        history = ["Input 1"]
        
        result = add_to_input_history(history, "")
        
        assert result == ["Input 1"]
    
    def test_trim_to_max_size(self):
        """Test that history is trimmed to MAX_HISTORY_ITEMS."""
        # Create history with MAX_HISTORY_ITEMS
        history = [f"Input {i}" for i in range(MAX_HISTORY_ITEMS)]
        new_input = "New input"
        
        result = add_to_input_history(history, new_input)
        
        assert len(result) == MAX_HISTORY_ITEMS
        assert result[0] == "New input"
        # Last item should be dropped
        assert f"Input {MAX_HISTORY_ITEMS - 1}" not in result


class TestTweetFunctions:
    """Tests for tweet formatting functions."""
    
    def test_format_tweet_for_display(self):
        """Test formatting tweet for display."""
        tweet = "  Test tweet  "
        result = format_tweet_for_display(tweet)
        assert result == "Test tweet"
    
    def test_calculate_tweet_length(self):
        """Test calculating tweet length."""
        tweet = "  Test tweet  "
        length = calculate_tweet_length(tweet)
        assert length == 10  # "Test tweet" without spaces
    
    def test_calculate_tweet_length_empty(self):
        """Test calculating length of empty tweet."""
        length = calculate_tweet_length("")
        assert length == 0
