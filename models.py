from pydantic import BaseModel, Field, validator
from typing import List
from constants import MIN_SCORE, MAX_SCORE

class CategoryEvaluation(BaseModel):
    """Pydantic model for a single category evaluation with reasoning."""
    
    category: str = Field(description="The evaluation category name")
    reasoning: str = Field(description="Explanation for the score")
    score: int = Field(
        description=f"Score for this category ({MIN_SCORE}-{MAX_SCORE})", 
        ge=MIN_SCORE, 
        le=MAX_SCORE
    )
    
    @validator('score')
    def validate_score(cls, score):
        """Ensure score is within the valid range."""
        if not isinstance(score, int) or score < MIN_SCORE or score > MAX_SCORE:
            raise ValueError(f"Score {score} must be an integer between {MIN_SCORE} and {MAX_SCORE}")
        return score

class EvaluationResult(BaseModel):
    """Pydantic model for tweet evaluation results."""
    
    evaluations: List[CategoryEvaluation] = Field(
        description="List of category evaluations with reasoning and scores"
    )
    
    @validator('evaluations')
    def validate_evaluations(cls, evals):
        """Ensure we have at least one evaluation."""
        if not evals or len(evals) < 1:
            raise ValueError("Must have at least one category evaluation")
        return evals
    
    @property
    def category_scores(self) -> List[int]:
        """Get list of scores for backwards compatibility."""
        return [eval.score for eval in self.evaluations]
    
    def total_score(self) -> float:
        """Calculate the total score across all categories."""
        return sum(eval.score for eval in self.evaluations)
    
    def average_score(self) -> float:
        """Calculate the average score across all categories."""
        return self.total_score() / len(self.evaluations)
    
    def __gt__(self, other):
        """Compare evaluation results based on total score."""
        if not isinstance(other, EvaluationResult):
            return NotImplemented
        return self.total_score() > other.total_score()
    
    def __eq__(self, other):
        """Check equality based on total score."""
        if not isinstance(other, EvaluationResult):
            return NotImplemented
        return self.total_score() == other.total_score()
