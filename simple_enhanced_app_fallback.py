#!/usr/bin/env python3
"""
Simplified Enhanced DSPy Tweet Optimizer - Fallback Version

This version doesn't use the get_available_models() function
to avoid any import issues on Streamlit Cloud.
"""

import streamlit as st
import time
import dspy
from dspy_modules import TweetGeneratorModule, TweetEvaluatorModule
from models import EvaluationResult
from hill_climbing import HillClimbingOptimizer
from utils import initialize_dspy, get_dspy_lm, save_settings, load_settings, load_categories, load_input_history
from session_state_manager import SessionStateManager
from optimization_manager import OptimizationManager
from ui_components import (
    render_custom_css,
    render_main_header,
    render_category_management,
    render_best_tweet_display,
    render_generator_inputs,
    render_evaluator_inputs,
    render_optimization_stats,
    render_latest_evaluation,
    render_score_history
)
from helpers import build_settings_dict
from constants import (
    PAGE_TITLE,
    PAGE_LAYOUT,
    AVAILABLE_MODELS,
    DEFAULT_MODEL,
    DEFAULT_ITERATIONS,
    DEFAULT_PATIENCE,
    DEFAULT_USE_CACHE,
    ITERATION_SLEEP_TIME,
    SIDEBAR_COL_CATEGORY,
    SIDEBAR_COL_DELETE,
    MAIN_COL_INPUT,
    MAIN_COL_STATS,
    INPUT_HEIGHT,
    HISTORY_RECENT_INDICATOR,
    HISTORY_RECENT_COUNT,
    HISTORY_TRUNCATE_LENGTH
)

# Page configuration
st.set_page_config(
    page_title=f"{PAGE_TITLE} - Enhanced",
    layout=PAGE_LAYOUT
)

# Custom CSS
render_custom_css()

def initialize_session_state() -> None:
    """Initialize session state variables with saved settings."""
    settings = load_settings()
    categories = load_categories()
    input_history = load_input_history()
    
    # Use SessionStateManager for cleaner initialization
    SessionStateManager.initialize(categories, input_history, settings)

def render_sidebar_configuration() -> tuple:
    """
    Render sidebar configuration UI.
    
    Returns:
        Tuple of (selected_model, iterations, patience)
    """
    with st.sidebar:
        st.header("Configuration")
        
        # Model selection
        st.subheader("Model Settings")
        
        # Find the index of the currently selected model
        reverse_model_options = {v: k for k, v in AVAILABLE_MODELS.items()}
        current_model_name = reverse_model_options.get(st.session_state.selected_model, "Claude Sonnet 4.5")
        
        # Handle case where current model is not available (e.g., Ollama model when Ollama is not running)
        if current_model_name not in AVAILABLE_MODELS:
            current_model_name = "Claude Sonnet 4.5"
            st.session_state.selected_model = AVAILABLE_MODELS[current_model_name]
        
        current_index = list(AVAILABLE_MODELS.keys()).index(current_model_name)
        
        selected_model_name = st.selectbox(
            "Select Model",
            options=list(AVAILABLE_MODELS.keys()),
            index=current_index
        )
        new_model = AVAILABLE_MODELS[selected_model_name]
        
        # Cache control
        use_cache = st.checkbox(
            "Enable DSPy Cache",
            value=st.session_state.use_cache,
            help="Enable DSPy's built-in caching to save API costs and speed up repeated queries"
        )
        
        # Save settings if model or cache changed
        if new_model != st.session_state.selected_model or use_cache != st.session_state.use_cache:
            st.session_state.selected_model = new_model
            st.session_state.use_cache = use_cache
            save_settings(build_settings_dict(
                st.session_state.selected_model,
                st.session_state.iterations,
                st.session_state.patience,
                st.session_state.use_cache
            ))
        
        st.divider()
        
        # Optimization parameters
        st.subheader("Optimization Settings")
        iterations = st.number_input(
            "Iterations (n)", 
            min_value=1, 
            max_value=100, 
            value=st.session_state.iterations,
            key="iterations_input"
        )
        patience = st.number_input(
            "Patience", 
            min_value=1, 
            max_value=50, 
            value=st.session_state.patience,
            key="patience_input"
        )
        
        # Save settings if iterations or patience changed
        if iterations != st.session_state.iterations or patience != st.session_state.patience:
            st.session_state.iterations = iterations
            st.session_state.patience = patience
            save_settings(build_settings_dict(
                st.session_state.selected_model,
                iterations,
                patience,
                st.session_state.use_cache
            ))
        
        st.divider()
        
        # Category management
        render_category_management(st.session_state.categories)
    
    return new_model, iterations, patience

def main() -> None:
    """Main application entry point."""
    initialize_session_state()

    # Enhanced header
    st.markdown("""
    <div style="background-color: #2a2a2a; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
        <h1 style="color: #ff0000; margin: 0;">🚀 Enhanced DSPy Tweet Optimizer</h1>
        <p style="margin: 0.5rem 0 0 0; color: #cccccc;">
            AI-powered tweet optimization with enhanced features
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    selected_model, iterations, patience = render_sidebar_configuration()
    
    # Initialize DSPy with selected model and cache settings
    try:
        initialize_dspy(st.session_state.selected_model, st.session_state.use_cache)
    except Exception as e:
        st.error(f"Failed to initialize DSPy: {str(e)}")
        return
    
    # Main content area
    col1, col2 = st.columns([MAIN_COL_INPUT, MAIN_COL_STATS])
    
    with col1:
        st.subheader("📝 Tweet Input")
        
        # Initialize main text input in session state if not exists
        if 'main_text_input' not in st.session_state:
            st.session_state.main_text_input = ""
        
        # Callback function for history selection
        def on_history_select():
            if st.session_state.history_selector:
                st.session_state.main_text_input = st.session_state.history_selector
                st.session_state.history_selector = ""
        
        # Input history dropdown (most recent first)
        if st.session_state.input_history:
            def format_history_option(x):
                if x == "":
                    return "Select from history..."
                idx = st.session_state.input_history.index(x) if x in st.session_state.input_history else -1
                prefix = HISTORY_RECENT_INDICATOR if idx < HISTORY_RECENT_COUNT else ""
                truncated = x[:HISTORY_TRUNCATE_LENGTH] + "..." if len(x) > HISTORY_TRUNCATE_LENGTH else x
                return f"{prefix}{truncated}"
            
            st.selectbox(
                "Load from history:",
                options=[""] + st.session_state.input_history,
                format_func=format_history_option,
                key="history_selector",
                on_change=on_history_select
            )
        
        # Text area
        input_text = st.text_area(
            "Enter your initial tweet concept:",
            placeholder="Enter the text you want to optimize into a tweet...",
            height=INPUT_HEIGHT,
            key="main_text_input"
        )
        
        # Enhanced buttons
        col1_btn, col2_btn = st.columns(2)
        
        with col1_btn:
            if st.button("🧠 Smart Optimization", use_container_width=True):
                if input_text.strip():
                    st.session_state.last_optimized_input = ""
                    st.success("🧠 Smart optimization triggered!")
                    st.rerun()
                else:
                    st.warning("Please enter some text first!")
        
        with col2_btn:
            if st.button("🔄 Rerun Optimization", use_container_width=True):
                if input_text.strip() and len(st.session_state.categories) > 0:
                    st.session_state.last_optimized_input = ""
                    st.success("🔄 Optimization rerun triggered!")
                    st.rerun()
                elif input_text.strip():
                    st.warning("Please add evaluation categories in the sidebar!")
                else:
                    st.warning("Please enter some text first!")
        
        # Progress bar and status placeholders
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Current best tweet display
        render_best_tweet_display(st.session_state.current_tweet)
        
        # Latest tweet display
        if (st.session_state.latest_tweet and 
            st.session_state.latest_tweet != st.session_state.current_tweet and
            st.session_state.scores_history):
            st.subheader("Latest Generated Tweet")
            st.markdown('<div class="best-tweet-container" style="background-color: #2a2a2a;">', unsafe_allow_html=True)
            st.write(st.session_state.latest_tweet)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption("🔄 Most recent attempt - didn't improve the score")
        
        # Generator and evaluator inputs display
        render_generator_inputs(st.session_state.generator_inputs)
        render_evaluator_inputs(st.session_state.evaluator_inputs)
    
    with col2:
        # Optimization stats
        st.session_state.stats_placeholders = render_optimization_stats(
            st.session_state.iteration_count,
            st.session_state.best_score,
            st.session_state.no_improvement_count,
            st.session_state.patience
        )
        
        # Latest evaluation with reasoning
        if st.session_state.scores_history and len(st.session_state.scores_history) > 0:
            latest_evaluation = st.session_state.scores_history[-1]
            render_latest_evaluation(latest_evaluation, st.session_state.categories)
        
        # Progress visualization
        if len(st.session_state.scores_history) > 0:
            st.subheader("Score History")
            scores = [sum(score.category_scores)/len(score.category_scores) for score in st.session_state.scores_history]
            st.line_chart(scores)

    # Auto-start optimization when input is available and different from last optimized
    should_optimize = (
        input_text.strip() and 
        len(st.session_state.categories) > 0 and 
        not st.session_state.optimization_running and
        input_text.strip() != st.session_state.last_optimized_input
    )
    
    if should_optimize:
        from utils import add_to_input_history, save_input_history
        
        # Add input to history
        st.session_state.input_history = add_to_input_history(st.session_state.input_history, input_text)
        save_input_history(st.session_state.input_history)
        
        # Track this input as optimized and set initial current_tweet
        st.session_state.optimizing_text = input_text.strip()
        st.session_state.last_optimized_input = input_text.strip()
        st.session_state.current_tweet = input_text
        st.session_state.latest_tweet = ""
        st.session_state.optimization_running = True
        st.session_state.iteration_count = 0
        st.session_state.scores_history = []
        st.session_state.no_improvement_count = 0
        st.session_state.generator_inputs = {}
        st.session_state.evaluator_inputs = {}
        
        # Trigger immediate rerun to show initial state and start optimization
        st.rerun()
    
    # Run optimization if it's marked as running
    if st.session_state.optimization_running and hasattr(st.session_state, 'optimizing_text'):
        # Get the LM for the selected model
        selected_lm = get_dspy_lm(st.session_state.selected_model)
        
        # Initialize optimizer
        optimizer = HillClimbingOptimizer(
            generator=TweetGeneratorModule(),
            evaluator=TweetEvaluatorModule(),
            categories=st.session_state.categories,
            max_iterations=iterations,
            patience=patience
        )
        
        # Create optimization manager
        optimization_manager = OptimizationManager(optimizer)
        
        try:
            # Run optimization with selected model using dspy.context
            with dspy.context(lm=selected_lm):
                optimization_manager.run_optimization(
                    input_text=st.session_state.optimizing_text,
                    iterations=iterations,
                    patience=patience,
                    progress_placeholder=progress_placeholder,
                    status_placeholder=status_placeholder
                )
        except Exception as e:
            st.error(f"Optimization failed: {str(e)}")
        finally:
            st.session_state.optimization_running = False
            progress_placeholder.progress(1.0)
            optimization_manager.display_completion_message(status_placeholder)
            st.rerun()
    
    # Detailed Score History Graph (full width)
    if st.session_state.scores_history and len(st.session_state.scores_history) > 0:
        render_score_history(st.session_state.scores_history, st.session_state.categories)

if __name__ == "__main__":
    main()
