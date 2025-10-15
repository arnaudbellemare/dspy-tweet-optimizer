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
- **Environment Variables**: `OPENROUTER_API_KEY` for API authentication.