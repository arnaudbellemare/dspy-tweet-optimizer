from pydantic import BaseModel, Field, validator
from typing import List

class CategoryEvaluation(BaseModel):
    """Pydantic model for a single category evaluation with reasoning."""
    
    category: str = Field(description="The evaluation category name")
    reasoning: str = Field(description="Explanation for the score")
    score: int = Field(description="Score for this category (1-9)", ge=1, le=9)
    
    @validator('score')
    def validate_score(cls, score):
        """Ensure score is within the valid range of 1-9."""
        if not isinstance(score, int) or score < 1 or score > 9:
            raise ValueError(f"Score {score} must be an integer between 1 and 9")
        return score

class EvaluationResult(BaseModel):
    """Pydantic model for tweet evaluation results."""
    
    evaluations: List[CategoryEvaluation] = Field(
        description="List of category evaluations with reasoning and scores",
        min_items=1
    )
    
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
