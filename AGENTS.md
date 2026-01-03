# Agent Guidelines for sauron-engine

## Build, Lint, and Test Commands

### Testing
```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/engine_tests/test_simple_engine.py

# Run specific test class
poetry run pytest tests/engine_tests/test_simple_engine.py::TestFirstEngineCases

# Run specific test method
poetry run pytest tests/engine_tests/test_simple_engine.py::TestFirstEngineCases::test_parsed_rules

# Run with coverage
poetry run pytest --cov=sauron --cov-report=html

# Run tests using tox (runs on py39 through py314)
tox
```

### Code Quality
```bash
# Format and lint with ruff (does both in one command)
poetry run ruff check sauron/ tests/

# Format code only
poetry run ruff format sauron/ tests/

# Fix linting issues automatically
poetry run ruff check --fix sauron/ tests/

# Type check with zuban
poetry run zuban check

# Run all quality checks (via pre-commit)
poetry run pre-commit run --all-files
```

### Task Runner (poethepoet)
```bash
# Run all tasks using poethepoet (preferred method)
poetry run poe <task>

# Available tasks:
# test          - Run all tests
# test-cov      - Run tests with coverage
# ruff          - Run ruff linting
# format        - Run ruff formatting
# formatcheck   - Check ruff formatting without modifying
# lint-fix      - Auto-fix linting issues
# typecheck     - Run zuban type checking
# lint          - Run all quality checks (ruff, formatcheck, typecheck)
# pre-commit    - Run all pre-commit hooks
# docs-build    - Build documentation
# docs-serve    - Serve documentation with live reload
# check-all     - Run all checks (lint, format, typecheck, test)

# Examples:
poetry run poe test
poetry run poe check-all
poetry run poe docs-serve
```

### Dependency Management
```bash
# Install dependencies
poetry install

# Add a dependency
poetry add <package>

# Update dependencies
poetry update
```

## Code Style Guidelines

### Imports
- Import order: standard library → third-party → local imports
- Use absolute imports for local modules (e.g., `from sauron.models import JobModel`)
- Group imports with blank lines between groups
- Avoid wildcard imports (except in specific cases like type stubs)
- Ruff automatically handles import sorting (I001)

### Formatting
- **Line length**: Maximum 79 characters (enforced by ruff)
- **Indentation**: 4 spaces (no tabs)
- **Trailing whitespace**: None
- Use ruff formatter for consistent style (replaces Black)
- Ruff lint rules ignores: E203, E266, E501, W503 (same as flake8)

### Type Annotations
- All functions must include type hints for parameters and return values
- Use `typing` module for complex types: `List[Type[JobModel]]`, `Dict[str, Any]`, `Union[str, Dict[str, Any]]`
- Use `Type[ClassName]` for class type annotations
- Use `Optional[T]` or `T | None` for nullable types
- Apply zuban type checking before committing

### Naming Conventions
- **Classes**: PascalCase (e.g., `Engine`, `JobModel`, `DefaultParser`)
- **Functions/Methods**: snake_case (e.g., `parse`, `apply_job_call`, `_add_callable`)
- **Variables**: snake_case (e.g., `parsed_rule`, `callables_collected`)
- **Constants**: UPPER_CASE (e.g., use sparingly for module-level constants)
- **Private methods**: Prefix with underscore (e.g., `_parse_single_job`)

### Code Structure
- Use Pydantic `BaseModel` for data models
- Class attributes defined before methods
- Type hints on class attributes (e.g., `session: Dict[str, Any] = {}`)
- Docstrings on classes and public methods
- Use decorators for job registration: `@engine.job()`, `@engine.condition()`, `@engine.action()`

### Error Handling
- Raise `ValueError` with descriptive messages for invalid inputs
- Use try/except blocks for error handling (e.g., JSONDecodeError in parsers)
- Validate inputs before processing

### Testing
- Use pytest framework
- Test files located in `tests/` directory mirroring `sauron/` structure
- Use `setup()` method in test classes for common initialization
- Follow given/when/then pattern in test comments where appropriate
- Test both success and failure cases
- Use descriptive test names: `test_can_parse_the_test_string`, `test_runtime_metrics_zero_values_before_ran`

### Documentation
- Docstrings on public classes and methods
- Triple-quoted docstrings
- Include parameter descriptions in docstrings
- Examples in code are helpful but not required

### Signals and Events
- Use blinker library for signals
- Signal names: snake_case with underscores (e.g., `pre_engine_run`, `post_job_call`)
- Send signal payloads as kwargs

### Session Management
- Session is a `Dict[str, Any]` passed through job execution
- Store results in `session["results"]` list
- Each result: `{"job": "job_name", "return": result}`

### File Organization
- `sauron/` - Main package
- `sauron/engine.py` - Core engine
- `sauron/models.py` - Pydantic models
- `sauron/parsers.py` - Rule parsers
- `sauron/exporters.py` - Metadata exporters
- `sauron/rule_engine.py` - Rule engine specialization
- `tests/` - Test suite

### Dependencies
- Pydantic v2.x for data validation
- ruamel.yaml for YAML/JSON parsing (supports YAML 1.2)
- blinker for signals/events
- poethepoet for task running
- Python 3.10+ support
