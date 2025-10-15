from typing import List, Iterator, Tuple
import dspy
from models import EvaluationResult
from dspy_modules import TweetGeneratorModule, TweetEvaluatorModule

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
    
    def optimize(self, initial_text: str) -> Iterator[Tuple[str, EvaluationResult, bool, int, dict]]:
        """
        Optimize tweet using hill climbing algorithm.
        
        Yields:
            Tuple of (current_tweet, evaluation_result, is_improvement, patience_counter, generator_inputs)
        """
        # Generate initial tweet
        generator_inputs = {
            "input_text": initial_text,
            "current_tweet": "",
            "feedback": ""
        }
        current_tweet = self.generator(initial_text)
        current_score = self.evaluator(current_tweet, self.categories)
        
        best_tweet = current_tweet
        best_score = current_score
        patience_counter = 0
        
        yield (current_tweet, current_score, True, patience_counter, generator_inputs)
        
        for iteration in range(1, self.max_iterations):
            # Generate feedback for improvement
            feedback = self._generate_feedback(best_tweet, best_score)
            
            # Generate improved tweet
            try:
                generator_inputs = {
                    "input_text": initial_text,
                    "current_tweet": best_tweet,
                    "feedback": feedback
                }
                
                candidate_tweet = self.generator(
                    input_text=initial_text,
                    current_tweet=best_tweet,
                    feedback=feedback
                )
                
                # Evaluate candidate
                candidate_score = self.evaluator(candidate_tweet, self.categories)
                
                # Check if candidate is better (hill climbing condition)
                is_improvement = candidate_score > best_score
                
                if is_improvement:
                    best_tweet = candidate_tweet
                    best_score = candidate_score
                    patience_counter = 0
                    yield (candidate_tweet, candidate_score, True, patience_counter, generator_inputs)
                else:
                    patience_counter += 1
                    yield (best_tweet, candidate_score, False, patience_counter, generator_inputs)
                
                # Early stopping if no improvement for 'patience' iterations
                if patience_counter >= self.patience:
                    break
                    
            except Exception as e:
                # If generation fails, yield current best
                patience_counter += 1
                yield (best_tweet, best_score, False, patience_counter, generator_inputs)
                
                if patience_counter >= self.patience:
                    break
    
    def _generate_feedback(self, current_tweet: str, current_score: EvaluationResult) -> str:
        """Generate feedback for tweet improvement based on current scores."""
        weak_categories = []
        
        for i, (category, score) in enumerate(zip(self.categories, current_score.category_scores)):
            if score < 7:  # Consider scores below 7 as needing improvement
                weak_categories.append(f"{category} (current score: {score}/9)")
        
        if weak_categories:
            feedback = f"Focus on improving these areas: {'; '.join(weak_categories)}. "
            feedback += "Make the tweet more engaging, concise, and impactful while staying within 280 characters."
        else:
            feedback = "The tweet is performing well across all categories. Try to make minor refinements for even better performance."
        
        return feedback
