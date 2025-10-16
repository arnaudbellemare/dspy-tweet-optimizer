# Test Suite

This directory contains comprehensive unit and integration tests for the DSPy Tweet Optimizer application.

## Running Tests

Run all tests (unit + integration):
```bash
pytest tests/
```

Run only unit tests:
```bash
pytest tests/ --ignore=tests/integration/
```

Run only integration tests:
```bash
pytest tests/integration/
```

Run tests with verbose output:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_models.py
```

Run specific test class or function:
```bash
pytest tests/test_models.py::TestCategoryEvaluation::test_valid_category_evaluation
```

## Test Structure

### Unit Tests (`tests/`)

#### `conftest.py`
Contains shared pytest fixtures used across test files:
- `sample_categories`: Sample evaluation categories
- `sample_category_evaluation`: Sample CategoryEvaluation instance
- `sample_evaluation_result`: Sample EvaluationResult instance
- `sample_settings`: Sample settings dictionary
- `sample_tweet`: Sample tweet text
- `long_tweet`: Tweet that exceeds character limit

#### `test_models.py` (14 tests)
Tests for Pydantic data models:
- **CategoryEvaluation**: Score validation, field requirements, integer constraints
- **EvaluationResult**: Total/average score calculations, comparisons, backwards compatibility

#### `test_helpers.py` (14 tests)
Tests for helper functions:
- **format_evaluation_for_generator()**: Formatting evaluation results
- **build_settings_dict()**: Settings dictionary construction
- **truncate_tweet()**: Tweet truncation with custom suffixes
- **truncate_category_display()**: Category name truncation

#### `test_session_state_manager.py` (7 tests)
Tests for SessionStateManager class:
- **initialize()**: State initialization with defaults and preservation
- **reset_optimization_state()**: Optimization state reset
- **get()**, **set()**, **update()**: State manipulation methods

#### `test_utils.py` (13 tests)
Tests for utility functions:
- **Category functions**: save_categories(), load_categories()
- **Settings functions**: save_settings(), load_settings()
- **Input history**: add_to_input_history() with deduplication and trimming
- **Tweet functions**: format_tweet_for_display(), calculate_tweet_length()

### Integration Tests (`tests/integration/`)

#### `integration/conftest.py`
Integration test fixtures:
- `temp_dir`: Temporary directory for file operations
- `sample_categories`, `sample_settings`, `sample_input_text`: Test data
- `mock_lm_response`: Mock LLM response generator
- `create_test_files`: Helper for creating test JSON files

#### `integration/test_optimization_flow.py` (6 tests)
Tests for complete optimization flow:
- **Basic hill climbing**: Full optimization cycle with mocked modules
- **Patience mechanism**: Stops after N iterations without improvement
- **Score improvements**: Handles progressively improving/declining scores
- **Max iterations**: Respects maximum iteration limit
- **Input tracking**: Generator and evaluator inputs are properly tracked

#### `integration/test_file_operations.py` (10 tests)
Tests for file I/O with actual files:
- **Category operations**: Save/load with real files, default creation
- **Settings operations**: Save/load with persistence, default handling
- **Input history**: Deduplication, size limits, empty input handling
- **Cross-file workflows**: Multiple files working together, isolation

#### `integration/test_dspy_modules.py` (8 tests)
Tests for DSPy module integration:
- **Generator module**: Initialization, forward method, feedback handling
- **Evaluator module**: Initialization, evaluation structure, all categories scored
- **Pipeline integration**: Generator→Evaluator workflow, iterative improvement cycles

## Test Coverage

Current test coverage: **72 tests** covering:

**Unit Tests (48)**:
- ✅ Pydantic model validation
- ✅ Helper function logic
- ✅ Session state management
- ✅ File I/O operations (mocked)
- ✅ Input history management
- ✅ Tweet formatting and validation

**Integration Tests (24)**:
- ✅ Hill-climbing optimization flow
- ✅ File operations with real files
- ✅ DSPy module interactions
- ✅ Generator/Evaluator pipeline
- ✅ Feedback loops and iterative improvement

## Mocking Strategy

- **Streamlit**: Uses `MockSessionState` class to simulate Streamlit's session_state behavior
- **File I/O**: Uses `unittest.mock.mock_open` to mock file operations
- **External dependencies**: Mocked using `@patch` decorator

## Adding New Tests

1. Create test file: `tests/test_<module_name>.py`
2. Import required fixtures from `conftest.py`
3. Use descriptive test names: `test_<what_it_does>`
4. Organize tests into classes: `class Test<FeatureName>`
5. Run tests to ensure they pass

## Continuous Integration

These tests are designed to run in CI/CD pipelines and provide:
- Fast execution (< 10 seconds)
- Clear failure messages
- Comprehensive coverage of critical paths
- Mocked external dependencies (no API calls)
