"""Integration tests for the optimization flow."""

import pytest
from unittest.mock import Mock, patch
from models import EvaluationResult, CategoryEvaluation
from hill_climbing import HillClimbingOptimizer
from dspy_modules import TweetGeneratorModule, TweetEvaluatorModule


class TestOptimizationFlow:
    """Integration tests for the complete optimization flow."""
    
    def test_hill_climbing_basic_flow(self, sample_input_text, sample_categories):
        """Test basic hill climbing optimization flow."""
        # Create mock generator
        generator = Mock(spec=TweetGeneratorModule)
        generator.return_value = "Generated optimized tweet"
        
        # Create mock evaluator
        evaluator = Mock(spec=TweetEvaluatorModule)
        evaluator.return_value = EvaluationResult(evaluations=[
            CategoryEvaluation(category=cat, reasoning="Good", score=7)
            for cat in sample_categories
        ])
        
        # Create optimizer
        optimizer = HillClimbingOptimizer(
            generator=generator,
            evaluator=evaluator,
            categories=sample_categories,
            max_iterations=3,
            patience=2
        )
        
        # Run optimization and collect results
        results = list(optimizer.optimize(sample_input_text))
        
        # Verify we got results
        assert len(results) > 0
        
        # Each result should be a tuple with expected elements
        for result in results:
            tweet, evaluation, is_improvement, patience_count, gen_inputs, eval_inputs = result
            assert isinstance(tweet, str)
            assert isinstance(evaluation, EvaluationResult)
            assert isinstance(is_improvement, bool)
            assert isinstance(patience_count, int)
            assert isinstance(gen_inputs, dict)
            assert isinstance(eval_inputs, dict)
    
    def test_hill_climbing_with_no_improvement(self, sample_input_text, sample_categories):
        """Test that optimization stops when patience is exhausted."""
        # Create mock generator
        generator = Mock(spec=TweetGeneratorModule)
        generator.return_value = "Same tweet every time"
        
        # Create mock evaluator that returns same score
        evaluator = Mock(spec=TweetEvaluatorModule)
        same_evaluation = EvaluationResult(evaluations=[
            CategoryEvaluation(category=cat, reasoning="Same", score=5)
            for cat in sample_categories
        ])
        evaluator.return_value = same_evaluation
        
        # Run optimization with low patience
        optimizer = HillClimbingOptimizer(
            generator=generator,
            evaluator=evaluator,
            categories=sample_categories,
            max_iterations=10,
            patience=2
        )
        
        results = list(optimizer.optimize(sample_input_text))
        
        # Should stop early due to patience (initial + patience attempts)
        assert len(results) <= 4  # 1 initial + 2 patience + 1 stop
        
        # Verify total score matches expected
        if len(results) > 0:
            assert results[0][1].total_score() == 15  # 3 categories * 5 score
    
    def test_optimization_with_improving_scores(self, sample_input_text, sample_categories):
        """Test optimization with progressively improving scores."""
        generator = Mock(spec=TweetGeneratorModule)
        generator.return_value = "Improving tweet"
        
        evaluator = Mock(spec=TweetEvaluatorModule)
        
        # Create evaluations with improving then declining scores
        scores = [5, 6, 7, 8, 7, 6]
        evaluation_sequence = []
        
        for score in scores:
            evaluation_sequence.append(
                EvaluationResult(evaluations=[
                    CategoryEvaluation(category=cat, reasoning=f"Score {score}", score=score)
                    for cat in sample_categories
                ])
            )
        
        evaluator.side_effect = evaluation_sequence
        
        # Run optimization
        optimizer = HillClimbingOptimizer(
            generator=generator,
            evaluator=evaluator,
            categories=sample_categories,
            max_iterations=10,
            patience=3
        )
        
        results = list(optimizer.optimize(sample_input_text))
        
        # Should have multiple iterations
        assert len(results) > 1
        
        # Best score should be from one of the iterations
        best_scores = [r[1].average_score() for r in results if r[2]]  # Filter improvements
        if best_scores:
            # Compare numeric values, not methods
            max_score = max(best_scores)
            assert max_score >= 5.0  # At least as good as starting score
    
    def test_max_iterations_limit(self, sample_input_text, sample_categories):
        """Test that optimization respects max iterations limit."""
        generator = Mock(spec=TweetGeneratorModule)
        generator.return_value = "Test tweet"
        
        evaluator = Mock(spec=TweetEvaluatorModule)
        
        # Return constant evaluation to force max iterations
        evaluator.return_value = EvaluationResult(evaluations=[
            CategoryEvaluation(category=cat, reasoning="Test", score=6)
            for cat in sample_categories
        ])
        
        max_iter = 5
        optimizer = HillClimbingOptimizer(
            generator=generator,
            evaluator=evaluator,
            categories=sample_categories,
            max_iterations=max_iter,
            patience=10  # High patience, should hit max iterations first
        )
        
        results = list(optimizer.optimize(sample_input_text))
        
        # Should not exceed max iterations
        assert len(results) <= max_iter
    
    def test_generator_inputs_tracked(self, sample_input_text, sample_categories):
        """Test that generator inputs are properly tracked."""
        generator = Mock(spec=TweetGeneratorModule)
        generator.return_value = "Tweet"
        
        evaluator = Mock(spec=TweetEvaluatorModule)
        evaluator.return_value = EvaluationResult(evaluations=[
            CategoryEvaluation(category=cat, reasoning="OK", score=6)
            for cat in sample_categories
        ])
        
        optimizer = HillClimbingOptimizer(
            generator=generator,
            evaluator=evaluator,
            categories=sample_categories,
            max_iterations=3,
            patience=2
        )
        
        results = list(optimizer.optimize(sample_input_text))
        
        # Check that generator inputs are tracked
        for result in results:
            gen_inputs = result[4]
            assert 'input_text' in gen_inputs
            assert gen_inputs['input_text'] == sample_input_text
    
    def test_evaluator_inputs_tracked(self, sample_input_text, sample_categories):
        """Test that evaluator inputs are properly tracked."""
        generator = Mock(spec=TweetGeneratorModule)
        generator.return_value = "Tweet"
        
        evaluator = Mock(spec=TweetEvaluatorModule)
        evaluator.return_value = EvaluationResult(evaluations=[
            CategoryEvaluation(category=cat, reasoning="OK", score=6)
            for cat in sample_categories
        ])
        
        optimizer = HillClimbingOptimizer(
            generator=generator,
            evaluator=evaluator,
            categories=sample_categories,
            max_iterations=3,
            patience=2
        )
        
        results = list(optimizer.optimize(sample_input_text))
        
        # Check that evaluator inputs are tracked
        for result in results:
            eval_inputs = result[5]
            assert 'original_text' in eval_inputs
            assert eval_inputs['original_text'] == sample_input_text
