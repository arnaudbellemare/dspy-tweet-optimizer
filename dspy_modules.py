import dspy
from typing import List, Optional
from models import EvaluationResult, CategoryEvaluation
from constants import (
    TWEET_MAX_LENGTH,
    TWEET_TRUNCATION_SUFFIX,
    TWEET_TRUNCATION_LENGTH,
    DEFAULT_SCORE,
    ERROR_PARSING,
    ERROR_VALIDATION,
    ERROR_GENERATION,
    ERROR_EVALUATION,
    MIN_SCORE,
    MAX_SCORE
)
from helpers import format_evaluation_for_generator, truncate_tweet

class TweetGenerator(dspy.Signature):
    """Generate or improve a tweet based on input text and detailed evaluation feedback with reasoning."""
    
    input_text: str = dspy.InputField(desc="Original text or current tweet to improve")
    current_tweet: str = dspy.InputField(desc="Current best tweet version (empty for first generation)")
    previous_evaluation: str = dspy.InputField(desc="Previous evaluation with category-by-category reasoning and scores (empty for first generation)")
    improved_tweet: str = dspy.OutputField(desc=f"Generated or improved tweet text (max {TWEET_MAX_LENGTH} characters)")

class TweetEvaluator(dspy.Signature):
    """Evaluate a tweet across multiple custom categories. For each category, provide detailed reasoning explaining the score, then assign a score. Ensure the tweet maintains the same meaning as the original text."""
    
    original_text: str = dspy.InputField(desc="Original input text that started the optimization")
    current_best_tweet: str = dspy.InputField(desc="Current best tweet version for comparison (empty for first evaluation)")
    tweet_text: str = dspy.InputField(desc="Tweet text to evaluate")
    categories: str = dspy.InputField(desc="Comma-separated list of evaluation category descriptions")
    evaluations: List[CategoryEvaluation] = dspy.OutputField(
        desc=f"List of evaluations with category name, detailed reasoning, and score ({MIN_SCORE}-{MAX_SCORE}) for each category. Ensure the tweet conveys the same meaning as the original text."
    )

class TweetGeneratorModule(dspy.Module):
    """DSPy module for generating and improving tweets."""
    
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(TweetGenerator)
    
    def forward(self, input_text: str, current_tweet: str = "", previous_evaluation: Optional[EvaluationResult] = None) -> str:
        """Generate or improve a tweet."""
        try:
            # Format previous evaluation as text
            eval_text = format_evaluation_for_generator(previous_evaluation)
            
            result = self.generate(
                input_text=input_text,
                current_tweet=current_tweet,
                previous_evaluation=eval_text
            )
            
            # Ensure tweet doesn't exceed character limit
            tweet = truncate_tweet(result.improved_tweet, TWEET_MAX_LENGTH, TWEET_TRUNCATION_SUFFIX)
            
            return tweet
        except Exception as e:
            raise Exception(f"{ERROR_GENERATION}: {str(e)}")

class TweetEvaluatorModule(dspy.Module):
    """DSPy module for evaluating tweets across custom categories."""
    
    def __init__(self):
        super().__init__()
        self.evaluate = dspy.ChainOfThought(TweetEvaluator)
    
    def forward(self, tweet_text: str, categories: List[str], original_text: str = "", current_best_tweet: str = "") -> EvaluationResult:
        """Evaluate a tweet across specified categories."""
        try:
            # Join categories into comma-separated string
            categories_str = ", ".join(categories)
            
            result = self.evaluate(
                original_text=original_text,
                current_best_tweet=current_best_tweet,
                tweet_text=tweet_text,
                categories=categories_str
            )
            
            # Extract and validate evaluations
            evaluations = result.evaluations
            
            # Ensure we have the right number of evaluations
            if len(evaluations) != len(categories):
                # Create default evaluations if mismatch
                evaluations = [
                    CategoryEvaluation(
                        category=cat,
                        reasoning=ERROR_PARSING,
                        score=DEFAULT_SCORE
                    ) for cat in categories
                ]
            else:
                # Validate each evaluation
                validated_evals = []
                for i, eval in enumerate(evaluations):
                    try:
                        # Ensure score is valid
                        score = max(MIN_SCORE, min(MAX_SCORE, int(eval.score)))
                        validated_evals.append(CategoryEvaluation(
                            category=categories[i] if i < len(categories) else eval.category,
                            reasoning=eval.reasoning if eval.reasoning else "No reasoning provided",
                            score=score
                        ))
                    except (ValueError, TypeError, AttributeError):
                        validated_evals.append(CategoryEvaluation(
                            category=categories[i] if i < len(categories) else "Unknown",
                            reasoning=ERROR_VALIDATION,
                            score=DEFAULT_SCORE
                        ))
                evaluations = validated_evals
            
            # Create validated result
            validated_result = EvaluationResult(evaluations=evaluations)
            
            return validated_result
        except Exception as e:
            # Return default evaluations on error
            default_evals = [
                CategoryEvaluation(
                    category=cat,
                    reasoning=f"{ERROR_EVALUATION}: {str(e)}",
                    score=DEFAULT_SCORE
                ) for cat in categories
            ]
            return EvaluationResult(evaluations=default_evals)
