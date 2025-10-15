# DSPy Tweet Optimizer

## Overview

This is a tweet optimization application built with Streamlit and DSPy (Declarative Self-improving Language Programs). The system uses a hill-climbing algorithm to iteratively generate and improve tweets based on customizable evaluation categories. It leverages Claude 3.5 Sonnet through OpenRouter to generate tweets and evaluate them across multiple dimensions, automatically refining the output through multiple iterations to maximize overall quality scores.

**Auto-Optimization**: The app automatically optimizes tweets when you enter text - no buttons needed. Simply type your text and tab out to trigger optimization.

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
  - Receives: original input text, current best tweet, and previous evaluation with detailed reasoning
  - Leverages category-by-category reasoning to make targeted improvements
- **TweetEvaluatorModule**: Uses DSPy's ChainOfThought for structured evaluation with Pydantic models
  - Receives: original input text, current best tweet, tweet to evaluate, and categories
  - Outputs: CategoryEvaluation objects with detailed reasoning and scores (1-9) for each category
  - Validates that improved tweets maintain the same meaning as the original
- **Character Limit Enforcement**: Automatic truncation to 280 characters with ellipsis

**Design Decision**: Separate modules for generation and evaluation enable independent optimization of each concern. Chain-of-thought for both generation and evaluation improves reasoning quality. Providing original text and current best tweet to the evaluator ensures semantic consistency. The evaluator now outputs detailed reasoning alongside scores, which the generator uses as rich feedback for targeted improvements.

#### Optimization Algorithm
- **Strategy**: Hill-climbing algorithm with patience mechanism
- **Iteration Control**: Configurable max iterations (default: 10) and patience counter (default: 5)
- **Feedback Loop**: Generates improvement feedback based on evaluation scores, feeds back to generator
- **Input Transparency**: Displays both generator and evaluator inputs for each iteration via UI expanders
  - Generator inputs: input_text, current_tweet, feedback
  - Evaluator inputs: original_text, current_best_tweet, tweet_being_evaluated

**Rationale**: Hill-climbing provides a simple yet effective optimization strategy for tweet improvement. The patience mechanism prevents infinite loops when no improvements are found. The feedback loop creates a self-improving system where evaluation results directly inform the next generation attempt. Showing both generator and evaluator inputs provides complete transparency into what data is being sent to each LLM module at each iteration, enabling users to understand and debug the optimization process.

#### Evaluation System
- **Customizable Categories**: User-defined evaluation dimensions stored in JSON
- **Scoring**: 1-9 integer scale per category with validation
- **Metrics**: Total score and average score calculations
- **Comparison**: Built-in comparison operators for determining improvements

**Design Decision**: Pydantic models ensure type safety and validation at the evaluation boundary. Customizable categories allow users to optimize for their specific goals (engagement, clarity, emotional impact, etc.). The 1-9 scale provides sufficient granularity while remaining interpretable.

#### Input History System
- **Persistent History**: User inputs stored in `input_history.json` (persists across sessions)
- **Capacity**: Maximum 50 historical inputs (configurable via `MAX_HISTORY_ITEMS`)
- **Deduplication**: Duplicate inputs removed, most recent occurrence kept at top
- **Display Order**: Most recent inputs appear first in dropdown (reverse chronological)
- **Visual Indicator**: 🕐 clock icon marks the 3 most recent entries
- **UI Integration**: Dropdown selector with "Load from history..." placeholder
- **Auto-populate**: Selecting history item populates input text area via Streamlit callback
- **Storage Trigger**: Input added to history when optimization starts

**Implementation Pattern:**
```python
# Callback-based selection (app.py)
def on_history_select():
    if st.session_state.history_selector:
        st.session_state.main_text_input = st.session_state.history_selector
        st.session_state.history_selector = ""  # Reset to placeholder

# History stored with most recent first
add_to_input_history() prepends: [new_input] + history

# Display with visual indicators
format_history_option() adds 🕐 to top 3 items
```

**Design Decision**: Reverse chronological order (newest first) makes it easy to quickly access recent work. Callback approach ensures reliable UI updates. Visual indicators help users identify newest entries at a glance.

#### Automatic Optimization (No Buttons)
- **Auto-Trigger**: Optimization starts automatically when text is entered
- **Conditions**: Text must be non-empty, categories configured, not currently running, and different from last optimized
- **User Flow**: Type text → Tab out → Optimization starts automatically
- **UI Feedback**: Current Best Tweet displays input text immediately, then updates with optimized versions
- **Deduplication**: Tracks last optimized input to prevent redundant runs
- **Progress Display**: Progress bar and status text appear above "Current Best Tweet" during optimization
  - Status format: `**Iteration X/Y** | Current: Z.ZZ | Best: Z.ZZ | No Improvement: X/Y`
  - Shows "✓ Improved!" when score increases, "⚠️ Stopping early" when patience reached
  - Completion message: `✓ **Optimization Complete** | X iterations | Best Score: Z.ZZ`

**Implementation Pattern:**
```python
# Auto-trigger check
should_optimize = (
    input_text.strip() and 
    len(st.session_state.categories) > 0 and 
    not st.session_state.optimization_running and
    input_text.strip() != st.session_state.last_optimized_input
)

if should_optimize:
    st.session_state.optimizing_text = input_text.strip()
    st.session_state.current_tweet = input_text
    st.session_state.optimization_running = True
    st.rerun()  # Update UI immediately

# Run optimization on rerun
if st.session_state.optimization_running:
    optimizer.optimize(st.session_state.optimizing_text)
```

**Design Decision**: Removed manual start/stop buttons for streamlined UX. Text area on_change callback triggers optimization automatically. Immediate rerun ensures UI updates before optimization starts, providing instant feedback.

### Data Models

#### CategoryEvaluation (Pydantic)
- **category**: str - The evaluation category name
- **reasoning**: str - Detailed explanation for the score
- **score**: int - Score from 1-9 with validation

#### EvaluationResult (Pydantic)
- **evaluations**: List[CategoryEvaluation] - List of category evaluations with reasoning
- Provides total_score() and average_score() calculations
- Implements comparison operators for hill-climbing decisions
- Maintains backwards compatibility via category_scores property

**Rationale**: Pydantic provides runtime type checking and validation, ensuring the LLM returns properly formatted evaluation data with detailed reasoning. This prevents downstream errors, makes the optimization loop robust, and provides rich feedback for the generator to make targeted improvements.

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

## Code Organization and Maintainability

### Module Structure

**Core Modules:**
- **constants.py**: Centralized configuration containing all magic numbers, colors, defaults, and error messages
- **helpers.py**: Reusable utility functions to eliminate code duplication
- **ui_components.py**: Modular UI rendering functions for improved code organization
- **models.py**: Pydantic data models for type safety
- **dspy_modules.py**: DSPy module implementations (generator and evaluator)
- **hill_climbing.py**: Optimization algorithm implementation
- **utils.py**: Utility functions for file I/O and DSPy initialization
- **app.py**: Main application entry point with clean, focused functions

**Key Design Principles:**
- DRY (Don't Repeat Yourself): Eliminated code duplication through helper functions
- Single Responsibility: Each function has one clear purpose
- Constants over Magic Numbers: All hardcoded values centralized in constants.py
- Type Safety: Comprehensive type hints throughout codebase
- Modular UI: UI components separated for reusability and testing

**Helper Functions:**
- `format_evaluation_for_generator()`: Formats evaluation results for generator input (eliminates duplication)
- `build_settings_dict()`: Constructs settings dictionary for persistence
- `truncate_tweet()`: Handles tweet truncation with configurable suffix
- `truncate_category_display()`: Truncates category names for display

**UI Components:**
- `render_custom_css()`: Applies application theme
- `render_main_header()`: Main page header
- `render_category_management()`: Category CRUD interface
- `render_best_tweet_display()`: Tweet display component
- `render_generator_inputs()`: Generator input transparency
- `render_evaluator_inputs()`: Evaluator input transparency
- `render_optimization_stats()`: Live optimization statistics
- `render_latest_evaluation()`: Evaluation results with reasoning
- `render_score_history()`: Detailed score visualization

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