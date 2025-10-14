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
    """Evaluate a tweet across multiple custom categories."""
    
    tweet_text: str = dspy.InputField(desc="Tweet text to evaluate")
    categories: List[str] = dspy.InputField(desc="List of evaluation category descriptions")
    evaluation: EvaluationResult = dspy.OutputField(desc="Structured evaluation with scores for each category")

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
        self.evaluate = dspy.TypedPredictor(TweetEvaluator)
    
    def forward(self, tweet_text: str, categories: List[str]) -> EvaluationResult:
        """Evaluate a tweet across specified categories."""
        try:
            result = self.evaluate(
                tweet_text=tweet_text,
                categories=categories
            )
            
            # Validate scores are within 1-9 range
            validated_scores = []
            for score in result.evaluation.category_scores:
                validated_score = max(1, min(9, int(score)))
                validated_scores.append(validated_score)
            
            # Create validated result
            validated_result = EvaluationResult(category_scores=validated_scores)
            
            return validated_result
        except Exception as e:
            raise Exception(f"Tweet evaluation failed: {str(e)}")
