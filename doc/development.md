# Development Guide

This document provides guidelines for contributing to the LTspice to SVG converter project.

## Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ltspice_to_svg.git
cd ltspice_to_svg
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black mypy
```

## Development Guidelines

### 1. Modularity
- Each renderer has a single responsibility
- Pure functions with explicit parameters
- Minimal dependencies between components

### 2. Configuration
- Centralize configuration in SVGGenerator
- Pass configuration explicitly to renderers
- Avoid hardcoded values

### 3. Debug Support
- Include debug logging where appropriate
- Export debug data for troubleshooting
- Maintain clear error messages

### 4. Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document public interfaces
- Keep functions focused and small

### 5. File Handling

#### LTspice File Encoding

When working with LTspice files (.asc and .asy):
1. Always use proper encoding handling (UTF-16LE without BOM for special characters)
2. Never modify files directly unless explicitly requested
3. If a file becomes corrupted, use the normalization tool:
   ```bash
   ./tools/normalize_encoding.py <file_path>
   ```

The normalization tool will:
- Create backups before making changes
- Only modify files that need normalization
- Provide clear feedback about actions taken

Common scenarios requiring normalization:
- Files that can't be opened in LTspice
- Files with special characters in ASCII format
- Files corrupted by different text editors
- Files copied from different systems

## Development Workflow

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following these guidelines:
   - Use type hints for all function parameters and return values
   - Add docstrings for all functions and classes
   - Follow PEP 8 style guidelines
   - Keep functions focused and modular
   - Add appropriate error handling

3. Run tests:
```bash
python -m pytest tests/
```

4. Format your code:
```bash
black src/ tests/
```

5. Run type checking:
```bash
mypy src/
```

6. Submit a pull request with:
   - Clear description of changes
   - Any new dependencies added
   - Test coverage for new features
   - Documentation updates if needed

## Testing Guidelines

### Test Coverage
- Write unit tests for all new functionality
- Use pytest fixtures for common test setup
- Test edge cases and error conditions
- Maintain test coverage above 80%

### Test Cases
Test with various LTspice files:
- Different symbol types
- Various rotations and mirrors
- Complex wire connections
- Different text alignments and sizes

## Documentation

### Required Updates
- Update README.md for user-facing changes
- Update architecture.md for implementation changes
- Document any new command-line options
- Add comments for complex algorithms
- Include examples for new features

### Documentation Structure
```
doc/
├── README.md           # High-level overview
├── development.md      # Development guidelines
├── architecture.md     # Detailed architecture
├── implementation.md   # Implementation details
└── lessons.md         # Project-specific lessons
```

## Future Improvements

### 1. Performance
- Optimize rendering for large schematics
- Implement caching where beneficial
- Profile and optimize critical paths

### 2. Features
- Add support for more LTspice elements
- Improve text rendering quality
- Enhance symbol handling

### 3. Testing
- Add unit tests for each component
- Implement integration tests
- Add visual regression tests

### 4. Documentation
- Add API documentation
- Create usage examples
- Document common issues and solutions

### 5. Export Options
- PNG export with configurable DPI
- Dark mode support
- Custom color schemes

### 6. Integration
- Web interface
- Batch processing
- Integration with other EDA tools 