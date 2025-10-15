import dspy
from typing import List, Optional
from models import EvaluationResult, CategoryEvaluation

class TweetGenerator(dspy.Signature):
    """Generate or improve a tweet based on input text and detailed evaluation feedback with reasoning."""
    
    input_text: str = dspy.InputField(desc="Original text or current tweet to improve")
    current_tweet: str = dspy.InputField(desc="Current best tweet version (empty for first generation)")
    previous_evaluation: str = dspy.InputField(desc="Previous evaluation with category-by-category reasoning and scores (empty for first generation)")
    improved_tweet: str = dspy.OutputField(desc="Generated or improved tweet text (max 280 characters)")

class TweetEvaluator(dspy.Signature):
    """Evaluate a tweet across multiple custom categories. For each category, provide detailed reasoning explaining the score, then assign a score from 1-9. Ensure the tweet maintains the same meaning as the original text."""
    
    original_text: str = dspy.InputField(desc="Original input text that started the optimization")
    current_best_tweet: str = dspy.InputField(desc="Current best tweet version for comparison (empty for first evaluation)")
    tweet_text: str = dspy.InputField(desc="Tweet text to evaluate")
    categories: str = dspy.InputField(desc="Comma-separated list of evaluation category descriptions")
    evaluations: List[CategoryEvaluation] = dspy.OutputField(desc="List of evaluations with category name, detailed reasoning, and score (1-9) for each category. Ensure the tweet conveys the same meaning as the original text.")

class TweetGeneratorModule(dspy.Module):
    """DSPy module for generating and improving tweets."""
    
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(TweetGenerator)
    
    def forward(self, input_text: str, current_tweet: str = "", previous_evaluation: Optional[EvaluationResult] = None) -> str:
        """Generate or improve a tweet."""
        try:
            # Format previous evaluation as text
            eval_text = ""
            if previous_evaluation and previous_evaluation.evaluations:
                eval_lines = []
                for eval in previous_evaluation.evaluations:
                    eval_lines.append(f"{eval.category} (Score: {eval.score}/9): {eval.reasoning}")
                eval_text = "\n".join(eval_lines)
            
            result = self.generate(
                input_text=input_text,
                current_tweet=current_tweet,
                previous_evaluation=eval_text
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
            
            # Extract and validate evaluations
            evaluations = result.evaluations
            
            # Ensure we have the right number of evaluations
            if len(evaluations) != len(categories):
                # Create default evaluations if mismatch
                evaluations = [
                    CategoryEvaluation(
                        category=cat,
                        reasoning="Default evaluation due to parsing error",
                        score=5
                    ) for cat in categories
                ]
            else:
                # Validate each evaluation
                validated_evals = []
                for i, eval in enumerate(evaluations):
                    try:
                        # Ensure score is valid
                        score = max(1, min(9, int(eval.score)))
                        validated_evals.append(CategoryEvaluation(
                            category=categories[i] if i < len(categories) else eval.category,
                            reasoning=eval.reasoning if eval.reasoning else "No reasoning provided",
                            score=score
                        ))
                    except (ValueError, TypeError, AttributeError):
                        validated_evals.append(CategoryEvaluation(
                            category=categories[i] if i < len(categories) else "Unknown",
                            reasoning="Default evaluation due to validation error",
                            score=5
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
                    reasoning=f"Default evaluation due to error: {str(e)}",
                    score=5
                ) for cat in categories
            ]
            return EvaluationResult(evaluations=default_evals)
