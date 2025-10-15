"""
Session state management for the DSPy Tweet Optimizer.

This module provides a centralized SessionStateManager class to handle
all session state initialization and management, reducing code duplication
and improving maintainability.
"""

import streamlit as st
from typing import Dict, Any, List
from constants import DEFAULT_MODEL, DEFAULT_ITERATIONS, DEFAULT_PATIENCE, DEFAULT_USE_CACHE


class SessionStateManager:
    """Manages Streamlit session state initialization and updates."""
    
    # Define all session state keys and their default values
    STATE_DEFAULTS: Dict[str, Any] = {
        'categories': [],
        'current_tweet': "",
        'best_score': 0.0,
        'iteration_count': 0,
        'optimization_running': False,
        'scores_history': [],
        'selected_model': DEFAULT_MODEL,
        'iterations': DEFAULT_ITERATIONS,
        'patience': DEFAULT_PATIENCE,
        'use_cache': DEFAULT_USE_CACHE,
        'no_improvement_count': 0,
        'generator_inputs': {},
        'evaluator_inputs': {},
        'input_history': [],
        'latest_tweet': "",
        'optimizing_text': "",
        'last_optimized_input': "",
        'main_text_input': "",
        'history_selector': ""
    }
    
    @classmethod
    def initialize(cls, categories: List[str], input_history: List[str], settings: Dict[str, Any]) -> None:
        """
        Initialize all session state variables with defaults and loaded data.
        
        Args:
            categories: List of evaluation categories from storage
            input_history: List of historical inputs from storage
            settings: Dictionary of user settings from storage
        """
        # Initialize categories if not present
        if 'categories' not in st.session_state:
            st.session_state.categories = categories
        
        # Initialize input history if not present
        if 'input_history' not in st.session_state:
            st.session_state.input_history = input_history
        
        # Initialize settings with saved values or defaults
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = settings.get('selected_model', DEFAULT_MODEL)
        
        if 'iterations' not in st.session_state:
            st.session_state.iterations = settings.get('iterations', DEFAULT_ITERATIONS)
        
        if 'patience' not in st.session_state:
            st.session_state.patience = settings.get('patience', DEFAULT_PATIENCE)
        
        if 'use_cache' not in st.session_state:
            st.session_state.use_cache = settings.get('use_cache', DEFAULT_USE_CACHE)
        
        # Initialize all other state variables with defaults
        for key, default_value in cls.STATE_DEFAULTS.items():
            if key not in st.session_state:
                # Skip if already initialized above
                if key not in ['categories', 'input_history', 'selected_model', 'iterations', 'patience', 'use_cache']:
                    st.session_state[key] = default_value
    
    @classmethod
    def reset_optimization_state(cls) -> None:
        """Reset optimization-related state variables."""
        st.session_state.current_tweet = ""
        st.session_state.best_score = 0.0
        st.session_state.iteration_count = 0
        st.session_state.optimization_running = False
        st.session_state.scores_history = []
        st.session_state.no_improvement_count = 0
        st.session_state.generator_inputs = {}
        st.session_state.evaluator_inputs = {}
        st.session_state.latest_tweet = ""
        st.session_state.optimizing_text = ""
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Safely get a session state value.
        
        Args:
            key: Session state key
            default: Default value if key doesn't exist
            
        Returns:
            Session state value or default
        """
        return st.session_state.get(key, default)
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Set a session state value.
        
        Args:
            key: Session state key
            value: Value to set
        """
        st.session_state[key] = value
    
    @classmethod
    def update(cls, **kwargs) -> None:
        """
        Update multiple session state values at once.
        
        Args:
            **kwargs: Key-value pairs to update in session state
        """
        for key, value in kwargs.items():
            st.session_state[key] = value
