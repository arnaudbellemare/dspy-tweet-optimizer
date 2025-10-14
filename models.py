from pydantic import BaseModel, Field, validator
from typing import List

class EvaluationResult(BaseModel):
    """Pydantic model for tweet evaluation results."""
    
    category_scores: List[int] = Field(
        description="Scores for each evaluation category on a scale of 1-9",
        min_items=1
    )
    
    @validator('category_scores')
    def validate_scores(cls, scores):
        """Ensure all scores are within the valid range of 1-9."""
        for score in scores:
            if not isinstance(score, int) or score < 1 or score > 9:
                raise ValueError(f"Score {score} must be an integer between 1 and 9")
        return scores
    
    def total_score(self) -> float:
        """Calculate the total score across all categories."""
        return sum(self.category_scores)
    
    def average_score(self) -> float:
        """Calculate the average score across all categories."""
        return sum(self.category_scores) / len(self.category_scores)
    
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
