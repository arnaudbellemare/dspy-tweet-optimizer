"""Integration tests for file operations."""

import pytest
import os
import json
from utils import (
    save_categories, load_categories,
    save_settings, load_settings,
    add_to_input_history, load_input_history
)


class TestCategoryFileOperations:
    """Integration tests for category file operations."""
    
    def test_save_and_load_categories(self, temp_dir, sample_categories):
        """Test saving and loading categories from actual files."""
        filepath = os.path.join(temp_dir, "categories.json")
        
        # Save categories
        save_categories(sample_categories, filepath)
        
        # Verify file exists
        assert os.path.exists(filepath)
        
        # Load categories
        loaded = load_categories(filepath)
        
        # Verify content
        assert loaded == sample_categories
    
    def test_load_categories_creates_default_file(self, temp_dir):
        """Test that loading from non-existent file creates default."""
        filepath = os.path.join(temp_dir, "categories.json")
        
        # File doesn't exist yet
        assert not os.path.exists(filepath)
        
        # Load should create default
        loaded = load_categories(filepath)
        
        # Should return default categories
        assert isinstance(loaded, list)
        assert len(loaded) > 0
        
        # File should now exist
        assert os.path.exists(filepath)
    
    def test_categories_persistence_across_operations(self, temp_dir):
        """Test that categories persist correctly across multiple operations."""
        filepath = os.path.join(temp_dir, "categories.json")
        
        # Save initial categories
        initial = ["Category1", "Category2"]
        save_categories(initial, filepath)
        
        # Load and verify
        loaded1 = load_categories(filepath)
        assert loaded1 == initial
        
        # Update categories
        updated = ["Category1", "Category2", "Category3"]
        save_categories(updated, filepath)
        
        # Load and verify update
        loaded2 = load_categories(filepath)
        assert loaded2 == updated
        assert len(loaded2) == 3


class TestSettingsFileOperations:
    """Integration tests for settings file operations."""
    
    def test_save_and_load_settings(self, temp_dir, sample_settings):
        """Test saving and loading settings from actual files."""
        filepath = os.path.join(temp_dir, "settings.json")
        
        # Save settings
        save_settings(sample_settings, filepath)
        
        # Verify file exists
        assert os.path.exists(filepath)
        
        # Load settings
        loaded = load_settings(filepath)
        
        # Verify content
        assert loaded == sample_settings
        assert loaded['model'] == sample_settings['model']
        assert loaded['iterations'] == sample_settings['iterations']
    
    def test_load_settings_returns_empty_dict_for_missing_file(self, temp_dir):
        """Test loading from non-existent settings file."""
        filepath = os.path.join(temp_dir, "settings.json")
        
        # Load from non-existent file
        loaded = load_settings(filepath)
        
        # Should return empty dict
        assert loaded == {}
        
        # File should NOT be created (settings work differently from categories)
        assert not os.path.exists(filepath)
    
    def test_settings_update_workflow(self, temp_dir):
        """Test complete settings update workflow."""
        filepath = os.path.join(temp_dir, "settings.json")
        
        # Initial settings
        settings_v1 = {
            "model": "model-v1",
            "iterations": 10
        }
        save_settings(settings_v1, filepath)
        
        # Load and modify
        loaded = load_settings(filepath)
        loaded["iterations"] = 20
        loaded["patience"] = 5
        
        # Save modified settings
        save_settings(loaded, filepath)
        
        # Verify persistence
        final = load_settings(filepath)
        assert final["model"] == "model-v1"
        assert final["iterations"] == 20
        assert final["patience"] == 5


class TestInputHistoryOperations:
    """Integration tests for input history operations."""
    
    def test_add_and_load_history(self, temp_dir):
        """Test adding to and loading input history."""
        filepath = os.path.join(temp_dir, "input_history.json")
        
        # Add first input
        add_to_input_history("First input", filepath)
        
        # Verify file exists
        assert os.path.exists(filepath)
        
        # Load and verify
        history = load_input_history(filepath)
        assert "First input" in history
    
    def test_history_deduplication(self, temp_dir):
        """Test that duplicate inputs are deduplicated."""
        filepath = os.path.join(temp_dir, "input_history.json")
        
        # Add inputs with duplicates
        add_to_input_history("Input 1", filepath)
        add_to_input_history("Input 2", filepath)
        add_to_input_history("Input 1", filepath)  # Duplicate
        
        # Load history
        history = load_input_history(filepath)
        
        # Should have only 2 unique items
        assert len(history) == 2
        
        # Most recent occurrence should be last
        assert history[-1] == "Input 1"
    
    def test_history_size_limit(self, temp_dir):
        """Test that history respects maximum size limit."""
        filepath = os.path.join(temp_dir, "input_history.json")
        
        # Add more than max items (max is 50)
        for i in range(60):
            add_to_input_history(f"Input {i}", filepath)
        
        # Load history
        history = load_input_history(filepath)
        
        # Should be limited to 50 items
        assert len(history) <= 50
        
        # Should keep most recent items
        assert "Input 59" in history
        assert "Input 0" not in history
    
    def test_empty_inputs_ignored(self, temp_dir):
        """Test that empty inputs are not added to history."""
        filepath = os.path.join(temp_dir, "input_history.json")
        
        # Try to add empty and whitespace inputs
        add_to_input_history("", filepath)
        add_to_input_history("   ", filepath)
        add_to_input_history("Valid input", filepath)
        
        # Load history
        history = load_input_history(filepath)
        
        # Should only have valid input
        assert len(history) == 1
        assert history[0] == "Valid input"


class TestCrossFileOperations:
    """Integration tests for operations involving multiple files."""
    
    def test_complete_workflow_with_all_files(self, temp_dir, sample_categories, sample_settings):
        """Test a complete workflow using all configuration files."""
        cat_file = os.path.join(temp_dir, "categories.json")
        settings_file = os.path.join(temp_dir, "settings.json")
        history_file = os.path.join(temp_dir, "input_history.json")
        
        # Save all configurations
        save_categories(sample_categories, cat_file)
        save_settings(sample_settings, settings_file)
        add_to_input_history("Test input", history_file)
        
        # Verify all files exist
        assert os.path.exists(cat_file)
        assert os.path.exists(settings_file)
        assert os.path.exists(history_file)
        
        # Load all configurations
        categories = load_categories(cat_file)
        settings = load_settings(settings_file)
        history = load_input_history(history_file)
        
        # Verify all data
        assert categories == sample_categories
        assert settings == sample_settings
        assert "Test input" in history
    
    def test_file_isolation(self, temp_dir):
        """Test that different file types don't interfere with each other."""
        cat_file = os.path.join(temp_dir, "categories.json")
        settings_file = os.path.join(temp_dir, "settings.json")
        
        # Save different data structures
        save_categories(["Cat1", "Cat2"], cat_file)
        save_settings({"key": "value"}, settings_file)
        
        # Load and verify isolation
        categories = load_categories(cat_file)
        settings = load_settings(settings_file)
        
        assert isinstance(categories, list)
        assert isinstance(settings, dict)
        assert categories == ["Cat1", "Cat2"]
        assert settings == {"key": "value"}
