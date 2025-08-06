# To-Do List

## Current Tasks

### [X] Version 0.2.0 Release Preparation
- [X] Fix critical symbol rotation bugs (M90, M270 orientations)
- [X] Add CLI version command support
- [X] Enhance SVG output with metadata and pretty formatting
- [X] Create comprehensive CHANGELOG.md
- [X] Update version to 0.2.0 and status to Beta
- [X] Build and test distribution packages
- [X] Include CHANGELOG.md in package distribution

### [X] Python Release Best Practices Implementation ✅ **COMPLETED v0.2.0**
**Goal**: Implement missing Python release best practices to improve project maintainability and professionalism.

#### Release Automation ✅ **COMPLETED**
- [X] Create git tags for version releases
  - [X] Tag v0.2.0 release
  - [X] Set up semantic versioning tag format
- [X] Set up GitHub Actions workflows
  - [X] Configure PyPI trusted publishing with OIDC authentication
  - [X] Create automated build and publish pipeline
  - [X] Remove CI testing (Linux/LTspice compatibility issues)
- [X] Implement automated PyPI publishing
  - [X] Set up GitHub Actions workflow for PyPI publishing
  - [X] Configure automated publishing on tag creation
  - [X] Add PyPI trusted publishing configuration

#### Project Governance ✅ **COMPLETED**
- [X] Create SECURITY.md
  - [X] Document vulnerability reporting process
  - [X] Add security contact information
  - [X] Define supported versions policy
- [X] Create CONTRIBUTING.md
  - [X] Document development environment setup
  - [X] Add code style guidelines
  - [X] Explain testing procedures and PR process
- [X] Create publishing documentation
  - [X] Document PyPI trusted publishing setup
  - [X] Add GitHub environment configuration instructions
  - [X] Create comprehensive release process guide

#### Remaining Items for Future
- [ ] Add CODE_OF_CONDUCT.md
  - [ ] Use standard Contributor Covenant
  - [ ] Adapt for project-specific needs
- [ ] Create GitHub templates
  - [ ] Issue templates for bug reports and feature requests
  - [ ] Pull request template with checklist

### [X] Enhanced Encoding Support ✅ **COMPLETED v0.2.0**
- [X] Improve encoding detection for ASC and ASY parsers
  - [X] Add support for UTF-8, UTF-16LE, ASCII, and latin1 encodings
  - [X] Reorder encoding priority for better detection
  - [X] Fix issue with µ (micro) symbol in component values
  - [X] Reduce debug noise by showing errors only when all encodings fail
- [X] Test encoding improvements
  - [X] Verify µ character handling in test files
  - [X] Confirm encoding detection works silently
  - [X] Test with various file encodings

#### Code Quality Improvements ⚠️ **FUTURE**
- [ ] Set up pre-commit hooks
  - [ ] Add code formatting (black, isort)
  - [ ] Add linting (flake8, pylint)
  - [ ] Add type checking (mypy)
- [ ] Configure Dependabot
  - [ ] Set up automated dependency updates
  - [ ] Configure update frequency and scope
- [ ] Implement single-source version management
  - [ ] Move version to __init__.py or _version.py
  - [ ] Update setup.py to read version dynamically
  - [ ] Update CLI module to import version

### [ ] NetlistSVG Compatibility Sprint 
**Goal**: Adapt SVG output format to be compatible with netlistsvg skin definition format for better interoperability and more concise, readable output.

#### Phase 1: CSS Classes Implementation ✅ **PRIORITY**
- [ ] Design CSS class taxonomy for different element types
  - [ ] Define classes for: `.symbol`, `.wire`, `.text`, `.flag`, `.shape`, `.connect`, `.detail`
  - [ ] Research netlistsvg's class naming conventions for alignment
  - [ ] Create comprehensive CSS class mapping for all our element types
- [ ] Add CSS `<style>` block to SVG header
  - [ ] Modify `SVGRenderer.create_drawing()` to include style definitions
  - [ ] Define global styles matching our current inline style patterns
  - [ ] Ensure styles are compatible with existing test expectations
- [ ] Refactor renderers to use CSS classes
  - [ ] Update `WireRenderer` to use classes instead of inline styles
  - [ ] Update `ShapeRenderer` to use classes instead of inline styles  
  - [ ] Update `SymbolRenderer` to use classes instead of inline styles
  - [ ] Update `TextRenderer` to use classes instead of inline styles
  - [ ] Update `FlagRenderer` to use classes instead of inline styles
- [ ] Test CSS class implementation
  - [ ] Run existing integration tests to ensure visual compatibility
  - [ ] Verify file size reduction from removing repeated inline styles
  - [ ] Check SVG readability improvement in generated files

#### Phase 2: Port Metadata Enhancement ✅ **IMPLEMENT**  
- [ ] Extract port information from parsed .asy symbols
  - [ ] Review current symbol parsing code for pin/port data availability
  - [ ] Identify which port information is already parsed vs needs extraction
  - [ ] Map LTspice pin definitions to netlistsvg port format
- [ ] Add port definition generation to symbol renderer
  - [ ] Modify `SymbolRenderer.begin_symbol()` to accept port data
  - [ ] Generate invisible `<g>` elements for each port with required attributes
  - [ ] Calculate port positions relative to symbol bounds
  - [ ] Determine appropriate `s:position` values ("left", "right", "top", "bottom")
- [ ] Update symbol rendering pipeline
  - [ ] Modify `SVGRenderer.render_symbols()` to pass port data to renderer  
  - [ ] Ensure port definitions are included in symbol groups
  - [ ] Test port metadata generation with different symbol types
- [ ] Validate port metadata implementation
  - [ ] Test with various symbol types (nmos, pmos, resistor, capacitor, etc.)
  - [ ] Verify port coordinates are accurate within symbol bounds
  - [ ] Check that port identifiers match expected values

#### Phase 3: Dynamic Attributes (Optional) ⚠️ **FUTURE**
- [ ] Add `s:attribute` support for component values  
  - [ ] Identify which text elements should have dynamic attributes
  - [ ] Add `s:attribute="value"` to component value text elements
  - [ ] Add `s:attribute="ref"` to reference designator text elements
- [ ] Extract component parameters from .asc files
  - [ ] Review parsed schematic data for component parameters
  - [ ] Map component attributes to appropriate s:attribute values
- [ ] Ensure standalone viewability
  - [ ] Verify text displays literal values when viewed outside netlistsvg
  - [ ] Test that SVG files remain standalone viewable

#### Testing and Validation
- [ ] Create comprehensive test suite for netlistsvg compatibility
  - [ ] Test CSS class generation and application
  - [ ] Test port metadata accuracy and completeness
  - [ ] Test dynamic attribute implementation (if implemented)
- [ ] Validate compatibility with netlistsvg tools
  - [ ] Test generated SVGs as potential skin components  
  - [ ] Verify namespace and attribute compatibility
  - [ ] Check for any validation issues with netlistsvg

#### Documentation Updates
- [ ] Update README with new output format features
- [ ] Document CSS class usage and customization options
- [ ] Add examples of netlistsvg compatibility features
- [ ] Update API documentation for new renderer methods

### [X] Enhance SVG Output with Symbol Metadata and Pretty Formatting
- [X] Add pretty formatting to SVG output 
  - [X] Research svgwrite's pretty printing capabilities
  - [X] Implement `save(pretty=True)` parameter for readable SVG output
  - [X] Test with actual schematic conversion
- [X] Add custom namespace support for symbol metadata
  - [X] Add `xmlns:s="https://github.com/nturley/netlistsvg"` namespace
  - [X] Disable svgwrite validation for custom attributes (set `debug=False`)
- [X] Add symbol type attributes to groups
  - [X] Modify `begin_symbol()` to accept symbol name parameter
  - [X] Add `s:type` attribute with actual symbol names
  - [X] Update SVGRenderer to pass symbol names to SymbolRenderer
- [X] Add symbol dimension attributes
  - [X] Create method to calculate symbol dimensions from shapes
  - [X] Add `s:width` and `s:height` attributes with calculated values
  - [X] Handle all shape types (lines, rectangles, circles, arcs) in dimension calculation
- [X] Fix viewbox calculation bug
  - [X] Identified missing symbol inclusion in ViewboxCalculator
  - [X] Added `_include_symbols()` method to process symbol positions
  - [X] Updated `calculate()` method to include symbols in bounds calculation

### [X] Add viewbox margin and font option to rendering options
- [X] Create a feature branch for rendering control options
- [X] Add margin option to `RenderingConfig`
- [X] Update `ViewboxCalculator` to utilize the margin
- [X] Add margin parameter to command-line interface
- [X] Write tests for the new margin feature
- [X] Fix validation logic in `RenderingConfig` to allow zero margin
- [X] Fix `ViewboxCalculator` to handle cases where bounds are invalid
- [X] Update tests to account for minimum height adjustment

### [X] Add font option to rendering options
- [X] Research font handling in SVG
- [X] Add font option to `RenderingConfig`
- [X] Update text rendering to use the configured font
- [X] Add font parameter to command-line interface
- [X] Write tests for the new font feature

## Completed Tasks

### [X] Implement improved text rendering for symbols
- [X] Fix text mirroring in symbols
- [X] Implement proper text alignment for symbol pins
- [X] Add support for component name and value text rendering

### [X] Create robust SVG output
- [X] Add proper SVG header and namespace declarations
- [X] Implement CSS styling for consistent appearance
- [X] Add metadata to SVG file

### [X] Fix encoding handling for LTspice files
- [X] Create utility to detect and fix file encoding
- [X] Update parser to handle different encodings
- [X] Add documentation for encoding issues

### [X] Enhance CLI with more rendering options
- [X] Add stroke width option for wires
- [X] Add dot size for junctions
- [X] Add base font size control
- [X] Implement text rendering control switches

[X] Examine the SVG renderer class to understand how it manages text rendering options
  - [X] Review `SVGRenderer.render_texts()` method to see text rendering controls
  - [X] Analyze `TextRenderer` class to understand text styling and positioning
  - [X] Examine how text rendering options are applied
  - [X] Understand the text rendering hierarchy (SVGRenderer -> TextRenderer)
  - [X] Document findings in memory.md

[X] Examine window text rendering in integration tests
  - [X] Understand how symbol window texts are rendered 
  - [X] Analyze the test case for window text rendering
  - [X] Examine how property values are displayed in symbols
  - [X] Document findings in memory.md

## Completed Tasks

[X] Debug and fix the failing test related to text rendering
  - [X] Run the failing test to reproduce the issue
  - [X] Identify the specific text rendering option causing the test failure
  - [X] Investigate any discrepancy between configuration settings and rendering behavior
  - [X] Fix the issue in the renderer code
  - [X] Verify the fix with the test
  - [X] Update documentation to reflect the fix

[X] Fix window text rendering in tests
  - [X] Identify the issue with window text property rendering
  - [X] Update tests to use the new configuration API
  - [X] Rename tests to better reflect their purpose
  - [X] Fix test assertions to work with updated renderer
  - [X] Verify all tests pass

[X] Create a shell script for running the tool directly
  - [X] Fix import issues in the ltspice_to_svg.py script
  - [X] Create a shell script wrapper
  - [X] Update README.md with correct usage instructions
  - [X] Create setup.py for installation as package
  - [X] Test the tool with example schematic

[X] Set up the project structure
  - [X] Create the virtual environment
  - [X] Set up the directory structure
  - [X] Initialize git repository
  - [X] Create initial README.md
  - [X] Create .gitignore file

### [X] Replace direct property access with config.get_option() calls
- [X] Update test_text_rendering_switches.py to use config interface
  - [X] Replace direct property assignment with config.set_option() calls
  - [X] Run tests to verify functionality
- [X] Update other test files that use text rendering options
  - [X] Identify all test files using direct property access
  - [X] Modify to use config interface
  - [X] Run tests after each modification
- [X] Remove property getters/setters from SVGRenderer
  - [X] Ensure all internal references use self.config.get_option()
  - [X] Run tests to verify functionality
- [X] Update symbol window text tests 
  - [X] Fix window text tests to use new config API
  - [X] Rename tests to be more descriptive
- [X] Document API changes

### [ ] Implement Rendering Configuration
- [X] Create RenderingConfig class
  - [X] Implement initialization with defaults
  - [X] Add methods for getting/setting options
  - [X] Add validation for option types
- [X] Update SVGRenderer to use configuration
  - [X] Implement `set_text_rendering_options()` method
  - [X] Update render methods to use config
  - [X] Ensure backward compatibility
- [ ] Update BaseRenderer to accept config parameter
- [ ] Connect command line options to config in main module
- [ ] Add unit tests for configuration class
- [X] Fix failing test in `test_text_rendering_options`

### [X] Refactor SVG Renderer
- [X] Extract viewbox calculation to separate class
- [X] Update code organization and method signatures
- [X] Update documentation and tests

### [X] Update Flag Rendering
- [X] Consolidate flag data structures
- [X] Implement unified flag rendering approach
- [X] Fix orientation handling for text elements

### [X] Improve Text Rendering
- [X] Simplify type checking for text elements
- [X] Enhance logging with type-specific details
- [X] Document text element structure and handling

### [X] Replace direct property access with config.get_option() calls
- [X] Update SVGRenderer properties to use config.get_option()
- [X] Modify tests to use the new config interface
- [X] Ensure backward compatibility with existing API

### [X] Fix TypeError in command line tests
- [X] Debug the issue with MagicMock in FlagRenderer._load_flag_definitions
- [X] Refine the mock_open_file fixture to handle JSON file reading properly
- [X] Update the test to mock the JSON loading process instead of the file open operation
- [X] Ensure all other tests continue to pass after the fix

### [X] Add --no-net-label option
- [X] Add command line flag to disable rendering of net label flags
- [X] Update RenderingConfig to support the new option
- [X] Modify SVGRenderer.render_flags to check for the option
- [X] Add tests to verify the functionality
- [X] Run all tests to ensure no regressions

### [X] Update CLI definition notes
- [X] Document the new --no-net-label option in memory.md
- [X] Ensure all CLI options are properly documented
- [X] Add clear descriptions for each option category
- [X] Include usage examples for common scenarios

### [X] Add --no-pin-name option
- [X] Add command line flag to disable rendering of I/O pin text
- [X] Update RenderingConfig to support the new option
- [X] Modify FlagRenderer.render_io_pin to check for the option
- [X] Update SVGRenderer to track skipped I/O pin text
- [X] Add tests to verify the functionality
- [X] Update CLI documentation in memory.md
- [X] Run all tests to ensure no regressions

### [X] Fix --no-text option behavior
- [X] Update the main script to make --no-text set all other text-related options
- [X] Fix the test to verify this behavior
- [X] Update the help text and documentation to clarify this option is a master switch
- [X] Run tests to ensure no regressions

### [X] Fix bug with --no-text option in main script
- [X] Debug the failing test_no_text test in command line tests
- [X] Modify the main script to skip render_texts() call when --no-text is enabled
- [X] Ensure the text rendering options are still properly set
- [X] Run tests to verify the fix works
- [X] Commit the changes with a descriptive message
- [X] Update memory.md to document the fix

### [X] Remove deprecated --scale option
- [X] Remove the --scale argument from the command line parser
- [X] Remove the deprecation warning code
- [X] Remove the warnings import since it's no longer needed
- [X] Delete the test_scale_deprecation_warning test
- [X] Update documentation to remove references to the scale option
- [X] Run tests to verify no regressions

### [X] Update README.md with latest command line options
- [X] Remove references to deprecated --scale option
- [X] Add new --no-net-label and --no-pin-name options
- [X] Update the description of --no-text to mention it's a master switch
- [X] Fix stroke-width default value to match the code
- [X] Update examples with relevant use cases
- [X] Organize examples by common usage patterns

### [X] Publish package to PyPI Test
- [X] Update package metadata in setup.py
- [X] Create pyproject.toml for modern Python packaging
- [X] Create MANIFEST.in for non-Python files
- [X] Build distribution packages
- [X] Register on PyPI Test website
- [X] Configure PyPI credentials
- [X] Upload to PyPI Test
- [X] Test installation from PyPI Test
- [X] Document the publishing process

### [X] Enable GitHub pip installation
- [X] Update setup.py for proper package discovery
- [X] Create installation documentation
- [X] Update README with GitHub installation instructions
- [X] Test pip installation directly from GitHub

## Next Steps

### [ ] Extend Configuration Refactoring
- [ ] Update all specialized renderers to use config object
- [ ] Create serialization/deserialization for config
- [ ] Add more configuration options as needed

### [ ] Clean up old code
- [ ] Remove deprecated methods and parameters
- [ ] Consider removing old `net_label_renderer.py` (check for dependencies)
- [ ] Consolidate redundant code in text rendering

### [ ] Improve Documentation
- [X] Review and update existing documentation for accuracy and completeness
  - [X] Audit all documentation files for outdated information
  - [X] Ensure command line options match current implementation
  - [X] Update code examples to reflect current API
- [X] Enhance architecture documentation
  - [X] Create diagrams showing component relationships
  - [X] Document data flow through the system
  - [X] Explain design decisions and patterns
- [X] Improve renderer documentation
  - [X] Document renderer hierarchy and inheritance
  - [X] Explain how renderers interact with configuration
  - [X] Add visual examples of renderer output
- [X] Create comprehensive user guide
  - [X] Add step-by-step tutorials for common use cases
  - [X] Include before/after examples with command line options
  - [X] Document advanced usage patterns
- [ ] Create contributor guide
  - [ ] Document development environment setup process
  - [ ] Add code style guidelines
  - [ ] Explain testing procedures and requirements
- [X] Add inline code documentation
  - [X] Review and improve docstrings
  - [X] Add type annotations where missing
  - [X] Document complex algorithms and logic

### [ ] Performance Optimization
- [ ] Identify bottlenecks in rendering process
- [ ] Consider caching symbol definitions
- [ ] Optimize viewbox calculation for large schematics

### [ ] Additional Features
- [ ] Add support for LTspice netlist export
- [ ] Implement interactive SVG features (hover, click)
- [ ] Add support for component highlighting
