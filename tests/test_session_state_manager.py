"""Tests for SessionStateManager."""

import pytest
from unittest.mock import MagicMock, patch
from session_state_manager import SessionStateManager


class MockSessionState(dict):
    """Mock class to simulate Streamlit's session_state behavior."""
    
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def __contains__(self, key):
        return dict.__contains__(self, key)


class TestSessionStateManager:
    """Tests for SessionStateManager class."""
    
    @patch('session_state_manager.st')
    def test_initialize_with_defaults(self, mock_st):
        """Test initialization with default values."""
        mock_st.session_state = MockSessionState()
        
        categories = ["Category 1", "Category 2"]
        input_history = ["Input 1", "Input 2"]
        settings = {
            "selected_model": "test/model",
            "iterations": 15,
            "patience": 7,
            "use_cache": True
        }
        
        SessionStateManager.initialize(categories, input_history, settings)
        
        # Check that session state was populated
        assert mock_st.session_state['categories'] == categories
        assert mock_st.session_state['input_history'] == input_history
        assert mock_st.session_state['selected_model'] == "test/model"
        assert mock_st.session_state['iterations'] == 15
        assert mock_st.session_state['patience'] == 7
        assert mock_st.session_state['use_cache'] is True
    
    @patch('session_state_manager.st')
    def test_initialize_preserves_existing_state(self, mock_st):
        """Test that initialization doesn't override existing state."""
        mock_st.session_state = MockSessionState({
            'categories': ["Existing Category"],
            'current_tweet': "Existing tweet"
        })
        
        categories = ["New Category"]
        input_history = []
        settings = {}
        
        SessionStateManager.initialize(categories, input_history, settings)
        
        # Existing values should be preserved
        assert mock_st.session_state['categories'] == ["Existing Category"]
        assert mock_st.session_state['current_tweet'] == "Existing tweet"
    
    @patch('session_state_manager.st')
    def test_reset_optimization_state(self, mock_st):
        """Test resetting optimization state."""
        mock_st.session_state = MockSessionState({
            'current_tweet': "Some tweet",
            'best_score': 8.5,
            'iteration_count': 5,
            'optimization_running': True,
            'scores_history': [1, 2, 3],
            'no_improvement_count': 2,
            'generator_inputs': {"test": "data"},
            'evaluator_inputs': {"test": "data"},
            'latest_tweet': "Latest",
            'optimizing_text': "Optimizing"
        })
        
        SessionStateManager.reset_optimization_state()
        
        # All optimization state should be reset
        assert mock_st.session_state['current_tweet'] == ""
        assert mock_st.session_state['best_score'] == 0.0
        assert mock_st.session_state['iteration_count'] == 0
        assert mock_st.session_state['optimization_running'] is False
        assert mock_st.session_state['scores_history'] == []
        assert mock_st.session_state['no_improvement_count'] == 0
        assert mock_st.session_state['generator_inputs'] == {}
        assert mock_st.session_state['evaluator_inputs'] == {}
        assert mock_st.session_state['latest_tweet'] == ""
        assert mock_st.session_state['optimizing_text'] == ""
    
    @patch('session_state_manager.st')
    def test_get_existing_key(self, mock_st):
        """Test getting an existing session state key."""
        mock_st.session_state = {'test_key': 'test_value'}
        
        value = SessionStateManager.get('test_key')
        assert value == 'test_value'
    
    @patch('session_state_manager.st')
    def test_get_missing_key_with_default(self, mock_st):
        """Test getting a missing key with default value."""
        mock_st.session_state = MockSessionState()
        
        value = SessionStateManager.get('missing_key', 'default_value')
        assert value == 'default_value'
    
    @patch('session_state_manager.st')
    def test_set_value(self, mock_st):
        """Test setting a session state value."""
        mock_st.session_state = {}
        
        SessionStateManager.set('test_key', 'test_value')
        assert mock_st.session_state['test_key'] == 'test_value'
    
    @patch('session_state_manager.st')
    def test_update_multiple_values(self, mock_st):
        """Test updating multiple session state values at once."""
        mock_st.session_state = {}
        
        SessionStateManager.update(
            key1='value1',
            key2='value2',
            key3=123
        )
        
        assert mock_st.session_state['key1'] == 'value1'
        assert mock_st.session_state['key2'] == 'value2'
        assert mock_st.session_state['key3'] == 123
