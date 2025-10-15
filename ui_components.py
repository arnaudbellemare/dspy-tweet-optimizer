"""
UI component functions for the DSPy Tweet Optimizer.

This module contains reusable UI components to improve code organization
and maintainability.
"""

import streamlit as st
from typing import List, Dict, Any
import pandas as pd
from models import EvaluationResult
from constants import (
    COLOR_PRIMARY,
    COLOR_BACKGROUND_DARK,
    COLOR_SUCCESS,
    COLOR_FAILURE,
    COLOR_NEUTRAL,
    CATEGORY_DISPLAY_MAX_LENGTH,
    CATEGORY_IMPROVEMENT_MAX_LENGTH,
    CHART_HEIGHT,
    MAX_SCORE
)
from helpers import truncate_category_display


def render_custom_css() -> None:
    """Render custom CSS for the application theme."""
    st.markdown(f"""
    <style>
        .main-header {{
            color: {COLOR_PRIMARY};
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 2rem;
        }}
        .category-item {{
            background-color: {COLOR_BACKGROUND_DARK};
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 3px solid {COLOR_PRIMARY};
            border-radius: 5px;
        }}
        .score-display {{
            font-size: 1.2rem;
            font-weight: bold;
            color: {COLOR_PRIMARY};
        }}
        .iteration-info {{
            background-color: {COLOR_BACKGROUND_DARK};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        .best-tweet-container {{
            background-color: {COLOR_BACKGROUND_DARK};
            padding: 1.5rem;
            border-left: 4px solid {COLOR_PRIMARY};
            border-radius: 5px;
            margin: 0.5rem 0;
        }}
        .best-tweet-container p {{
            font-size: 1.1rem;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 0;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_main_header() -> None:
    """Render the main application header."""
    st.markdown('<h1 class="main-header">DSPy Tweet Optimizer</h1>', unsafe_allow_html=True)


def render_category_management(categories: List[str]) -> None:
    """
    Render category management UI in the sidebar.
    
    Args:
        categories: List of current evaluation categories
    """
    st.subheader("Evaluation Categories")
    
    # Add new category
    with st.expander("Add New Category"):
        new_category = st.text_area("Category Description", placeholder="e.g., Engagement potential of the tweet")
        if st.button("Add Category"):
            if new_category.strip():
                st.session_state.categories.append(new_category.strip())
                from utils import save_categories
                save_categories(st.session_state.categories)
                st.success("Category added!")
                st.rerun()
    
    # Display and manage existing categories
    if categories:
        st.write("Current Categories:")
        for i, category in enumerate(categories):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="category-item">{category}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("Delete", key=f"delete_{i}"):
                    st.session_state.categories.pop(i)
                    from utils import save_categories
                    save_categories(st.session_state.categories)
                    st.rerun()
    else:
        st.warning("No categories defined. Add at least one category to enable optimization.")


def render_best_tweet_display(current_tweet: str) -> None:
    """
    Render the best tweet display.
    
    Args:
        current_tweet: The current best tweet text
    """
    st.subheader("Current Best Tweet")
    if current_tweet:
        st.markdown('<div class="best-tweet-container">', unsafe_allow_html=True)
        st.write(current_tweet)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No optimized tweet yet. Enter text above to automatically optimize.")


def render_generator_inputs(generator_inputs: Dict[str, Any]) -> None:
    """
    Render generator inputs display.
    
    Args:
        generator_inputs: Dictionary of generator input values
    """
    if generator_inputs:
        st.subheader("Generator Inputs")
        with st.expander("View Generator Inputs", expanded=False):
            st.write("**Input Text:**")
            st.write(generator_inputs.get("input_text", ""))
            
            st.write("**Current Tweet:**")
            current = generator_inputs.get("current_tweet", "")
            st.write(current if current else "(empty for first iteration)")
            
            st.write("**Previous Evaluation:**")
            prev_eval = generator_inputs.get("previous_evaluation", "")
            st.write(prev_eval if prev_eval else "(empty for first iteration)")


def render_evaluator_inputs(evaluator_inputs: Dict[str, Any]) -> None:
    """
    Render evaluator inputs display.
    
    Args:
        evaluator_inputs: Dictionary of evaluator input values
    """
    if evaluator_inputs:
        st.subheader("Evaluator Inputs")
        with st.expander("View Evaluator Inputs", expanded=False):
            st.write("**Original Text:**")
            st.write(evaluator_inputs.get("original_text", ""))
            
            st.write("**Current Best Tweet:**")
            current_best = evaluator_inputs.get("current_best_tweet", "")
            st.write(current_best if current_best else "(empty for first iteration)")
            
            st.write("**Tweet Being Evaluated:**")
            st.write(evaluator_inputs.get("tweet_text", ""))


def render_optimization_stats(iteration_count: int, best_score: float, no_improvement_count: int, patience: int) -> Dict[str, Any]:
    """
    Render optimization statistics.
    
    Args:
        iteration_count: Current iteration number
        best_score: Best score achieved so far
        no_improvement_count: Number of iterations without improvement
        patience: Patience threshold
        
    Returns:
        Dictionary of placeholders for live updates
    """
    st.subheader("Optimization Stats")
    
    st.markdown('<div class="iteration-info">', unsafe_allow_html=True)
    
    iteration_placeholder = st.empty()
    score_placeholder = st.empty()
    no_improvement_placeholder = st.empty()
    
    iteration_placeholder.write(f"**Iteration:** {iteration_count}")
    score_placeholder.write(f"**Best Score:** {best_score:.2f}")
    no_improvement_placeholder.write(f"**No Improvement:** {no_improvement_count}/{patience}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'iteration': iteration_placeholder,
        'score': score_placeholder,
        'no_improvement': no_improvement_placeholder
    }


def render_latest_evaluation(latest_evaluation: EvaluationResult, categories: List[str]) -> None:
    """
    Render the latest evaluation with reasoning.
    
    Args:
        latest_evaluation: The latest evaluation result
        categories: List of category names
    """
    st.subheader("Latest Evaluation")
    
    # Display each category evaluation with reasoning
    if hasattr(latest_evaluation, 'evaluations') and latest_evaluation.evaluations:
        for eval in latest_evaluation.evaluations:
            with st.expander(f"**{eval.category}: {eval.score}/{MAX_SCORE}**", expanded=False):
                st.write(eval.reasoning)
    else:
        # Fallback for old format (backwards compatibility)
        for i, (category, score) in enumerate(zip(categories, latest_evaluation.category_scores)):
            truncated_cat = truncate_category_display(category, CATEGORY_DISPLAY_MAX_LENGTH)
            st.markdown(f'<div class="score-display">{truncated_cat}: {score}/{MAX_SCORE}</div>', unsafe_allow_html=True)


def render_score_history(scores_history: List[EvaluationResult], categories: List[str]) -> None:
    """
    Render detailed score history visualizations.
    
    Args:
        scores_history: List of evaluation results
        categories: List of category names
    """
    st.divider()
    st.subheader("Detailed Score History")
    
    tab1, tab2 = st.tabs(["Average Score", "Category Breakdown"])
    
    with tab1:
        # Average score over iterations
        avg_scores = [sum(score.category_scores)/len(score.category_scores) for score in scores_history]
        
        df_avg = pd.DataFrame({
            'Iteration': list(range(1, len(avg_scores) + 1)),
            'Average Score': avg_scores
        })
        
        st.line_chart(df_avg.set_index('Iteration'), use_container_width=True, height=CHART_HEIGHT)
        
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
        if categories:
            # Build dataframe with all category scores
            data = {'Iteration': list(range(1, len(scores_history) + 1))}
            
            for i, category in enumerate(categories):
                category_name = truncate_category_display(category, CATEGORY_DISPLAY_MAX_LENGTH)
                data[category_name] = [score.category_scores[i] for score in scores_history]
            
            df_categories = pd.DataFrame(data)
            st.line_chart(df_categories.set_index('Iteration'), use_container_width=True, height=CHART_HEIGHT)
            
            # Show improvement per category
            st.subheader("Category Improvements")
            for i, category in enumerate(categories):
                initial_score = scores_history[0].category_scores[i]
                current_score = scores_history[-1].category_scores[i]
                improvement = current_score - initial_score
                
                truncated_cat = truncate_category_display(category, CATEGORY_IMPROVEMENT_MAX_LENGTH)
                color = COLOR_SUCCESS if improvement > 0 else COLOR_FAILURE if improvement < 0 else COLOR_NEUTRAL
                
                st.markdown(
                    f'<div class="category-item">'
                    f'<strong>{truncated_cat}</strong><br>'
                    f'Start: {initial_score}/{MAX_SCORE} → Current: {current_score}/{MAX_SCORE} '
                    f'<span style="color: {color}">({improvement:+.0f})</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
