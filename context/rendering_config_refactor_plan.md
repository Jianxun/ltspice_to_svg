# Rendering Configuration Refactoring Plan

## Overview
This document outlines the plan for implementing a dedicated configuration class to manage rendering options in the LTSpice to SVG converter. This refactoring will separate configuration management from rendering logic, providing a cleaner separation of concerns and a more maintainable codebase.

## New Class
1. **RenderingConfig**
   - Will store all rendering options
   - Will provide initialization with default values
   - Will include validation methods for option types
   - Will serve as a single source of truth for all configuration options

## Affected Classes and Methods

### SVGRenderer
- **`__init__`**: Need to accept configuration object or create default
- **`set_stroke_width`**: Should update config and propagate
- **`set_base_font_size`**: Should update config and propagate
- **`set_text_rendering_option`**: Should update config
- **`set_text_rendering_options`**: New method to update multiple text options
- **`render_texts`**: Should read from config instead of instance variables
- **`render_symbols`**: Should pass config to symbol renderer
- All other render methods that might use configuration values

### BaseRenderer
- **`__init__`**: Should accept config parameter
- Properties like `stroke_width` and `base_font_size` should reference config

### Other Renderers 
(SymbolRenderer, TextRenderer, ShapeRenderer, FlagRenderer, WireRenderer)
- Each would need to access the config object instead of individual properties
- Methods that use configuration values should be updated

### Main Module (ltspice_to_svg.py)
- **`main`**: Should create configuration object from command-line arguments
- Should pass the config to SVGRenderer instead of calling individual setters

### Tests
- **`test_text_rendering_options`**: Already expects `set_text_rendering_options` method
- Other tests that set renderer properties directly would need updating
- New tests for RenderingConfig class would be needed

## Specific Methods to Implement or Modify

### In RenderingConfig:
```python
__init__(self, **kwargs)  # Initialize with defaults and overrides
set_text_options(self, **kwargs)  # Set multiple text options
set_option(self, name, value)  # Set any option
get_option(self, name, default=None)  # Get any option
```

### In SVGRenderer:
```python
__init__(self, config=None)  # Accept config or create default
get_config(self)  # Return current config
set_config(self, config)  # Replace config
set_text_rendering_options(self, **kwargs)  # Update text options
```

### In BaseRenderer:
```python
__init__(self, dwg, config=None)  # Accept config parameter
```

### In ltspice_to_svg.py:
```python
create_config_from_args(args)  # Helper to create config from arguments
```

## Implementation Strategy

1. **Short-term**: Implement a minimal `set_text_rendering_options` method in SVGRenderer to fix the failing test
2. **Medium-term**: Create the RenderingConfig class and update SVGRenderer to use it
3. **Long-term**: Refactor all renderers to use the configuration object

## Benefits

1. **Separation of concerns**: Configuration management separated from rendering logic
2. **Maintainability**: Easier to add new configuration options
3. **Consistency**: Ensures consistent configuration across all renderers
4. **Testability**: Makes it easier to test configuration independently
5. **Flexibility**: Allows for serialization/deserialization of configuration

## Potential Challenges

1. **Backward compatibility**: Need to ensure existing interfaces continue to work
2. **Test updates**: Will need to update numerous tests to use the new approach
3. **Propagation of changes**: Ensuring all renderers use the configuration correctly 