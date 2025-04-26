# To-Do List

## Current Tasks

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

## Current Tasks

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
- [ ] Add high-level architecture documentation
- [ ] Document renderer relationships and responsibilities
- [ ] Add examples for common use cases

### [ ] Performance Optimization
- [ ] Identify bottlenecks in rendering process
- [ ] Consider caching symbol definitions
- [ ] Optimize viewbox calculation for large schematics

### [ ] Additional Features
- [ ] Add support for LTspice netlist export
- [ ] Implement interactive SVG features (hover, click)
- [ ] Add support for component highlighting
