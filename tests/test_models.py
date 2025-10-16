"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError
from models import CategoryEvaluation, EvaluationResult
from constants import MIN_SCORE, MAX_SCORE


class TestCategoryEvaluation:
    """Tests for CategoryEvaluation model."""
    
    def test_valid_category_evaluation(self):
        """Test creating a valid CategoryEvaluation."""
        eval = CategoryEvaluation(
            category="Test Category",
            reasoning="This is a test reasoning",
            score=7
        )
        assert eval.category == "Test Category"
        assert eval.reasoning == "This is a test reasoning"
        assert eval.score == 7
    
    def test_score_validation_min(self):
        """Test score validation for minimum value."""
        with pytest.raises(ValidationError):
            CategoryEvaluation(
                category="Test",
                reasoning="Test",
                score=0  # Below MIN_SCORE
            )
    
    def test_score_validation_max(self):
        """Test score validation for maximum value."""
        with pytest.raises(ValidationError):
            CategoryEvaluation(
                category="Test",
                reasoning="Test",
                score=10  # Above MAX_SCORE
            )
    
    def test_score_validation_valid_range(self):
        """Test that all valid scores (1-9) work."""
        for score in range(MIN_SCORE, MAX_SCORE + 1):
            eval = CategoryEvaluation(
                category="Test",
                reasoning="Test",
                score=score
            )
            assert eval.score == score
    
    def test_score_must_be_integer(self):
        """Test that score must be an integer."""
        with pytest.raises(ValidationError):
            CategoryEvaluation(
                category="Test",
                reasoning="Test",
                score=7.5  # Float not allowed
            )


class TestEvaluationResult:
    """Tests for EvaluationResult model."""
    
    def test_valid_evaluation_result(self, sample_evaluation_result):
        """Test creating a valid EvaluationResult."""
        assert len(sample_evaluation_result.evaluations) == 3
        assert sample_evaluation_result.total_score() == 24
        assert sample_evaluation_result.average_score() == 8.0
    
    def test_empty_evaluations_fails(self):
        """Test that empty evaluations list fails validation."""
        with pytest.raises(ValidationError):
            EvaluationResult(evaluations=[])
    
    def test_total_score_calculation(self):
        """Test total score calculation."""
        result = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="C1", reasoning="R1", score=5),
                CategoryEvaluation(category="C2", reasoning="R2", score=7),
                CategoryEvaluation(category="C3", reasoning="R3", score=9)
            ]
        )
        assert result.total_score() == 21
    
    def test_average_score_calculation(self):
        """Test average score calculation."""
        result = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="C1", reasoning="R1", score=6),
                CategoryEvaluation(category="C2", reasoning="R2", score=8),
                CategoryEvaluation(category="C3", reasoning="R3", score=7)
            ]
        )
        assert result.average_score() == 7.0
    
    def test_category_scores_property(self):
        """Test category_scores property for backwards compatibility."""
        result = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="C1", reasoning="R1", score=5),
                CategoryEvaluation(category="C2", reasoning="R2", score=8)
            ]
        )
        assert result.category_scores == [5, 8]
    
    def test_comparison_greater_than(self):
        """Test greater than comparison."""
        result1 = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="C1", reasoning="R1", score=8)
            ]
        )
        result2 = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="C1", reasoning="R1", score=5)
            ]
        )
        assert result1 > result2
        assert not (result2 > result1)
    
    def test_comparison_equality(self):
        """Test equality comparison."""
        result1 = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="C1", reasoning="R1", score=7)
            ]
        )
        result2 = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="C1", reasoning="R1", score=7)
            ]
        )
        assert result1 == result2
    
    def test_comparison_multiple_categories(self):
        """Test comparison with multiple categories (total score)."""
        result1 = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="C1", reasoning="R1", score=5),
                CategoryEvaluation(category="C2", reasoning="R2", score=5)
            ]
        )
        result2 = EvaluationResult(
            evaluations=[
                CategoryEvaluation(category="C1", reasoning="R1", score=3),
                CategoryEvaluation(category="C2", reasoning="R2", score=6)
            ]
        )
        # Both have total of 10 and 9
        assert result1 > result2
