# Unit Tests

This directory contains comprehensive unit tests for the DSPy Tweet Optimizer application.

## Running Tests

Run all tests:
```bash
pytest tests/
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

### `conftest.py`
Contains shared pytest fixtures used across test files:
- `sample_categories`: Sample evaluation categories
- `sample_category_evaluation`: Sample CategoryEvaluation instance
- `sample_evaluation_result`: Sample EvaluationResult instance
- `sample_settings`: Sample settings dictionary
- `sample_tweet`: Sample tweet text
- `long_tweet`: Tweet that exceeds character limit

### `test_models.py`
Tests for Pydantic data models:
- **CategoryEvaluation**: Score validation, field requirements, integer constraints
- **EvaluationResult**: Total/average score calculations, comparisons, backwards compatibility

### `test_helpers.py`
Tests for helper functions:
- **format_evaluation_for_generator()**: Formatting evaluation results
- **build_settings_dict()**: Settings dictionary construction
- **truncate_tweet()**: Tweet truncation with custom suffixes
- **truncate_category_display()**: Category name truncation

### `test_session_state_manager.py`
Tests for SessionStateManager class:
- **initialize()**: State initialization with defaults and preservation
- **reset_optimization_state()**: Optimization state reset
- **get()**, **set()**, **update()**: State manipulation methods

### `test_utils.py`
Tests for utility functions:
- **Category functions**: save_categories(), load_categories()
- **Settings functions**: save_settings(), load_settings()
- **Input history**: add_to_input_history() with deduplication and trimming
- **Tweet functions**: format_tweet_for_display(), calculate_tweet_length()

## Test Coverage

Current test coverage: **48 tests** covering:
- ✅ Pydantic model validation
- ✅ Helper function logic
- ✅ Session state management
- ✅ File I/O operations (mocked)
- ✅ Input history management
- ✅ Tweet formatting and validation

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
