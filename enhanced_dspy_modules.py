"""
Enhanced DSPy modules with advanced LLM integration.

This module extends the original DSPy modules to support:
- Multiple LLM providers (Ollama, Perplexity, etc.)
- GEPA-ACE context optimization
- Web search capabilities for tweet optimization
- Advanced reasoning with real-time information
"""

import dspy
from typing import List, Optional, Dict, Any
from models import EvaluationResult, CategoryEvaluation
from advanced_llm_manager import advanced_llm_manager, setup_advanced_llm_system
from constants import (
    TWEET_MAX_LENGTH,
    TWEET_TRUNCATION_SUFFIX,
    TWEET_TRUNCATION_LENGTH,
    DEFAULT_SCORE,
    ERROR_PARSING,
    ERROR_VALIDATION,
    ERROR_GENERATION,
    ERROR_EVALUATION,
    MIN_SCORE,
    MAX_SCORE
)
from helpers import format_evaluation_for_generator, truncate_tweet
import logging

logger = logging.getLogger(__name__)

class EnhancedTweetGenerator(dspy.Signature):
    """Enhanced tweet generator with web search and context optimization capabilities."""
    
    input_text: str = dspy.InputField(desc="Original text or current tweet to improve")
    current_tweet: str = dspy.InputField(desc="Current best tweet version (empty for first generation)")
    previous_evaluation: str = dspy.InputField(desc="Previous evaluation with category-by-category reasoning and scores (empty for first generation)")
    web_context: str = dspy.InputField(desc="Relevant web information for context (optional)")
    improved_tweet: str = dspy.OutputField(desc=f"Generated or improved tweet text (max {TWEET_MAX_LENGTH} characters)")

class EnhancedTweetEvaluator(dspy.Signature):
    """Enhanced tweet evaluator with advanced reasoning and web context awareness."""
    
    original_text: str = dspy.InputField(desc="Original input text that started the optimization")
    current_best_tweet: str = dspy.InputField(desc="Current best tweet version for comparison (empty for first evaluation)")
    tweet_text: str = dspy.InputField(desc="Tweet text to evaluate")
    categories: str = dspy.InputField(desc="Comma-separated list of evaluation category descriptions")
    web_context: str = dspy.InputField(desc="Relevant web information for evaluation context (optional)")
    evaluations: List[CategoryEvaluation] = dspy.OutputField(
        desc=f"List of evaluations with category name, detailed reasoning, and score ({MIN_SCORE}-{MAX_SCORE}) for each category. Consider web context and current trends."
    )

class WebSearchModule:
    """Module for web search and context gathering."""
    
    def __init__(self):
        self.search_cache = {}
    
    def search_relevant_context(self, topic: str, max_results: int = 3) -> str:
        """
        Search for relevant web context about a topic.
        
        Args:
            topic: The topic to search for
            max_results: Maximum number of search results to include
            
        Returns:
            Concatenated relevant context from web search
        """
        # Use cache if available
        if topic in self.search_cache:
            return self.search_cache[topic]
        
        try:
            # Use Perplexity provider for web search if available
            if "perplexity_sonar" in advanced_llm_manager.providers:
                search_prompt = f"""
                Search for recent, relevant information about: {topic}
                
                Focus on:
                - Current trends and discussions
                - Popular opinions and reactions
                - Recent news or developments
                - Social media sentiment
                
                Provide concise, factual information that would help optimize a tweet about this topic.
                """
                
                context = advanced_llm_manager.generate(
                    search_prompt,
                    provider="perplexity_sonar",
                    use_context_optimization=True
                )
                
                self.search_cache[topic] = context
                return context
            else:
                # Fallback: return empty context
                return ""
                
        except Exception as e:
            logger.warning(f"Web search failed: {e}")
            return ""
    
    def extract_topic_keywords(self, text: str) -> List[str]:
        """Extract key topics/keywords from text for web search."""
        # Simple keyword extraction - in practice, this could use NLP libraries
        words = text.lower().split()
        
        # Filter out common words and extract meaningful terms
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should"}
        
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Return top 3 most relevant keywords
        return keywords[:3]

class EnhancedTweetGeneratorModule(dspy.Module):
    """Enhanced DSPy module for generating and improving tweets with web context."""
    
    def __init__(self, use_web_search: bool = True):
        super().__init__()
        self.generate = dspy.ChainOfThought(EnhancedTweetGenerator)
        self.web_search = WebSearchModule()
        self.use_web_search = use_web_search
    
    def forward(self, input_text: str, current_tweet: str = "", previous_evaluation: Optional[EvaluationResult] = None) -> str:
        """Generate or improve a tweet with enhanced context."""
        try:
            # Format previous evaluation as text
            eval_text = format_evaluation_for_generator(previous_evaluation)
            
            # Get web context if enabled
            web_context = ""
            if self.use_web_search:
                keywords = self.web_search.extract_topic_keywords(input_text)
                if keywords:
                    topic = " ".join(keywords)
                    web_context = self.web_search.search_relevant_context(topic)
            
            result = self.generate(
                input_text=input_text,
                current_tweet=current_tweet,
                previous_evaluation=eval_text,
                web_context=web_context
            )
            
            # Ensure tweet doesn't exceed character limit
            tweet = truncate_tweet(result.improved_tweet, TWEET_MAX_LENGTH, TWEET_TRUNCATION_SUFFIX)
            
            return tweet
        except Exception as e:
            logger.error(f"Enhanced tweet generation failed: {e}")
            raise Exception(f"{ERROR_GENERATION}: {str(e)}")

class EnhancedTweetEvaluatorModule(dspy.Module):
    """Enhanced DSPy module for evaluating tweets with web context awareness."""
    
    def __init__(self, use_web_search: bool = True):
        super().__init__()
        self.evaluate = dspy.ChainOfThought(EnhancedTweetEvaluator)
        self.web_search = WebSearchModule()
        self.use_web_search = use_web_search
    
    def forward(self, tweet_text: str, categories: List[str], original_text: str = "", current_best_tweet: str = "") -> EvaluationResult:
        """Evaluate a tweet across specified categories with web context."""
        try:
            # Join categories into comma-separated string
            categories_str = ", ".join(categories)
            
            # Get web context if enabled
            web_context = ""
            if self.use_web_search:
                keywords = self.web_search.extract_topic_keywords(tweet_text)
                if keywords:
                    topic = " ".join(keywords)
                    web_context = self.web_search.search_relevant_context(topic)
            
            result = self.evaluate(
                original_text=original_text,
                current_best_tweet=current_best_tweet,
                tweet_text=tweet_text,
                categories=categories_str,
                web_context=web_context
            )
            
            # Extract and validate evaluations
            evaluations = result.evaluations
            
            # Ensure we have the right number of evaluations
            if len(evaluations) != len(categories):
                # Create default evaluations if mismatch
                evaluations = [
                    CategoryEvaluation(
                        category=cat,
                        reasoning=ERROR_PARSING,
                        score=DEFAULT_SCORE
                    ) for cat in categories
                ]
            else:
                # Validate each evaluation
                validated_evals = []
                for i, eval in enumerate(evaluations):
                    try:
                        # Ensure score is valid
                        score = max(MIN_SCORE, min(MAX_SCORE, int(eval.score)))
                        validated_evals.append(CategoryEvaluation(
                            category=categories[i] if i < len(categories) else eval.category,
                            reasoning=eval.reasoning if eval.reasoning else "No reasoning provided",
                            score=score
                        ))
                    except (ValueError, TypeError, AttributeError):
                        validated_evals.append(CategoryEvaluation(
                            category=categories[i] if i < len(categories) else "Unknown",
                            reasoning=ERROR_VALIDATION,
                            score=DEFAULT_SCORE
                        ))
                evaluations = validated_evals
            
            # Create validated result
            validated_result = EvaluationResult(evaluations=evaluations)
            
            return validated_result
        except Exception as e:
            logger.error(f"Enhanced tweet evaluation failed: {e}")
            # Return default evaluations on error
            default_evals = [
                CategoryEvaluation(
                    category=cat,
                    reasoning=f"{ERROR_EVALUATION}: {str(e)}",
                    score=DEFAULT_SCORE
                ) for cat in categories
            ]
            return EvaluationResult(evaluations=default_evals)

class HybridOptimizationModule:
    """Module for hybrid optimization using multiple LLM providers."""
    
    def __init__(self):
        self.optimization_strategies = {
            "local_fast": "ollama_gemma3_4b",
            "web_enhanced": "perplexity_sonar",
            "balanced": None  # Use hybrid routing
        }
    
    def optimize_with_strategy(self, strategy: str, prompt: str, **kwargs) -> str:
        """
        Optimize using a specific strategy.
        
        Args:
            strategy: Optimization strategy ("local_fast", "web_enhanced", "balanced")
            prompt: The prompt to optimize
            **kwargs: Additional parameters
            
        Returns:
            Optimized result
        """
        provider = self.optimization_strategies.get(strategy)
        
        if strategy == "web_enhanced":
            # Use web search for enhanced context
            kwargs["use_context_optimization"] = True
        
        return advanced_llm_manager.generate(
            prompt=prompt,
            provider=provider,
            **kwargs
        )
    
    def get_available_strategies(self) -> List[str]:
        """Get list of available optimization strategies."""
        available = []
        
        for strategy, provider in self.optimization_strategies.items():
            if provider is None:  # Balanced strategy (hybrid routing)
                available.append(strategy)
            elif provider in advanced_llm_manager.providers:
                if advanced_llm_manager.providers[provider].is_available():
                    available.append(strategy)
        
        return available

# Initialize the advanced LLM system
def initialize_enhanced_system():
    """Initialize the enhanced DSPy system with advanced LLM capabilities."""
    try:
        # Set up advanced LLM manager
        setup_advanced_llm_system()
        
        # Create enhanced modules
        enhanced_generator = EnhancedTweetGeneratorModule(use_web_search=True)
        enhanced_evaluator = EnhancedTweetEvaluatorModule(use_web_search=True)
        hybrid_optimizer = HybridOptimizationModule()
        
        logger.info("Enhanced DSPy system initialized successfully")
        
        return {
            "generator": enhanced_generator,
            "evaluator": enhanced_evaluator,
            "hybrid_optimizer": hybrid_optimizer,
            "web_search": WebSearchModule()
        }
        
    except Exception as e:
        logger.error(f"Failed to initialize enhanced system: {e}")
        raise

# Global instances
enhanced_modules = None

def get_enhanced_modules():
    """Get or create enhanced modules."""
    global enhanced_modules
    if enhanced_modules is None:
        enhanced_modules = initialize_enhanced_system()
    return enhanced_modules
