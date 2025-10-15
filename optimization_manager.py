"""
Optimization management for the DSPy Tweet Optimizer.

This module provides the OptimizationManager class to handle the optimization
loop execution, progress tracking, and UI updates, separating concerns from
the main application logic.
"""

import time
import streamlit as st
from typing import Optional, Any
from hill_climbing import HillClimbingOptimizer
from session_state_manager import SessionStateManager
from constants import ITERATION_SLEEP_TIME


class OptimizationManager:
    """Manages the tweet optimization process and UI updates."""
    
    def __init__(self, optimizer: HillClimbingOptimizer):
        """
        Initialize the optimization manager.
        
        Args:
            optimizer: The HillClimbingOptimizer instance to use
        """
        self.optimizer = optimizer
    
    def run_optimization(
        self,
        input_text: str,
        iterations: int,
        patience: int,
        progress_placeholder: Any,
        status_placeholder: Any
    ) -> None:
        """
        Run the optimization process and update UI in real-time.
        
        Args:
            input_text: The text to optimize
            iterations: Maximum number of iterations
            patience: Patience threshold for early stopping
            progress_placeholder: Streamlit placeholder for progress bar
            status_placeholder: Streamlit placeholder for status text
        """
        early_stop = False
        
        # Run optimization loop
        for iteration, (current_tweet, scores, is_improvement, patience_counter, generator_inputs, evaluator_inputs) in enumerate(
            self.optimizer.optimize(input_text)
        ):
            # Update session state
            SessionStateManager.update(
                iteration_count=iteration + 1,
                no_improvement_count=patience_counter,
                generator_inputs=generator_inputs,
                evaluator_inputs=evaluator_inputs,
                latest_tweet=current_tweet
            )
            
            # Add to history
            st.session_state.scores_history.append(scores)
            
            # Update best tweet if improved
            if is_improvement:
                SessionStateManager.update(
                    current_tweet=current_tweet,
                    best_score=sum(scores.category_scores) / len(scores.category_scores)
                )
            
            # Update live stats if placeholders exist
            if 'stats_placeholders' in st.session_state:
                st.session_state.stats_placeholders['iteration'].write(
                    f"**Iteration:** {st.session_state.iteration_count}"
                )
                st.session_state.stats_placeholders['score'].write(
                    f"**Best Score:** {st.session_state.best_score:.2f}"
                )
                st.session_state.stats_placeholders['no_improvement'].write(
                    f"**No Improvement:** {st.session_state.no_improvement_count}/{patience}"
                )
            
            # Check for early stopping
            if patience_counter >= patience:
                early_stop = True
            
            # Update progress bar and status
            self._update_progress_display(
                iteration=iteration,
                iterations=iterations,
                scores=scores,
                patience_counter=patience_counter,
                patience=patience,
                is_improvement=is_improvement,
                early_stop=early_stop,
                progress_placeholder=progress_placeholder,
                status_placeholder=status_placeholder
            )
            
            # Brief pause for UI updates
            time.sleep(ITERATION_SLEEP_TIME)
            
            # Check if user stopped optimization
            if not st.session_state.optimization_running:
                break
    
    def _update_progress_display(
        self,
        iteration: int,
        iterations: int,
        scores,
        patience_counter: int,
        patience: int,
        is_improvement: bool,
        early_stop: bool,
        progress_placeholder: Any,
        status_placeholder: Any
    ) -> None:
        """
        Update progress bar and status text.
        
        Args:
            iteration: Current iteration number (0-indexed)
            iterations: Total iterations
            scores: Current evaluation scores
            patience_counter: Current patience counter
            patience: Patience threshold
            is_improvement: Whether this iteration improved
            early_stop: Whether stopping early
            progress_placeholder: Streamlit placeholder for progress bar
            status_placeholder: Streamlit placeholder for status text
        """
        # Update progress bar
        progress_placeholder.progress((iteration + 1) / iterations)
        
        # Calculate current score
        current_score = sum(scores.category_scores) / len(scores.category_scores)
        
        # Build status message
        status_msg = (
            f"**Iteration {iteration + 1}/{iterations}** | "
            f"Current: {current_score:.2f} | "
            f"Best: {st.session_state.best_score:.2f} | "
            f"No Improvement: {patience_counter}/{patience}"
        )
        
        # Add status indicators
        if early_stop:
            status_msg += " | ⚠️ Stopping early"
        elif is_improvement:
            status_msg += " | ✓ Improved!"
        
        status_placeholder.markdown(status_msg)
    
    def display_completion_message(
        self,
        status_placeholder: Any
    ) -> None:
        """
        Display completion message after optimization finishes.
        
        Args:
            status_placeholder: Streamlit placeholder for status text
        """
        status_placeholder.markdown(
            f"✓ **Optimization Complete** | "
            f"{st.session_state.iteration_count} iterations | "
            f"Best Score: {st.session_state.best_score:.2f}"
        )
