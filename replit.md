# DSPy Tweet Optimizer

## Overview

This is a tweet optimization application built with Streamlit and DSPy (Declarative Self-improving Language Programs). The system uses a hill-climbing algorithm to iteratively generate and improve tweets based on customizable evaluation categories. It leverages Claude 3.5 Sonnet through OpenRouter to generate tweets and evaluate them across multiple dimensions, automatically refining the output through multiple iterations to maximize overall quality scores.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Frontend**: Streamlit web application with custom CSS theming (pop-punk aesthetic)
- **Language Model Framework**: DSPy for structured language model interactions and chain-of-thought reasoning
- **Language Model Provider**: Claude 3.5 Sonnet via OpenRouter API

**Rationale**: Streamlit provides rapid prototyping and an interactive UI for iterative tweet optimization. DSPy offers structured signatures and typed predictors for reliable LLM interactions, with built-in support for chain-of-thought reasoning which improves tweet generation quality.

### Core Components

#### Tweet Generation Pipeline
- **TweetGeneratorModule**: Uses DSPy's ChainOfThought to generate or improve tweets
- **TweetEvaluatorModule**: Uses DSPy's TypedPredictor for structured evaluation with Pydantic models
- **Character Limit Enforcement**: Automatic truncation to 280 characters with ellipsis

**Design Decision**: Separate modules for generation and evaluation enable independent optimization of each concern. Chain-of-thought for generation improves reasoning quality, while typed prediction ensures structured, parseable evaluation results.

#### Optimization Algorithm
- **Strategy**: Hill-climbing algorithm with patience mechanism
- **Iteration Control**: Configurable max iterations (default: 10) and patience counter (default: 5)
- **Feedback Loop**: Generates improvement feedback based on evaluation scores, feeds back to generator
- **Input Transparency**: Displays generator inputs (input_text, current_tweet, feedback) for each iteration via UI expander

**Rationale**: Hill-climbing provides a simple yet effective optimization strategy for tweet improvement. The patience mechanism prevents infinite loops when no improvements are found. The feedback loop creates a self-improving system where evaluation results directly inform the next generation attempt. Showing generator inputs provides transparency into what's being sent to the LLM at each iteration.

#### Evaluation System
- **Customizable Categories**: User-defined evaluation dimensions stored in JSON
- **Scoring**: 1-9 integer scale per category with validation
- **Metrics**: Total score and average score calculations
- **Comparison**: Built-in comparison operators for determining improvements

**Design Decision**: Pydantic models ensure type safety and validation at the evaluation boundary. Customizable categories allow users to optimize for their specific goals (engagement, clarity, emotional impact, etc.). The 1-9 scale provides sufficient granularity while remaining interpretable.

### Data Models

#### EvaluationResult (Pydantic)
- Validates category scores are integers between 1-9
- Provides total_score() and average_score() calculations
- Implements comparison operators for hill-climbing decisions

**Rationale**: Pydantic provides runtime type checking and validation, ensuring the LLM returns properly formatted evaluation data. This prevents downstream errors and makes the optimization loop robust.

### State Management
- **Session State**: Streamlit session state for UI persistence within a session
- **File-based Storage**: 
  - `categories.json` for evaluation category persistence across sessions
  - `settings.json` for user preferences (model, iterations, patience) across sessions
- **Default Values**: Fallback to sensible defaults if files are missing or corrupted

**Design Decision**: Lightweight file-based storage is sufficient for this application's needs. Session state enables reactive UI updates during optimization iterations, while JSON files provide cross-session persistence for user preferences.

**Persisted Settings:**
- Selected LLM model (default: Claude Sonnet 4.5)
- Max iterations (default: 10)
- Patience threshold (default: 5)
- DSPy cache enabled (default: True)
- Custom evaluation categories

## External Dependencies

### Language Model API
- **Service**: OpenRouter (https://openrouter.ai/api/v1)
- **Model**: anthropic/claude-3.5-sonnet
- **Authentication**: API key via OPENROUTER_API_KEY environment variable
- **Purpose**: Powers both tweet generation and evaluation

**Integration Details**: DSPy's OpenAI adapter is configured to use OpenRouter's API endpoint, allowing access to Claude 3.5 Sonnet through a unified interface.

### Python Libraries
- **streamlit**: Web application framework and UI components
- **dspy-ai**: Language model programming framework with signatures and modules
- **pydantic**: Data validation and settings management
- **pandas**: Data structure support (likely for displaying results)

### Configuration Files
- **categories.json**: Stores user-defined evaluation categories (persists across sessions)
- **settings.json**: Stores user preferences for model, iterations, and patience (persists across sessions)
- **Environment Variables**: OPENROUTER_API_KEY for API authentication

## Technical Implementation Notes

### DSPy Configuration Pattern (Thread-Safe Model Switching)

**Problem**: DSPy's `dspy.configure()` is thread-sensitive and can only be called once per thread. Streamlit's multi-threaded architecture causes errors when attempting to reconfigure DSPy for different models.

**Solution**: 
1. **One-time Global Configuration**: DSPy is configured exactly once on first run using a global flag (`dspy._replit_configured`)
2. **Cached LM Instances**: Individual LM instances are created and cached per model using `@st.cache_resource`
3. **Context-based Model Switching**: Use `dspy.context(lm=selected_lm)` to temporarily switch models without reconfiguration

**Implementation**:
```python
# In utils.py
@st.cache_resource
def get_dspy_lm(model_name: str):
    """Get a DSPy LM instance for the specified model (cached per model)."""
    return dspy.LM(model=model_name, api_key=..., api_base=...)

def initialize_dspy(model_name: str):
    """Initialize DSPy once globally."""
    if not hasattr(dspy, '_replit_configured'):
        default_lm = get_dspy_lm(model_name)
        dspy.configure(lm=default_lm)
        dspy._replit_configured = True

# In app.py - During optimization
selected_lm = get_dspy_lm(st.session_state.selected_model)
with dspy.context(lm=selected_lm):
    for iteration, (tweet, scores, improved) in enumerate(optimizer.optimize(input_text)):
        # Optimization runs with selected model
```

**Key Points**:
- Never call `dspy.configure()` more than once
- Always wrap DSPy module usage in `dspy.context()` when using non-default models
- LM instances are lightweight and safe to cache
- This pattern prevents "settings can only be changed by the thread that initially configured it" errors

**Available Models** (October 2025):
- Claude Sonnet 4.5 (default)
- Opus 4.1
- Gemini 2.5 Flash
- Gemini 2.5 Flash Lite
- Gemini 2.5 Pro
- GPT-5