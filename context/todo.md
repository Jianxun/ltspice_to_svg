# Todo List

## Current Tasks

### [ ] Implement Rendering Configuration
- [ ] Create RenderingConfig class
  - [ ] Implement initialization with defaults
  - [ ] Add methods for getting/setting options
  - [ ] Add validation for option types
- [ ] Update SVGRenderer to use configuration
  - [ ] Implement `set_text_rendering_options()` method
  - [ ] Update render methods to use config
  - [ ] Ensure backward compatibility
- [ ] Update BaseRenderer to accept config parameter
- [ ] Connect command line options to config in main module
- [ ] Add unit tests for configuration class
- [ ] Fix failing test in `test_text_rendering_options`

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
