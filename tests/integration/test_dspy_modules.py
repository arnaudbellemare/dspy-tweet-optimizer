"""Integration tests for DSPy modules."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from dspy_modules import TweetGeneratorModule, TweetEvaluatorModule
from models import EvaluationResult, CategoryEvaluation
import dspy


class TestTweetGeneratorModule:
    """Integration tests for TweetGeneratorModule."""
    
    @patch('dspy.ChainOfThought')
    def test_generator_initialization(self, mock_cot):
        """Test that generator module initializes correctly."""
        generator = TweetGeneratorModule()
        
        # Verify ChainOfThought was called with correct signature
        mock_cot.assert_called_once()
        call_args = mock_cot.call_args
        assert 'TweetGenerator' in str(call_args)
    
    @patch('dspy.ChainOfThought')
    def test_generator_forward_returns_tweet(self, mock_cot):
        """Test that generator forward method returns a tweet."""
        # Setup mock
        mock_predictor = Mock()
        mock_result = Mock()
        mock_result.improved_tweet = "This is a generated tweet!"
        mock_predictor.return_value = mock_result
        mock_cot.return_value = mock_predictor
        
        # Create generator and call forward
        generator = TweetGeneratorModule()
        result = generator.forward(
            input_text="Test input",
            current_tweet="",
            previous_evaluation=None
        )
        
        # Verify result is a string
        assert isinstance(result, str)
        assert len(result) > 0
    
    @patch('dspy.ChainOfThought')
    def test_generator_with_feedback(self, mock_cot):
        """Test generator with evaluation feedback."""
        mock_predictor = Mock()
        mock_result = Mock()
        mock_result.improved_tweet = "Improved tweet based on feedback"
        mock_predictor.return_value = mock_result
        mock_cot.return_value = mock_predictor
        
        generator = TweetGeneratorModule()
        
        # Create previous evaluation
        from models import CategoryEvaluation, EvaluationResult
        prev_eval = EvaluationResult(evaluations=[
            CategoryEvaluation(category="Clarity", reasoning="Lacks clarity", score=5)
        ])
        current_tweet = "Old tweet"
        
        result = generator.forward(
            input_text="Launch announcement",
            current_tweet=current_tweet,
            previous_evaluation=prev_eval
        )
        
        # Verify the predictor was called
        mock_predictor.assert_called_once()
        assert isinstance(result, str)


class TestTweetEvaluatorModule:
    """Integration tests for TweetEvaluatorModule."""
    
    @patch('dspy.ChainOfThought')
    def test_evaluator_initialization(self, mock_cot):
        """Test that evaluator module initializes correctly."""
        evaluator = TweetEvaluatorModule()
        
        # Verify ChainOfThought was called
        mock_cot.assert_called_once()
    
    @patch('dspy.ChainOfThought')
    def test_evaluator_forward_returns_evaluation(self, mock_cot, sample_categories):
        """Test that evaluator forward method returns proper evaluation."""
        # Setup mock to return proper evaluation structure
        mock_predictor = Mock()
        mock_result = Mock()
        mock_result.evaluations = [
            CategoryEvaluation(
                category=cat,
                reasoning=f"Good {cat.lower()}",
                score=7
            ) for cat in sample_categories
        ]
        mock_predictor.return_value = mock_result
        mock_cot.return_value = mock_predictor
        
        evaluator = TweetEvaluatorModule()
        result = evaluator.forward(
            original_text="Test input",
            tweet_text="Test tweet",
            categories=sample_categories
        )
        
        # Verify result is EvaluationResult
        assert isinstance(result, EvaluationResult)
        assert len(result.evaluations) == len(sample_categories)
        assert all(isinstance(e, CategoryEvaluation) for e in result.evaluations)
    
    @patch('dspy.ChainOfThought')
    def test_evaluator_scores_all_categories(self, mock_cot):
        """Test that evaluator scores all provided categories."""
        categories = ["Cat1", "Cat2", "Cat3", "Cat4"]
        
        mock_predictor = Mock()
        mock_result = Mock()
        mock_result.evaluations = [
            CategoryEvaluation(category=cat, reasoning="Test", score=5)
            for cat in categories
        ]
        mock_predictor.return_value = mock_result
        mock_cot.return_value = mock_predictor
        
        evaluator = TweetEvaluatorModule()
        result = evaluator.forward(
            original_text="Input",
            tweet_text="Tweet",
            categories=categories
        )
        
        # Verify all categories are evaluated
        evaluated_categories = [e.category for e in result.evaluations]
        assert set(evaluated_categories) == set(categories)


class TestModuleIntegration:
    """Integration tests for generator and evaluator working together."""
    
    @patch('dspy.ChainOfThought')
    def test_generator_evaluator_pipeline(self, mock_cot):
        """Test complete pipeline of generation and evaluation."""
        categories = ["Clarity", "Impact"]
        
        # Setup mocks
        mock_gen = Mock()
        mock_gen_result = Mock()
        mock_gen_result.improved_tweet = "Generated tweet for testing"
        mock_gen.return_value = mock_gen_result
        
        mock_eval = Mock()
        mock_eval_result = Mock()
        mock_eval_result.evaluations = [
            CategoryEvaluation(category="Clarity", reasoning="Clear", score=8),
            CategoryEvaluation(category="Impact", reasoning="Impactful", score=7)
        ]
        mock_eval.return_value = mock_eval_result
        
        # Return different mocks for generator and evaluator
        mock_cot.side_effect = [mock_gen, mock_eval]
        
        # Create modules
        generator = TweetGeneratorModule()
        evaluator = TweetEvaluatorModule()
        
        # Generate tweet
        gen_result = generator.forward(
            input_text="Product launch",
            current_tweet="",
            previous_evaluation=None
        )
        
        # Evaluate generated tweet
        eval_result = evaluator.forward(
            original_text="Product launch",
            tweet_text=gen_result,
            categories=categories
        )
        
        # Verify pipeline works
        assert gen_result == "Generated tweet for testing"
        assert isinstance(eval_result, EvaluationResult)
        assert eval_result.total_score() == 15
        assert eval_result.average_score() == 7.5
    
    @patch('dspy.ChainOfThought')
    def test_iterative_improvement_cycle(self, mock_cot):
        """Test iterative improvement with feedback loop."""
        categories = ["Quality"]
        
        # Setup generator to improve based on feedback
        gen_tweets = [
            "First attempt",
            "Improved attempt based on feedback"
        ]
        mock_gen = Mock()
        mock_gen.side_effect = [Mock(improved_tweet=t) for t in gen_tweets]
        
        # Setup evaluator to give improving scores
        eval_results = [
            Mock(evaluations=[
                CategoryEvaluation(category="Quality", reasoning="OK", score=5)
            ]),
            Mock(evaluations=[
                CategoryEvaluation(category="Quality", reasoning="Better", score=7)
            ])
        ]
        mock_eval = Mock()
        mock_eval.side_effect = eval_results
        
        mock_cot.side_effect = [mock_gen, mock_eval]
        
        generator = TweetGeneratorModule()
        evaluator = TweetEvaluatorModule()
        
        # First iteration
        tweet1 = generator.forward(
            input_text="Test",
            current_tweet="",
            previous_evaluation=None
        )
        eval1 = evaluator.forward(
            original_text="Test",
            tweet_text=tweet1,
            categories=categories
        )
        
        # Create feedback from first evaluation (as EvaluationResult)
        feedback_eval = EvaluationResult(evaluations=eval1.evaluations)
        
        # Second iteration with feedback
        tweet2 = generator.forward(
            input_text="Test",
            current_tweet=tweet1,
            previous_evaluation=feedback_eval
        )
        
        # Verify improvement cycle
        assert tweet1 == "First attempt"
        assert eval1.total_score() == 5
