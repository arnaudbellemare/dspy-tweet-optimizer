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
        mock_result.tweet = "This is a generated tweet!"
        mock_predictor.return_value = mock_result
        mock_cot.return_value = mock_predictor
        
        # Create generator and call forward
        generator = TweetGeneratorModule()
        result = generator.forward(
            input_text="Test input",
            current_best="",
            evaluation_feedback=""
        )
        
        # Verify result
        assert hasattr(result, 'tweet')
        assert isinstance(result.tweet, str)
    
    @patch('dspy.ChainOfThought')
    def test_generator_with_feedback(self, mock_cot):
        """Test generator with evaluation feedback."""
        mock_predictor = Mock()
        mock_result = Mock()
        mock_result.tweet = "Improved tweet based on feedback"
        mock_predictor.return_value = mock_result
        mock_cot.return_value = mock_predictor
        
        generator = TweetGeneratorModule()
        
        feedback = "Previous tweet lacked clarity. Be more specific."
        current_best = "Old tweet"
        
        result = generator.forward(
            input_text="Launch announcement",
            current_best=current_best,
            evaluation_feedback=feedback
        )
        
        # Verify the predictor was called with feedback
        mock_predictor.assert_called_once()
        call_kwargs = mock_predictor.call_args[1]
        assert 'evaluation_feedback' in call_kwargs
        assert call_kwargs['evaluation_feedback'] == feedback


class TestTweetEvaluatorModule:
    """Integration tests for TweetEvaluatorModule."""
    
    @patch('dspy.ChainOfThought')
    def test_evaluator_initialization(self, mock_cot):
        """Test that evaluator module initializes with categories."""
        categories = ["Clarity", "Engagement"]
        evaluator = TweetEvaluatorModule(categories=categories)
        
        # Verify ChainOfThought was called
        mock_cot.assert_called_once()
        
        # Verify categories are stored
        assert evaluator.categories == categories
    
    @patch('dspy.ChainOfThought')
    def test_evaluator_forward_returns_evaluation(self, mock_cot, sample_categories):
        """Test that evaluator forward method returns proper evaluation."""
        # Setup mock to return proper evaluation structure
        mock_predictor = Mock()
        mock_result = EvaluationResult(evaluations=[
            CategoryEvaluation(
                category=cat,
                reasoning=f"Good {cat.lower()}",
                score=7
            ) for cat in sample_categories
        ])
        mock_predictor.return_value = mock_result
        mock_cot.return_value = mock_predictor
        
        evaluator = TweetEvaluatorModule(categories=sample_categories)
        result = evaluator.forward(
            original_input="Test input",
            tweet="Test tweet"
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
        mock_result = EvaluationResult(evaluations=[
            CategoryEvaluation(category=cat, reasoning="Test", score=5)
            for cat in categories
        ])
        mock_predictor.return_value = mock_result
        mock_cot.return_value = mock_predictor
        
        evaluator = TweetEvaluatorModule(categories=categories)
        result = evaluator.forward(
            original_input="Input",
            tweet="Tweet"
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
        mock_gen_result.tweet = "Generated tweet for testing"
        mock_gen.return_value = mock_gen_result
        
        mock_eval = Mock()
        mock_eval_result = EvaluationResult(evaluations=[
            CategoryEvaluation(category="Clarity", reasoning="Clear", score=8),
            CategoryEvaluation(category="Impact", reasoning="Impactful", score=7)
        ])
        mock_eval.return_value = mock_eval_result
        
        # Return different mocks for generator and evaluator
        mock_cot.side_effect = [mock_gen, mock_eval]
        
        # Create modules
        generator = TweetGeneratorModule()
        evaluator = TweetEvaluatorModule(categories=categories)
        
        # Generate tweet
        gen_result = generator.forward(
            input_text="Product launch",
            current_best="",
            evaluation_feedback=""
        )
        
        # Evaluate generated tweet
        eval_result = evaluator.forward(
            original_input="Product launch",
            tweet=gen_result.tweet
        )
        
        # Verify pipeline works
        assert gen_result.tweet == "Generated tweet for testing"
        assert isinstance(eval_result, EvaluationResult)
        assert eval_result.total_score == 15
        assert eval_result.average_score == 7.5
    
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
        mock_gen.side_effect = [Mock(tweet=t) for t in gen_tweets]
        
        # Setup evaluator to give improving scores
        eval_scores = [
            EvaluationResult(evaluations=[
                CategoryEvaluation(category="Quality", reasoning="OK", score=5)
            ]),
            EvaluationResult(evaluations=[
                CategoryEvaluation(category="Quality", reasoning="Better", score=7)
            ])
        ]
        mock_eval = Mock()
        mock_eval.side_effect = eval_scores
        
        mock_cot.side_effect = [mock_gen, mock_eval]
        
        generator = TweetGeneratorModule()
        evaluator = TweetEvaluatorModule(categories=categories)
        
        # First iteration
        tweet1 = generator.forward(
            input_text="Test",
            current_best="",
            evaluation_feedback=""
        )
        eval1 = evaluator.forward(
            original_input="Test",
            tweet=tweet1.tweet
        )
        
        # Create feedback from first evaluation
        feedback = f"{eval1.evaluations[0].category}: {eval1.evaluations[0].reasoning} (score: {eval1.evaluations[0].score})"
        
        # Second iteration with feedback
        tweet2 = generator.forward(
            input_text="Test",
            current_best=tweet1.tweet,
            evaluation_feedback=feedback
        )
        
        # Verify improvement cycle
        assert tweet1.tweet == "First attempt"
        assert eval1.total_score == 5
        
        # Generator should have been called with feedback on second iteration
        second_call_kwargs = mock_gen.call_args_list[1][1] if len(mock_gen.call_args_list) > 1 else mock_gen.call_args[1]
        assert 'evaluation_feedback' in second_call_kwargs
        assert feedback in second_call_kwargs['evaluation_feedback']
