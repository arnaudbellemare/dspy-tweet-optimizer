import dspy
from typing import List
from models import EvaluationResult

class TweetGenerator(dspy.Signature):
    """Generate or improve a tweet based on input text and feedback."""
    
    input_text: str = dspy.InputField(desc="Original text or current tweet to improve")
    current_tweet: str = dspy.InputField(desc="Current best tweet version (empty for first generation)")
    feedback: str = dspy.InputField(desc="Feedback on what to improve (empty for first generation)")
    improved_tweet: str = dspy.OutputField(desc="Generated or improved tweet text (max 280 characters)")

class TweetEvaluator(dspy.Signature):
    """Evaluate a tweet across multiple custom categories. Ensure the tweet maintains the same meaning as the original text. Return scores from 1-9 for each category."""
    
    original_text: str = dspy.InputField(desc="Original input text that started the optimization")
    current_best_tweet: str = dspy.InputField(desc="Current best tweet version for comparison (empty for first evaluation)")
    tweet_text: str = dspy.InputField(desc="Tweet text to evaluate")
    categories: str = dspy.InputField(desc="Comma-separated list of evaluation category descriptions")
    category_scores: List[int] = dspy.OutputField(desc="List of integer scores (1-9) for each category in order. Ensure the tweet conveys the same meaning as the original text.")

class TweetGeneratorModule(dspy.Module):
    """DSPy module for generating and improving tweets."""
    
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(TweetGenerator)
    
    def forward(self, input_text: str, current_tweet: str = "", feedback: str = "") -> str:
        """Generate or improve a tweet."""
        try:
            result = self.generate(
                input_text=input_text,
                current_tweet=current_tweet,
                feedback=feedback
            )
            
            # Ensure tweet doesn't exceed 280 characters
            tweet = result.improved_tweet.strip()
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            return tweet
        except Exception as e:
            raise Exception(f"Tweet generation failed: {str(e)}")

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
            
            # Extract and validate scores
            scores = result.category_scores
            
            # Ensure we have the right number of scores
            if len(scores) != len(categories):
                # If mismatch, use default scores
                scores = [5] * len(categories)
            
            # Validate scores are within 1-9 range
            validated_scores = []
            for score in scores:
                try:
                    validated_score = max(1, min(9, int(score)))
                    validated_scores.append(validated_score)
                except (ValueError, TypeError):
                    validated_scores.append(5)  # Default to 5 if invalid
            
            # Create validated result
            validated_result = EvaluationResult(category_scores=validated_scores)
            
            return validated_result
        except Exception as e:
            # Return default scores on error
            return EvaluationResult(category_scores=[5] * len(categories))
