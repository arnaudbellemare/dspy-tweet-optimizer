"""Integration tests for the optimization flow."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from models import EvaluationResult, CategoryEvaluation
from hill_climbing import optimize_tweet
from dspy_modules import TweetGeneratorModule, TweetEvaluatorModule
import dspy


class TestOptimizationFlow:
    """Integration tests for the complete optimization flow."""
    
    @patch('dspy.OpenAI')
    def test_complete_optimization_flow(self, mock_openai, sample_input_text, sample_categories):
        """Test the complete optimization flow from input to optimized tweet."""
        # Mock DSPy LM responses
        mock_lm = Mock()
        
        # Create mock responses for generator
        def mock_forward(*args, **kwargs):
            result = Mock()
            result.tweet = "Great news! Our innovative product is now live. Check it out today! 🎉"
            return result
        
        mock_lm.return_value = mock_forward
        mock_openai.return_value = mock_lm
        
        # Mock evaluator responses with improving scores
        evaluation_responses = [
            EvaluationResult(evaluations=[
                CategoryEvaluation(category="Clarity", reasoning="Clear message", score=6),
                CategoryEvaluation(category="Engagement", reasoning="Good engagement", score=7),
                CategoryEvaluation(category="Professionalism", reasoning="Professional tone", score=6)
            ]),
            EvaluationResult(evaluations=[
                CategoryEvaluation(category="Clarity", reasoning="Very clear", score=7),
                CategoryEvaluation(category="Engagement", reasoning="Excellent engagement", score=8),
                CategoryEvaluation(category="Professionalism", reasoning="Very professional", score=7)
            ])
        ]
        
        call_count = 0
        
        def mock_evaluate(*args, **kwargs):
            nonlocal call_count
            result = evaluation_responses[min(call_count, len(evaluation_responses) - 1)]
            call_count += 1
            return result
        
        # Configure DSPy
        with patch('dspy.ChainOfThought') as mock_cot:
            # Setup generator mock
            mock_gen = Mock()
            mock_gen.return_value.tweet = "Great news! Our innovative product is now live. Check it out today! 🎉"
            
            # Setup evaluator mock
            mock_eval = Mock()
            mock_eval.side_effect = mock_evaluate
            
            mock_cot.side_effect = [mock_gen, mock_eval]
            
            generator = TweetGeneratorModule()
            evaluator = TweetEvaluatorModule(categories=sample_categories)
            
            # Run optimization
            with patch.object(generator, 'forward', return_value=Mock(tweet="Optimized tweet here!")):
                with patch.object(evaluator, 'forward', side_effect=mock_evaluate):
                    result = optimize_tweet(
                        input_text=sample_input_text,
                        categories=sample_categories,
                        generator=generator,
                        evaluator=evaluator,
                        max_iterations=3,
                        patience=2
                    )
        
        # Verify results
        assert result is not None
        assert 'best_tweet' in result
        assert 'best_evaluation' in result
        assert 'iteration_count' in result
        assert result['iteration_count'] > 0
    
    def test_hill_climbing_with_no_improvement(self, sample_input_text, sample_categories):
        """Test that optimization stops when patience is exhausted."""
        # Create mock generator
        generator = Mock(spec=TweetGeneratorModule)
        generator.forward.return_value = Mock(tweet="Same tweet every time")
        
        # Create mock evaluator that returns same score
        evaluator = Mock(spec=TweetEvaluatorModule)
        same_evaluation = EvaluationResult(evaluations=[
            CategoryEvaluation(category=cat, reasoning="Same", score=5)
            for cat in sample_categories
        ])
        evaluator.forward.return_value = same_evaluation
        
        # Run optimization with low patience
        result = optimize_tweet(
            input_text=sample_input_text,
            categories=sample_categories,
            generator=generator,
            evaluator=evaluator,
            max_iterations=10,
            patience=2
        )
        
        # Should stop after patience + 1 iterations (initial + patience attempts)
        assert result['iteration_count'] <= 3
        assert result['best_evaluation'].total_score == 15  # 3 categories * 5 score
    
    def test_optimization_with_improving_scores(self, sample_input_text, sample_categories):
        """Test optimization with progressively improving scores."""
        generator = Mock(spec=TweetGeneratorModule)
        generator.forward.return_value = Mock(tweet="Improving tweet")
        
        evaluator = Mock(spec=TweetEvaluatorModule)
        
        # Create evaluations with improving scores
        scores = [5, 6, 7, 8, 7, 6]  # Improve then decline
        evaluation_sequence = []
        
        for score in scores:
            evaluation_sequence.append(
                EvaluationResult(evaluations=[
                    CategoryEvaluation(category=cat, reasoning=f"Score {score}", score=score)
                    for cat in sample_categories
                ])
            )
        
        evaluator.forward.side_effect = evaluation_sequence
        
        # Run optimization
        result = optimize_tweet(
            input_text=sample_input_text,
            categories=sample_categories,
            generator=generator,
            evaluator=evaluator,
            max_iterations=10,
            patience=3
        )
        
        # Best score should be from the peak (score=8)
        assert result['best_evaluation'].average_score == 8.0
        # Should have stopped after patience iterations of no improvement
        assert result['iteration_count'] <= 7  # 4 improvements + 3 patience
    
    def test_max_iterations_limit(self, sample_input_text, sample_categories):
        """Test that optimization respects max iterations limit."""
        generator = Mock(spec=TweetGeneratorModule)
        generator.forward.return_value = Mock(tweet="Test tweet")
        
        evaluator = Mock(spec=TweetEvaluatorModule)
        
        # Always return improving scores to test max iterations
        def improving_eval(*args, **kwargs):
            import random
            score = random.randint(5, 9)
            return EvaluationResult(evaluations=[
                CategoryEvaluation(category=cat, reasoning=f"Score {score}", score=score)
                for cat in sample_categories
            ])
        
        evaluator.forward.side_effect = improving_eval
        
        max_iter = 5
        result = optimize_tweet(
            input_text=sample_input_text,
            categories=sample_categories,
            generator=generator,
            evaluator=evaluator,
            max_iterations=max_iter,
            patience=10  # High patience, should hit max iterations first
        )
        
        # Should stop at max iterations
        assert result['iteration_count'] <= max_iter + 1
