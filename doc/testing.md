# Testing Strategy

This document outlines the testing strategy and coverage for the LTspice to SVG converter.

## Test Structure

The test suite is organized into several categories, each focusing on specific components or features:

```
tests/
├── test_schematic_shapes/    # Shape parsing and rendering tests
├── test_asc_parser/         # ASC file parsing tests
├── test_symbol_finding/     # Symbol resolution tests
├── test_flags/             # Flag and IO pin tests
├── test_schematic_texts/    # Schematic text rendering tests
└── test_symbol_texts/      # Symbol text rendering tests
```

## Test Categories

### 1. Shape Testing (`test_schematic_shapes/`)
- Tests parsing and rendering of basic shapes:
  - Wires and connections
  - Lines with different styles
  - Rectangles
  - Circles
  - Arcs
- Coverage includes:
  - Shape coordinate parsing
  - Style attribute handling
  - SVG element generation
  - Visual verification

### 2. Flag and IO Pin Testing (`test_flags/`)
- Tests flag and IO pin functionality:
  - Ground flags
  - IO pins (input, output, bidirectional)
  - Net labels
  - Pin orientations
- Coverage includes:
  - Pin type detection
  - Orientation calculation
  - Text placement
  - Connection handling

### 3. Text Testing
- Schematic Text (`test_schematic_texts/`)
  - Net labels
  - Component values
  - Comments
- Symbol Text (`test_symbol_texts/`)
  - Pin labels
  - Component names
  - WINDOW attributes

### 4. Parser Testing (`test_asc_parser/`)
- Tests ASC file parsing:
  - File format validation
  - Element extraction
  - Data structure generation
- Coverage includes:
  - Error handling
  - Edge cases
  - Format variations

### 5. Symbol Testing (`test_symbol_finding/`)
- Tests symbol resolution:
  - Library path handling
  - Symbol file loading
  - Symbol inheritance
- Coverage includes:
  - Path resolution
  - File loading
  - Symbol caching

## Test Data

Each test category includes:
- Test input files (.asc, .asy)
- Expected output files (.svg)
- Debug data (.json)
- Test scripts

Example test data structure:
```
test_category/
├── test_case.asc          # Input schematic
├── test_case.svg          # Expected output
├── test_case_parsed.json  # Parsed data
├── test_case_debug.json   # Debug information
└── test_case.py           # Test script
```

## Test Coverage

### 1. Unit Tests
- Individual component testing
- Pure function verification
- Data structure validation
- Error handling

### 2. Integration Tests
- Component interaction testing
- Data flow verification
- End-to-end processing
- File I/O operations

### 3. Visual Tests
- SVG output verification
- Element positioning
- Style application
- Text rendering

## Test Execution

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test category
python -m pytest tests/test_schematic_shapes/

# Run with coverage report
python -m pytest --cov=src tests/
```

### Test Output
- SVG files for visual verification
- JSON files for data validation
- Coverage reports
- Debug information

## Test Maintenance

### Adding New Tests
1. Create test data directory
2. Add input files (.asc, .asy)
3. Create expected output (.svg)
4. Write test script
5. Add debug data export

### Updating Tests
1. Modify test data as needed
2. Update expected output
3. Verify test coverage
4. Update documentation

## Continuous Integration

### Automated Testing
- Run on every commit
- Generate coverage reports
- Verify SVG output
- Check for regressions

### Test Requirements
- Maintain >80% code coverage
- All tests must pass
- No regressions in visual output
- Debug data must be valid

## Future Improvements

### Planned Test Enhancements
1. Visual Regression Testing
   - Compare SVG outputs
   - Detect visual changes
   - Generate diff reports

2. Performance Testing
   - Large schematic handling
   - Memory usage
   - Processing speed

3. Edge Cases
   - Complex symbols
   - Nested components
   - Special characters

4. Error Cases
   - Invalid files
   - Missing symbols
   - Format errors 