# Development Guide

## Project Structure

```
ltspice_to_svg/
├── src/
│   ├── parsers/
│   │   ├── asc_parser.py
│   │   ├── asy_parser.py
│   │   ├── schematic_parser.py
│   │   └── shape_parser.py
│   ├── renderers/
│   │   ├── base_renderer.py
│   │   ├── flag_renderer.py
│   │   ├── shape_renderer.py
│   │   ├── symbol_renderer.py
│   │   ├── svg_renderer.py
│   │   ├── text_renderer.py
│   │   └── wire_renderer.py
│   └── ltspice_to_svg.py
├── tests/
│   └── ...
├── tools/
│   └── fix_encoding.py
└── doc/
    ├── architecture.md
    ├── api.md
    ├── user_guide.md
    └── development.md
```

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Coding Standards

### Python Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Document all public functions and classes with docstrings
- Keep functions focused and single-purpose
- Use meaningful variable and function names

### Documentation

- Update documentation when making changes
- Include examples in docstrings
- Document any breaking changes
- Keep the architecture document up to date

### Testing

- Write tests for all new features
- Maintain test coverage above 90%
- Use pytest fixtures for test setup
- Group related tests in classes
- Use descriptive test names

## Adding New Features

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Implement the feature:
   - Add new parser/renderer if needed
   - Update existing code
   - Add tests
   - Update documentation

3. Run tests:
```bash
pytest
```

4. Check code style:
```bash
flake8
mypy .
```

5. Create a pull request

## Debugging

### Common Debugging Tools

1. **JSON Export**
   - Use `--export-json` to inspect intermediate data
   - Check the generated JSON files in the `output` directory

2. **Logging**
   - Use the built-in logging system
   - Set log level to DEBUG for detailed information

3. **Test Cases**
   - Create minimal test cases to reproduce issues
   - Use pytest's debugging features

### Debugging Tips

1. **Symbol Issues**
   - Check symbol file encoding
   - Verify pin definitions
   - Inspect symbol rendering order

2. **Text Rendering**
   - Check text positioning calculations
   - Verify font settings
   - Inspect text transformation matrices

3. **Performance**
   - Profile code with cProfile
   - Check for unnecessary object creation
   - Optimize rendering loops

## Release Process

1. Update version number
2. Update changelog
3. Run all tests
4. Create release tag
5. Build and upload to PyPI

## Contributing Guidelines

1. **Pull Requests**
   - Create feature branches
   - Include tests
   - Update documentation
   - Follow coding standards

2. **Issues**
   - Use the issue template
   - Provide reproduction steps
   - Include relevant files

3. **Code Review**
   - Review code for style and functionality
   - Check test coverage
   - Verify documentation updates

## Maintenance

### Regular Tasks

1. **Dependencies**
   - Update dependencies regularly
   - Check for security vulnerabilities
   - Test with new dependency versions

2. **Documentation**
   - Review and update documentation
   - Add new examples
   - Update troubleshooting guides

3. **Testing**
   - Run full test suite
   - Update test cases
   - Check coverage reports

### Performance Optimization

1. **Profiling**
   - Profile code regularly
   - Identify bottlenecks
   - Optimize critical paths

2. **Memory Usage**
   - Monitor memory usage
   - Optimize data structures
   - Clean up resources

3. **Rendering**
   - Optimize SVG generation
   - Reduce unnecessary operations
   - Cache expensive calculations 