from typing import List, Iterator, Tuple, Dict
import dspy
from models import EvaluationResult
from dspy_modules import TweetGeneratorModule, TweetEvaluatorModule
from helpers import format_evaluation_for_generator

class HillClimbingOptimizer:
    """Hill climbing optimizer for tweet improvement."""
    
    def __init__(
        self,
        generator: TweetGeneratorModule,
        evaluator: TweetEvaluatorModule,
        categories: List[str],
        max_iterations: int = 10,
        patience: int = 5
    ):
        self.generator = generator
        self.evaluator = evaluator
        self.categories = categories
        self.max_iterations = max_iterations
        self.patience = patience
    
    def optimize(self, initial_text: str) -> Iterator[Tuple[str, EvaluationResult, bool, int, Dict[str, str], Dict[str, str]]]:
        """
        Optimize tweet using hill climbing algorithm.
        
        Yields:
            Tuple of (current_tweet, evaluation_result, is_improvement, patience_counter, generator_inputs, evaluator_inputs)
        """
        # Generate initial tweet
        generator_inputs = {
            "input_text": initial_text,
            "current_tweet": "",
            "previous_evaluation": ""
        }
        current_tweet = self.generator(
            input_text=initial_text,
            current_tweet="",
            previous_evaluation=None
        )
        
        evaluator_inputs = {
            "original_text": initial_text,
            "current_best_tweet": "",
            "tweet_text": current_tweet
        }
        current_score = self.evaluator(
            tweet_text=current_tweet,
            categories=self.categories,
            original_text=initial_text,
            current_best_tweet=""
        )
        
        best_tweet = current_tweet
        best_score = current_score
        patience_counter = 0
        
        yield (current_tweet, current_score, True, patience_counter, generator_inputs, evaluator_inputs)
        
        for iteration in range(1, self.max_iterations):
            # Generate improved tweet with previous evaluation as feedback
            try:
                # Format evaluation for display in generator inputs
                eval_text = format_evaluation_for_generator(best_score)
                
                generator_inputs = {
                    "input_text": initial_text,
                    "current_tweet": best_tweet,
                    "previous_evaluation": eval_text
                }
                
                candidate_tweet = self.generator(
                    input_text=initial_text,
                    current_tweet=best_tweet,
                    previous_evaluation=best_score
                )
                
                # Evaluate candidate
                evaluator_inputs = {
                    "original_text": initial_text,
                    "current_best_tweet": best_tweet,
                    "tweet_text": candidate_tweet
                }
                candidate_score = self.evaluator(
                    tweet_text=candidate_tweet,
                    categories=self.categories,
                    original_text=initial_text,
                    current_best_tweet=best_tweet
                )
                
                # Check if candidate is better (hill climbing condition)
                is_improvement = candidate_score > best_score
                
                if is_improvement:
                    best_tweet = candidate_tweet
                    best_score = candidate_score
                    patience_counter = 0
                    yield (candidate_tweet, candidate_score, True, patience_counter, generator_inputs, evaluator_inputs)
                else:
                    patience_counter += 1
                    yield (best_tweet, candidate_score, False, patience_counter, generator_inputs, evaluator_inputs)
                
                # Early stopping if no improvement for 'patience' iterations
                if patience_counter >= self.patience:
                    break
                    
            except Exception as e:
                # If generation fails, yield current best
                patience_counter += 1
                evaluator_inputs = {
                    "original_text": initial_text,
                    "current_best_tweet": best_tweet,
                    "tweet_text": best_tweet
                }
                yield (best_tweet, best_score, False, patience_counter, generator_inputs, evaluator_inputs)
                
                if patience_counter >= self.patience:
                    break
    
