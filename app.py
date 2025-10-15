import streamlit as st
import json
import os
import time
from typing import List, Dict
import dspy
import pandas as pd
from dspy_modules import TweetGeneratorModule, TweetEvaluatorModule
from models import EvaluationResult
from hill_climbing import HillClimbingOptimizer
from utils import save_categories, load_categories, initialize_dspy, get_dspy_lm, save_settings, load_settings

# Page configuration
st.set_page_config(
    page_title="DSPy Tweet Optimizer",
    layout="wide"
)

# Custom CSS for pop punk theme
st.markdown("""
<style>
    .main-header {
        color: #ff0000;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .category-item {
        background-color: #1a1a1a;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #ff0000;
        border-radius: 5px;
    }
    .score-display {
        font-size: 1.2rem;
        font-weight: bold;
        color: #ff0000;
    }
    .iteration-info {
        background-color: #1a1a1a;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .best-tweet-container {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-left: 4px solid #ff0000;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .best-tweet-container p {
        font-size: 1.1rem;
        line-height: 1.6;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    # Load saved settings
    settings = load_settings()
    
    if 'categories' not in st.session_state:
        st.session_state.categories = load_categories()
    if 'current_tweet' not in st.session_state:
        st.session_state.current_tweet = ""
    if 'best_score' not in st.session_state:
        st.session_state.best_score = 0
    if 'iteration_count' not in st.session_state:
        st.session_state.iteration_count = 0
    if 'optimization_running' not in st.session_state:
        st.session_state.optimization_running = False
    if 'scores_history' not in st.session_state:
        st.session_state.scores_history = []
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = settings.get("selected_model", "openrouter/anthropic/claude-sonnet-4.5")
    if 'iterations' not in st.session_state:
        st.session_state.iterations = settings.get("iterations", 10)
    if 'patience' not in st.session_state:
        st.session_state.patience = settings.get("patience", 5)
    if 'use_cache' not in st.session_state:
        st.session_state.use_cache = settings.get("use_cache", True)
    if 'no_improvement_count' not in st.session_state:
        st.session_state.no_improvement_count = 0
    if 'generator_inputs' not in st.session_state:
        st.session_state.generator_inputs = {}
    if 'evaluator_inputs' not in st.session_state:
        st.session_state.evaluator_inputs = {}

def main():
    initialize_session_state()

    # Main header
    st.markdown('<h1 class="main-header">DSPy Tweet Optimizer</h1>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Model selection
        st.subheader("Model Settings")
        model_options = {
            "Claude Sonnet 4.5": "openrouter/anthropic/claude-sonnet-4.5",
            "Opus 4.1": "openrouter/anthropic/claude-opus-4.1",
            "Gemini 2.5 Flash": "openrouter/google/gemini-2.5-flash",
            "Gemini 2.5 Flash Lite": "openrouter/google/gemini-2.5-flash-lite",
            "Gemini 2.5 Pro": "openrouter/google/gemini-2.5-pro",
            "GPT-5": "openrouter/openai/gpt-5"
        }
        
        # Find the index of the currently selected model
        reverse_model_options = {v: k for k, v in model_options.items()}
        current_model_name = reverse_model_options.get(st.session_state.selected_model, "Claude Sonnet 4.5")
        current_index = list(model_options.keys()).index(current_model_name)
        
        selected_model_name = st.selectbox(
            "Select Model",
            options=list(model_options.keys()),
            index=current_index
        )
        new_model = model_options[selected_model_name]
        
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
            save_settings({
                "selected_model": st.session_state.selected_model,
                "iterations": st.session_state.iterations,
                "patience": st.session_state.patience,
                "use_cache": st.session_state.use_cache
            })
        
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
            save_settings({
                "selected_model": st.session_state.selected_model,
                "iterations": iterations,
                "patience": patience,
                "use_cache": st.session_state.use_cache
            })
        
        st.divider()
        
        # Category management
        st.subheader("Evaluation Categories")
        
        # Add new category
        with st.expander("Add New Category"):
            new_category = st.text_area("Category Description", placeholder="e.g., Engagement potential of the tweet")
            if st.button("Add Category"):
                if new_category.strip():
                    st.session_state.categories.append(new_category.strip())
                    save_categories(st.session_state.categories)
                    st.success("Category added!")
                    st.rerun()
        
        # Display and manage existing categories
        if st.session_state.categories:
            st.write("Current Categories:")
            for i, category in enumerate(st.session_state.categories):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f'<div class="category-item">{category}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("Delete", key=f"delete_{i}"):
                        st.session_state.categories.pop(i)
                        save_categories(st.session_state.categories)
                        st.rerun()
        else:
            st.warning("No categories defined. Add at least one category to start optimization.")
    
    # Initialize DSPy with selected model and cache settings (after model selector is set)
    try:
        initialize_dspy(st.session_state.selected_model, st.session_state.use_cache)
    except Exception as e:
        st.error(f"Failed to initialize DSPy: {str(e)}")
        return
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Tweet Input")
        input_text = st.text_area(
            "Enter your initial tweet concept:",
            placeholder="Enter the text you want to optimize into a tweet...",
            height=100
        )
        
        # Optimization controls
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            start_optimization = st.button(
                "Start Optimization",
                disabled=not input_text.strip() or len(st.session_state.categories) == 0 or st.session_state.optimization_running
            )
        with col1_2:
            if st.button("Stop Optimization", disabled=not st.session_state.optimization_running):
                st.session_state.optimization_running = False
                st.rerun()
        
        # Current best tweet display
        st.subheader("Current Best Tweet")
        if st.session_state.current_tweet:
            # Use safe container approach - apply styling to container, display content safely
            st.markdown('<div class="best-tweet-container">', unsafe_allow_html=True)
            st.write(st.session_state.current_tweet)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No optimized tweet yet. Start optimization to see results.")
        
        # Generator inputs display
        if st.session_state.generator_inputs:
            st.subheader("Generator Inputs")
            with st.expander("View Generator Inputs", expanded=False):
                st.write("**Input Text:**")
                st.write(st.session_state.generator_inputs.get("input_text", ""))
                
                st.write("**Current Tweet:**")
                current = st.session_state.generator_inputs.get("current_tweet", "")
                st.write(current if current else "(empty for first iteration)")
                
                st.write("**Feedback:**")
                feedback = st.session_state.generator_inputs.get("feedback", "")
                st.write(feedback if feedback else "(empty for first iteration)")
        
        # Evaluator inputs display
        if st.session_state.evaluator_inputs:
            st.subheader("Evaluator Inputs")
            with st.expander("View Evaluator Inputs", expanded=False):
                st.write("**Original Text:**")
                st.write(st.session_state.evaluator_inputs.get("original_text", ""))
                
                st.write("**Current Best Tweet:**")
                current_best = st.session_state.evaluator_inputs.get("current_best_tweet", "")
                st.write(current_best if current_best else "(empty for first iteration)")
                
                st.write("**Tweet Being Evaluated:**")
                st.write(st.session_state.evaluator_inputs.get("tweet_text", ""))
    
    with col2:
        st.subheader("Optimization Stats")
        
        # Iteration info with live update placeholders
        st.markdown(f'<div class="iteration-info">', unsafe_allow_html=True)
        
        # Create placeholders for live updates
        if 'stats_placeholders' not in st.session_state:
            st.session_state.stats_placeholders = {}
        
        iteration_placeholder = st.empty()
        score_placeholder = st.empty()
        no_improvement_placeholder = st.empty()
        
        # Display current values
        iteration_placeholder.write(f"**Iteration:** {st.session_state.iteration_count}")
        score_placeholder.write(f"**Best Score:** {st.session_state.best_score:.2f}")
        no_improvement_placeholder.write(f"**No Improvement:** {st.session_state.no_improvement_count}/{st.session_state.patience}")
        
        # Store placeholders in session state for use in optimization loop
        st.session_state.stats_placeholders = {
            'iteration': iteration_placeholder,
            'score': score_placeholder,
            'no_improvement': no_improvement_placeholder
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Score breakdown
        if st.session_state.scores_history and len(st.session_state.scores_history) > 0:
            latest_scores = st.session_state.scores_history[-1]
            st.subheader("Latest Scores")
            for i, (category, score) in enumerate(zip(st.session_state.categories, latest_scores.category_scores)):
                st.markdown(f'<div class="score-display">{category[:30]}...: {score}/9</div>', unsafe_allow_html=True)
        
        # Progress visualization
        if len(st.session_state.scores_history) > 0:
            st.subheader("Score History")
            scores = [sum(score.category_scores)/len(score.category_scores) for score in st.session_state.scores_history]
            st.line_chart(scores)

    # Start optimization process
    if start_optimization:
        st.session_state.optimization_running = True
        st.session_state.iteration_count = 0
        st.session_state.current_tweet = input_text
        st.session_state.scores_history = []
        st.session_state.no_improvement_count = 0
        st.session_state.generator_inputs = {}
        st.session_state.evaluator_inputs = {}
        
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
        
        # Create progress placeholders
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Run optimization with selected model using dspy.context
            early_stop = False
            with dspy.context(lm=selected_lm):
                for iteration, (current_tweet, scores, is_improvement, patience_counter, generator_inputs, evaluator_inputs) in enumerate(
                    optimizer.optimize(input_text)
                ):
                    st.session_state.iteration_count = iteration + 1
                    st.session_state.scores_history.append(scores)
                    st.session_state.no_improvement_count = patience_counter
                    st.session_state.generator_inputs = generator_inputs
                    st.session_state.evaluator_inputs = evaluator_inputs
                    
                    if is_improvement:
                        st.session_state.current_tweet = current_tweet
                        st.session_state.best_score = sum(scores.category_scores) / len(scores.category_scores)
                    
                    # Update live stats if placeholders exist
                    if 'stats_placeholders' in st.session_state:
                        st.session_state.stats_placeholders['iteration'].write(f"**Iteration:** {st.session_state.iteration_count}")
                        st.session_state.stats_placeholders['score'].write(f"**Best Score:** {st.session_state.best_score:.2f}")
                        st.session_state.stats_placeholders['no_improvement'].write(f"**No Improvement:** {st.session_state.no_improvement_count}/{patience}")
                    
                    # Check if we'll stop due to patience on next iteration
                    if patience_counter >= patience:
                        early_stop = True
                    
                    # Update progress
                    progress_bar.progress((iteration + 1) / iterations)
                    if early_stop:
                        status_text.write(f"Stopped early at iteration {iteration + 1} - No improvement for {patience} iterations")
                    else:
                        status_text.write(f"Iteration {iteration + 1}/{iterations} - {'Improved!' if is_improvement else 'No improvement'}")
                    
                    # Brief pause to allow UI to update visibly
                    time.sleep(0.1)
                    
                    if not st.session_state.optimization_running:
                        break
                
        except Exception as e:
            st.error(f"Optimization failed: {str(e)}")
        finally:
            st.session_state.optimization_running = False
            progress_bar.progress(1.0)
            if early_stop:
                status_text.write(f"Optimization stopped - No improvement for {patience} iterations")
            else:
                status_text.write("Optimization completed!")
            # Rerun once at the end to show final results
            st.rerun()
    
    # Detailed Score History Graph (full width)
    if st.session_state.scores_history and len(st.session_state.scores_history) > 0:
        st.divider()
        st.subheader("Detailed Score History")
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Average Score", "Category Breakdown"])
        
        with tab1:
            # Average score over iterations
            avg_scores = [sum(score.category_scores)/len(score.category_scores) for score in st.session_state.scores_history]
            
            df_avg = pd.DataFrame({
                'Iteration': list(range(1, len(avg_scores) + 1)),
                'Average Score': avg_scores
            })
            
            st.line_chart(df_avg.set_index('Iteration'), use_container_width=True, height=400)
            
            # Display statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Starting Score", f"{avg_scores[0]:.2f}")
            with col2:
                st.metric("Current Score", f"{avg_scores[-1]:.2f}")
            with col3:
                improvement = avg_scores[-1] - avg_scores[0]
                st.metric("Total Improvement", f"{improvement:.2f}", delta=f"{improvement:.2f}")
        
        with tab2:
            # Individual category scores over iterations
            if st.session_state.categories:
                # Build dataframe with all category scores
                data = {'Iteration': list(range(1, len(st.session_state.scores_history) + 1))}
                
                for i, category in enumerate(st.session_state.categories):
                    category_name = category[:30] + "..." if len(category) > 30 else category
                    data[category_name] = [score.category_scores[i] for score in st.session_state.scores_history]
                
                df_categories = pd.DataFrame(data)
                st.line_chart(df_categories.set_index('Iteration'), use_container_width=True, height=400)
                
                # Show improvement per category
                st.subheader("Category Improvements")
                for i, category in enumerate(st.session_state.categories):
                    initial_score = st.session_state.scores_history[0].category_scores[i]
                    current_score = st.session_state.scores_history[-1].category_scores[i]
                    improvement = current_score - initial_score
                    
                    st.markdown(
                        f'<div class="category-item">'
                        f'<strong>{category[:50]}</strong><br>'
                        f'Start: {initial_score}/9 → Current: {current_score}/9 '
                        f'<span style="color: {"#00ff00" if improvement > 0 else "#ff0000" if improvement < 0 else "#ffffff"}">({improvement:+.0f})</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main()
