# Contributing to ltspice_to_svg

Thank you for your interest in contributing to ltspice_to_svg! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Documentation](#documentation)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to jianxun.zhu@gmail.com.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ltspice_to_svg.git
   cd ltspice_to_svg
   ```

## Development Environment

### Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the project in development mode:
   ```bash
   pip install -e .
   pip install -r requirements.txt
   ```

3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov
   ```

### Project Structure

```
ltspice_to_svg/
├── src/                    # Source code
│   ├── ltspice_to_svg.py  # Main entry point
│   ├── parsers/           # ASC/ASY file parsers
│   ├── renderers/         # SVG rendering components
│   └── utils/             # Utility functions
├── tests/                 # Test suite
│   ├── unit_tests/        # Unit tests
│   └── integration/       # Integration tests
├── schematics/           # Example LTspice files
└── docs/                 # Documentation
```

## Making Changes

### Development Workflow

1. Create a new branch for your feature/bugfix:
   ```bash
   git checkout -b feature-name
   ```

2. Make your changes following the code style guidelines

3. Add or update tests as necessary

4. Run the test suite to ensure nothing is broken

5. Update documentation if needed

6. Commit your changes with a descriptive message

### Commit Messages

Use clear, descriptive commit messages:

- Start with a capitalized verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 72 characters
- Include more details in the body if necessary

Examples:
```
Add support for custom stroke widths in wire rendering

Fix symbol rotation bug for M90 and M270 orientations

Update documentation for new CLI options
```

## Testing

### Running Tests

Run the full test suite:
```bash
pytest
```

Run specific test categories:
```bash
# Unit tests only
pytest tests/unit_tests/

# Integration tests only  
pytest tests/integration/

# Specific test file
pytest tests/unit_tests/test_rendering_config.py
```

Run tests with coverage:
```bash
pytest --cov=src --cov-report=html
```

### Writing Tests

- Write tests for new functionality
- Update existing tests when modifying behavior
- Use descriptive test names that explain what is being tested
- Include both positive and negative test cases
- Place test files in appropriate directories (unit_tests/ or integration/)

### Test Structure

Unit tests should test individual components in isolation:
```python
def test_rendering_config_default_values():
    config = RenderingConfig()
    assert config.get_option('base_font_size') == 12
```

Integration tests should test complete workflows:
```python
def test_complete_schematic_conversion():
    # Test full ASC -> SVG conversion pipeline
    pass
```

## Submitting Changes

### Pull Request Process

1. Ensure your branch is up to date with main:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. Push your branch to your fork:
   ```bash
   git push origin your-branch
   ```

3. Create a Pull Request on GitHub with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Reference to any related issues
   - Screenshots for UI changes (if applicable)

### Pull Request Checklist

- [ ] Code follows the project's style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated if necessary
- [ ] CHANGELOG.md updated for significant changes
- [ ] Commit messages are clear and descriptive

## Code Style

### Python Style

- Follow PEP 8 conventions
- Use meaningful variable and function names
- Keep functions focused and reasonably sized
- Add docstrings to classes and public methods
- Use type hints where helpful

### Example Function:

```python
def calculate_symbol_bounds(shapes: List[Shape]) -> Tuple[float, float, float, float]:
    """Calculate the bounding box of a collection of shapes.
    
    Args:
        shapes: List of shape objects to calculate bounds for
        
    Returns:
        Tuple of (min_x, min_y, max_x, max_y) coordinates
        
    Raises:
        ValueError: If shapes list is empty
    """
    if not shapes:
        raise ValueError("Cannot calculate bounds of empty shape list")
    
    # Implementation here...
```

### Import Organization

Organize imports in this order:
1. Standard library imports
2. Third-party imports  
3. Local application imports

```python
import sys
from pathlib import Path

import svgwrite

from .parsers import AscParser
from .utils import logger
```

## Documentation

### Code Documentation

- Add docstrings to all public classes and methods
- Include type hints for function parameters and return values
- Document complex algorithms and business logic
- Keep comments focused on "why" rather than "what"

### User Documentation

- Update README.md for new features
- Add examples for new command-line options
- Update docs/ files for architectural changes
- Include code examples in documentation

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- Python version and operating system
- ltspice_to_svg version
- Complete error message and stack trace
- Minimal example to reproduce the issue
- Expected vs actual behavior

### Feature Requests

When requesting features:

- Explain the use case and motivation
- Describe the desired behavior
- Consider backward compatibility
- Discuss alternative approaches if applicable

### Security Issues

For security vulnerabilities, please follow our [Security Policy](SECURITY.md) and report privately to jianxun.zhu@gmail.com.

## Development Resources

### Useful Commands

```bash
# Run specific test with verbose output
pytest -v tests/unit_tests/test_rendering_config.py

# Run tests with coverage and open HTML report
pytest --cov=src --cov-report=html && open htmlcov/index.html

# Format code (if using black)
black src/ tests/

# Check types (if using mypy)
mypy src/
```

### Understanding the Codebase

Key concepts to understand:

1. **Parsers**: Convert LTspice files to Python objects
2. **Renderers**: Convert Python objects to SVG elements
3. **Configuration**: Centralized settings management
4. **Testing**: Unit tests for components, integration tests for workflows

### Getting Help

- Check existing documentation in docs/
- Look at similar implementations in the codebase
- Ask questions in GitHub issues or discussions
- Review the project's architecture documentation

## Recognition

Contributors will be recognized in:

- CHANGELOG.md for significant contributions
- GitHub contributors page
- Release notes for major features

Thank you for contributing to ltspice_to_svg!