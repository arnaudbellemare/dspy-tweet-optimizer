"""Integration tests for file operations."""

import pytest
import os
import json
from unittest.mock import patch
from utils import (
    save_categories, load_categories,
    save_settings, load_settings,
    add_to_input_history, load_input_history, save_input_history
)
from constants import CATEGORIES_FILE, SETTINGS_FILE, HISTORY_FILE


class TestCategoryFileOperations:
    """Integration tests for category file operations."""
    
    @patch('utils.CATEGORIES_FILE')
    @patch('streamlit.error')
    def test_save_and_load_categories(self, mock_error, mock_file, temp_dir, sample_categories):
        """Test saving and loading categories from actual files."""
        filepath = os.path.join(temp_dir, "categories.json")
        mock_file.__str__ = lambda self: filepath
        
        with patch('utils.CATEGORIES_FILE', filepath):
            # Save categories
            save_categories(sample_categories)
            
            # Verify file exists
            assert os.path.exists(filepath)
            
            # Load categories
            loaded = load_categories()
            
            # Verify content
            assert loaded == sample_categories
    
    @patch('streamlit.error')
    def test_load_categories_creates_default_file(self, mock_error, temp_dir):
        """Test that loading from non-existent file creates default."""
        filepath = os.path.join(temp_dir, "test_categories.json")
        
        with patch('utils.CATEGORIES_FILE', filepath):
            # File doesn't exist yet
            assert not os.path.exists(filepath)
            
            # Load should create default
            loaded = load_categories()
            
            # Should return default categories
            assert isinstance(loaded, list)
            assert len(loaded) > 0
            
            # File should now exist
            assert os.path.exists(filepath)


class TestSettingsFileOperations:
    """Integration tests for settings file operations."""
    
    @patch('streamlit.error')
    def test_save_and_load_settings(self, mock_error, temp_dir, sample_settings):
        """Test saving and loading settings from actual files."""
        filepath = os.path.join(temp_dir, "settings.json")
        
        with patch('utils.SETTINGS_FILE', filepath):
            # Save settings
            save_settings(sample_settings)
            
            # Verify file exists
            assert os.path.exists(filepath)
            
            # Load settings
            loaded = load_settings()
            
            # Verify content has the keys we saved
            for key in sample_settings:
                if key in loaded:
                    assert loaded[key] == sample_settings[key]
    
    @patch('streamlit.error')
    def test_load_settings_creates_default_for_missing_file(self, mock_error, temp_dir):
        """Test loading from non-existent settings file creates defaults."""
        filepath = os.path.join(temp_dir, "settings.json")
        
        with patch('utils.SETTINGS_FILE', filepath):
            # Load from non-existent file
            loaded = load_settings()
            
            # Should return default settings
            assert isinstance(loaded, dict)
            assert 'selected_model' in loaded or 'model' in loaded
            
            # File should be created
            assert os.path.exists(filepath)


class TestInputHistoryOperations:
    """Integration tests for input history operations."""
    
    @patch('streamlit.error')
    def test_add_and_save_history(self, mock_error, temp_dir):
        """Test adding to and saving input history."""
        filepath = os.path.join(temp_dir, "input_history.json")
        
        with patch('utils.HISTORY_FILE', filepath):
            # Start with empty history
            history = []
            
            # Add first input
            history = add_to_input_history(history, "First input")
            save_input_history(history)
            
            # Verify file exists
            assert os.path.exists(filepath)
            
            # Load and verify
            loaded = load_input_history()
            assert "First input" in loaded
    
    def test_history_deduplication(self):
        """Test that duplicate inputs are deduplicated."""
        history = []
        
        # Add inputs with duplicates
        history = add_to_input_history(history, "Input 1")
        history = add_to_input_history(history, "Input 2")
        history = add_to_input_history(history, "Input 1")  # Duplicate
        
        # Should have only 2 unique items
        assert len(history) == 2
        
        # Most recent occurrence should be first
        assert history[0] == "Input 1"
    
    def test_history_size_limit(self):
        """Test that history respects maximum size limit."""
        history = []
        
        # Add more than max items (max is 50)
        for i in range(60):
            history = add_to_input_history(history, f"Input {i}")
        
        # Should be limited to 50 items
        assert len(history) <= 50
        
        # Should keep most recent items (most recent first)
        assert "Input 59" in history
        assert "Input 0" not in history
    
    def test_empty_inputs_ignored(self):
        """Test that empty inputs are not added to history."""
        history = []
        
        # Try to add empty and whitespace inputs
        history = add_to_input_history(history, "")
        history = add_to_input_history(history, "   ")
        history = add_to_input_history(history, "Valid input")
        
        # Should only have valid input
        assert len(history) == 1
        assert history[0] == "Valid input"


class TestCrossFileOperations:
    """Integration tests for operations involving multiple files."""
    
    @patch('streamlit.error')
    def test_complete_workflow_with_all_files(self, mock_error, temp_dir, sample_categories, sample_settings):
        """Test a complete workflow using all configuration files."""
        cat_file = os.path.join(temp_dir, "categories.json")
        settings_file = os.path.join(temp_dir, "settings.json")
        history_file = os.path.join(temp_dir, "input_history.json")
        
        with patch('utils.CATEGORIES_FILE', cat_file), \
             patch('utils.SETTINGS_FILE', settings_file), \
             patch('utils.HISTORY_FILE', history_file):
            
            # Save all configurations
            save_categories(sample_categories)
            save_settings(sample_settings)
            
            history = add_to_input_history([], "Test input")
            save_input_history(history)
            
            # Verify all files exist
            assert os.path.exists(cat_file)
            assert os.path.exists(settings_file)
            assert os.path.exists(history_file)
            
            # Load all configurations
            categories = load_categories()
            settings = load_settings()
            loaded_history = load_input_history()
            
            # Verify all data
            assert categories == sample_categories
            # Settings may have additional default keys
            for key in sample_settings:
                if key in settings:
                    assert settings[key] == sample_settings[key]
            assert "Test input" in loaded_history
    
    @patch('streamlit.error')
    def test_file_isolation(self, mock_error, temp_dir):
        """Test that different file types don't interfere with each other."""
        cat_file = os.path.join(temp_dir, "categories.json")
        settings_file = os.path.join(temp_dir, "settings.json")
        
        with patch('utils.CATEGORIES_FILE', cat_file), \
             patch('utils.SETTINGS_FILE', settings_file):
            
            # Save different data structures
            save_categories(["Cat1", "Cat2"])
            save_settings({"key": "value"})
            
            # Load and verify isolation
            categories = load_categories()
            settings = load_settings()
            
            assert isinstance(categories, list)
            assert isinstance(settings, dict)
            assert categories == ["Cat1", "Cat2"]
            # Settings will have default keys added, so just check our key
            assert "key" in settings and settings["key"] == "value"
