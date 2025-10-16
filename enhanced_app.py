"""
Enhanced DSPy Tweet Optimizer with Advanced LLM Integration.

This application extends the original tweet optimizer with:
- Multiple LLM providers (Ollama, Perplexity, OpenRouter)
- GEPA-ACE context optimization
- Web search capabilities
- Hybrid optimization strategies
- Advanced performance tracking
"""

import streamlit as st
import time
import dspy
from typing import Optional, Dict, Any
import logging

# Import enhanced modules
from enhanced_dspy_modules import (
    EnhancedTweetGeneratorModule, 
    EnhancedTweetEvaluatorModule,
    get_enhanced_modules,
    initialize_enhanced_system
)
from advanced_llm_manager import advanced_llm_manager, setup_advanced_llm_system
from enhanced_ui_components import (
    render_enhanced_custom_css,
    render_enhanced_main_interface,
    render_enhanced_sidebar,
    render_system_status_banner,
    render_web_context_display,
    render_enhanced_optimization_stats
)
from enhanced_constants import (
    OPTIMIZATION_STRATEGIES,
    ENHANCED_CATEGORIES,
    FEATURE_FLAGS
)

# Import original modules for fallback
from models import EvaluationResult
from hill_climbing import HillClimbingOptimizer
from utils import save_settings, load_settings, load_categories, load_input_history
from session_state_manager import SessionStateManager
from optimization_manager import OptimizationManager
from helpers import build_settings_dict
from constants import (
    PAGE_TITLE,
    PAGE_LAYOUT,
    DEFAULT_ITERATIONS,
    DEFAULT_PATIENCE,
    DEFAULT_USE_CACHE,
    ITERATION_SLEEP_TIME,
    MAIN_COL_INPUT,
    MAIN_COL_STATS,
    INPUT_HEIGHT,
    HISTORY_RECENT_INDICATOR,
    HISTORY_RECENT_COUNT,
    HISTORY_TRUNCATE_LENGTH
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=f"{PAGE_TITLE} - Enhanced",
    layout=PAGE_LAYOUT
)

# Custom CSS
render_enhanced_custom_css()

def initialize_enhanced_session_state() -> None:
    """Initialize session state with enhanced features."""
    settings = load_settings()
    categories = load_categories()
    input_history = load_input_history()
    
    # Use enhanced categories if available
    if FEATURE_FLAGS.get("enable_advanced_categories", True) and not categories:
        categories = ENHANCED_CATEGORIES
    
    # Initialize original session state
    SessionStateManager.initialize(categories, input_history, settings)
    
    # Add enhanced session state variables
    if 'enhanced_mode' not in st.session_state:
        st.session_state.enhanced_mode = True
    
    if 'selected_strategy' not in st.session_state:
        st.session_state.selected_strategy = "hybrid_balanced"
    
    if 'selected_provider' not in st.session_state:
        st.session_state.selected_provider = None
    
    if 'web_context' not in st.session_state:
        st.session_state.web_context = ""
    
    if 'performance_metrics' not in st.session_state:
        st.session_state.performance_metrics = {}

def initialize_enhanced_system_safely():
    """Initialize the enhanced system with error handling."""
    try:
        # Set up advanced LLM manager
        setup_advanced_llm_system()
        
        # Initialize enhanced modules
        enhanced_modules = initialize_enhanced_system()
        
        logger.info("Enhanced system initialized successfully")
        return enhanced_modules
        
    except Exception as e:
        logger.error(f"Failed to initialize enhanced system: {e}")
        st.warning(f"⚠️ Enhanced features unavailable: {str(e)}")
        st.info("💡 **Tips for enabling enhanced features:**")
        st.info("• **For local LLMs**: Install Ollama and start the service")
        st.info("• **For web search**: Set PERPLEXITY_API_KEY environment variable")
        st.info("• **For cloud models**: Set OPENROUTER_API_KEY environment variable")
        st.info("• **For full setup**: Run `python setup_advanced_system.py`")
        return None

def render_enhanced_tweet_input():
    """Render enhanced tweet input with web context display."""
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
    
    # Enhanced features for input
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Analyze with Web Search", use_container_width=True):
            if input_text.strip():
                # Trigger web search analysis
                st.session_state.web_context = "Searching for relevant context..."
                st.rerun()
    
    with col2:
        if st.button("🧠 Smart Optimization", use_container_width=True):
            if input_text.strip():
                # Use enhanced optimization
                st.session_state.selected_strategy = "web_enhanced"
                st.rerun()
    
    # Rerun button
    if input_text.strip() and len(st.session_state.categories) > 0 and not st.session_state.optimization_running:
        if st.button("🔄 Rerun Optimization", use_container_width=True):
            st.session_state.last_optimized_input = ""
            st.rerun()
    
    return input_text

def run_enhanced_optimization(input_text: str, enhanced_modules: Dict[str, Any], 
                            selected_strategy: str, selected_provider: Optional[str],
                            iterations: int, patience: int):
    """Run optimization using enhanced modules and strategies."""
    
    # Get strategy configuration
    strategy_config = OPTIMIZATION_STRATEGIES.get(selected_strategy, {})
    
    # Create enhanced optimizer
    optimizer = HillClimbingOptimizer(
        generator=enhanced_modules["generator"],
        evaluator=enhanced_modules["evaluator"],
        categories=st.session_state.categories,
        max_iterations=iterations,
        patience=patience
    )
    
    # Create optimization manager
    optimization_manager = OptimizationManager(optimizer)
    
    # Set up progress tracking
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        # Run optimization with enhanced features
        optimization_manager.run_optimization(
            input_text=input_text,
            iterations=iterations,
            patience=patience,
            progress_placeholder=progress_placeholder,
            status_placeholder=status_placeholder
        )
        
        # Update performance metrics
        if hasattr(optimization_manager, 'get_performance_metrics'):
            st.session_state.performance_metrics = optimization_manager.get_performance_metrics()
        
    except Exception as e:
        st.error(f"Enhanced optimization failed: {str(e)}")
        logger.error(f"Optimization error: {e}")
    finally:
        st.session_state.optimization_running = False
        progress_placeholder.progress(1.0)
        optimization_manager.display_completion_message(status_placeholder)

def main() -> None:
    """Main enhanced application entry point."""
    
    # Initialize session state
    initialize_enhanced_session_state()
    
    # Initialize enhanced system
    enhanced_modules = initialize_enhanced_system_safely()
    
    # Render enhanced interface
    render_enhanced_main_interface()
    
    # System status banner
    render_system_status_banner()
    
    # Enhanced sidebar
    selected_strategy, selected_provider = render_enhanced_sidebar()
    
    # Update session state with selections
    if selected_strategy:
        st.session_state.selected_strategy = selected_strategy
    if selected_provider:
        st.session_state.selected_provider = selected_provider
    
    # Main content area
    col1, col2 = st.columns([MAIN_COL_INPUT, MAIN_COL_STATS])
    
    with col1:
        # Enhanced tweet input
        input_text = render_enhanced_tweet_input()
        
        # Progress bar and status placeholders
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Current best tweet display
        from ui_components import render_best_tweet_display
        render_best_tweet_display(st.session_state.current_tweet)
        
        # Web context display
        if st.session_state.get('web_context'):
            render_web_context_display(st.session_state.web_context)
        
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
        from ui_components import render_generator_inputs, render_evaluator_inputs
        render_generator_inputs(st.session_state.generator_inputs)
        render_evaluator_inputs(st.session_state.evaluator_inputs)
    
    with col2:
        # Enhanced optimization stats
        render_enhanced_optimization_stats(
            st.session_state.iteration_count,
            st.session_state.best_score,
            st.session_state.no_improvement_count,
            st.session_state.patience,
            st.session_state.selected_strategy,
            st.session_state.selected_provider
        )
        
        # Latest evaluation with reasoning
        if st.session_state.scores_history and len(st.session_state.scores_history) > 0:
            from ui_components import render_latest_evaluation
            latest_evaluation = st.session_state.scores_history[-1]
            render_latest_evaluation(latest_evaluation, st.session_state.categories)
        
        # Progress visualization
        if len(st.session_state.scores_history) > 0:
            st.subheader("Score History")
            scores = [sum(score.category_scores)/len(score.category_scores) for score in st.session_state.scores_history]
            st.line_chart(scores)
    
    # Auto-start optimization when input is available
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
        
        # Track this input as optimized
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
        
        # Trigger immediate rerun
        st.rerun()
    
    # Run optimization if it's marked as running
    if st.session_state.optimization_running and hasattr(st.session_state, 'optimizing_text'):
        
        if enhanced_modules:
            # Use enhanced optimization
            run_enhanced_optimization(
                input_text=st.session_state.optimizing_text,
                enhanced_modules=enhanced_modules,
                selected_strategy=st.session_state.selected_strategy,
                selected_provider=st.session_state.selected_provider,
                iterations=st.session_state.iterations,
                patience=st.session_state.patience
            )
        else:
            # Fallback to original optimization using original modules
            st.warning("Using fallback optimization mode - enhanced features unavailable")
            
            # Use original DSPy modules as fallback
            from dspy_modules import TweetGeneratorModule, TweetEvaluatorModule
            from hill_climbing import HillClimbingOptimizer
            from optimization_manager import OptimizationManager
            
            # Create fallback optimizer
            optimizer = HillClimbingOptimizer(
                generator=TweetGeneratorModule(),
                evaluator=TweetEvaluatorModule(),
                categories=st.session_state.categories,
                max_iterations=st.session_state.iterations,
                patience=st.session_state.patience
            )
            
            # Create optimization manager
            optimization_manager = OptimizationManager(optimizer)
            
            # Set up progress tracking
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            
            try:
                # Run optimization with fallback modules
                optimization_manager.run_optimization(
                    input_text=st.session_state.optimizing_text,
                    iterations=st.session_state.iterations,
                    patience=st.session_state.patience,
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
    
    # Detailed Score History Graph
    if st.session_state.scores_history and len(st.session_state.scores_history) > 0:
        from ui_components import render_score_history
        render_score_history(st.session_state.scores_history, st.session_state.categories)

if __name__ == "__main__":
    main()
