## Overview

This project is a tweet optimization application built with Streamlit and DSPy. It leverages Claude 3.5 Sonnet via OpenRouter to generate and iteratively improve tweets based on customizable evaluation categories. The system employs a hill-climbing algorithm to refine tweet quality automatically, providing real-time feedback and transparency into the optimization process. The application focuses on auto-optimization, triggering improvements as soon as text is entered.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Frontend**: Streamlit web application with custom CSS theming.
- **Language Model Framework**: DSPy for structured LLM interactions and chain-of-thought reasoning.
- **Language Model Provider**: Claude 3.5 Sonnet via OpenRouter API.

### Core Components

#### Tweet Generation Pipeline
- **TweetGeneratorModule**: Uses DSPy's ChainOfThought to generate or improve tweets based on input text, current best tweet, and detailed evaluation feedback.
- **TweetEvaluatorModule**: Uses DSPy's ChainOfThought for structured evaluation with Pydantic models, providing scores (1-9) and detailed reasoning across categories. Ensures semantic consistency with the original input.
- **Character Limit Enforcement**: Automatic truncation to 280 characters.

#### Optimization Algorithm
- **Strategy**: Hill-climbing algorithm with a configurable patience mechanism to prevent infinite loops.
- **Feedback Loop**: Evaluation scores and reasoning directly inform the next generation attempt.
- **Transparency**: UI displays inputs for both generator and evaluator for each iteration.

#### Evaluation System
- **Customizable Categories**: User-defined evaluation dimensions stored in JSON.
- **Scoring**: 1-9 integer scale per category.
- **Metrics**: Total and average score calculations.
- **Comparison**: Built-in operators for determining improvements.

#### Input History System
- **Persistence**: Stores user inputs in `input_history.json` (max 50 items) for cross-session access.
- **Deduplication**: Keeps only the most recent occurrence of duplicate inputs.
- **UI Integration**: Dropdown selector with visual indicators for recent entries.

#### Automatic Optimization
- **Auto-Trigger**: Optimization starts automatically upon text input, with no manual buttons.
- **Conditions**: Requires non-empty text, configured categories, and not currently running.
- **UI Feedback**: Provides real-time progress, status updates, and completion messages during optimization.

### Data Models
- **CategoryEvaluation (Pydantic)**: Defines evaluation details for a single category, including name, reasoning, and a 1-9 score.
- **EvaluationResult (Pydantic)**: Aggregates multiple `CategoryEvaluation` objects, provides total/average scores, and comparison operators. Ensures type safety and detailed feedback from the LLM.

### State Management
- **Session State**: Streamlit's session state for UI persistence within a user session.
- **File-based Storage**: `categories.json` and `settings.json` persist user preferences (model, iterations, patience) and custom categories across sessions.
- **Defaults**: Sensible default values are provided if configuration files are missing.

### DSPy Configuration Pattern
- **Thread-Safe Model Switching**: Implements a solution for Streamlit's multi-threaded environment by configuring DSPy once globally and using `dspy.context(lm=selected_lm)` for model switching to prevent configuration errors. Cached LM instances (`@st.cache_resource`) ensure efficiency.

## External Dependencies

### Language Model API
- **Service**: OpenRouter (https://openrouter.ai/api/v1)
- **Model**: anthropic/claude-3.5-sonnet (default)
- **Authentication**: `OPENROUTER_API_KEY` environment variable.
- **Purpose**: Powers both tweet generation and evaluation processes.

### Python Libraries
- **streamlit**: Web application framework.
- **dspy-ai**: Language model programming framework.
- **pydantic**: Data validation and settings management.
- **pandas**: Used for data structuring (e.g., displaying results).

### Configuration Files
- **categories.json**: Stores user-defined evaluation categories.
- **settings.json**: Stores user preferences (LLM model, max iterations, patience).
- **input_history.json**: Stores recent inputs for quick access.
- **Environment Variables**: `OPENROUTER_API_KEY` for API authentication.

## Code Architecture

### Module Structure

**Core Modules:**
- **constants.py**: Centralized configuration containing all magic numbers, colors, defaults, and error messages
- **session_state_manager.py**: SessionStateManager class for centralized session state initialization and management
- **optimization_manager.py**: OptimizationManager class for optimization loop execution and progress tracking
- **helpers.py**: Reusable utility functions to eliminate code duplication
- **ui_components.py**: Modular UI rendering functions for improved code organization
- **models.py**: Pydantic data models for type safety
- **dspy_modules.py**: DSPy module implementations (generator and evaluator)
- **hill_climbing.py**: Optimization algorithm implementation
- **utils.py**: Utility functions for file I/O and DSPy initialization
- **app.py**: Main application entry point with clean, focused functions

**Key Design Principles:**
- DRY (Don't Repeat Yourself): Eliminated code duplication through helper functions and manager classes
- Single Responsibility: Each function has one clear purpose
- Constants over Magic Numbers: All hardcoded values centralized in constants.py
- Type Safety: Comprehensive type hints throughout codebase
- Modular UI: UI components separated for reusability and testing
- Separation of Concerns: Business logic separated from UI logic through manager classes

**Architecture Improvements (October 2025):**
- **SessionStateManager**: Centralized class for session state management
  - Eliminates repetitive if-not-in-state checks across 20+ state variables
  - Provides clean initialization with `SessionStateManager.initialize()`
  - Offers utility methods: `get()`, `set()`, `update()`, `reset_optimization_state()`
  - Improves maintainability and reduces boilerplate code by ~40 lines
- **OptimizationManager**: Extracted optimization loop logic from app.py
  - Encapsulates optimization execution in `run_optimization()` method
  - Handles progress tracking and UI updates in isolation
  - Separates business logic from presentation layer
  - Reduces app.py complexity by ~60 lines
- **Enhanced Constants**: Added UI-related constants
  - `HISTORY_RECENT_INDICATOR`, `HISTORY_RECENT_COUNT`, `HISTORY_TRUNCATE_LENGTH`
  - All magic numbers now centralized for easy configuration

## Testing

### Test Infrastructure
- **Framework**: pytest with pytest-mock
- **Coverage**: 48 comprehensive unit tests
- **Execution Time**: < 10 seconds
- **Location**: `tests/` directory

### Test Coverage
- ✅ **Pydantic Models**: Score validation, comparisons, field requirements
- ✅ **Helper Functions**: Text formatting, truncation, settings management
- ✅ **Session State Manager**: Initialization, updates, state reset
- ✅ **Utility Functions**: File I/O, input history, tweet processing
- ✅ **Mocked Dependencies**: Streamlit session_state, file operations

### Running Tests
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py
```

### Test Organization
- **conftest.py**: Shared fixtures (sample data, mock objects)
- **test_models.py**: Pydantic model validation tests
- **test_helpers.py**: Helper function tests
- **test_session_state_manager.py**: State management tests
- **test_utils.py**: Utility function tests
- **MockSessionState**: Custom mock class simulating Streamlit's session_state

See `tests/README.md` for detailed testing documentation.