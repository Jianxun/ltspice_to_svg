# SVGRenderer Refactor Plan

## Overview
This document outlines the plan to create a new SVGRenderer class that implements an explicit and cleaner interface for rendering schematic elements. This new class will coexist with the existing SVGGenerator class to allow for gradual migration.

## Current Issues
- Configuration parameters are mixed between different rendering types
- Rendering control is implicit through configuration flags
- Tight coupling between SVGGenerator and renderer classes
- Complex parameter passing through multiple layers
- Large rendering methods that are difficult to maintain

## New Design

### Modular Renderer Structure

#### Base Renderer
```python
# src/renderers/base_renderer.py
from abc import ABC, abstractmethod
import svgwrite

class BaseRenderer(ABC):
    def __init__(self, dwg: svgwrite.Drawing):
        self.dwg = dwg
        
    @abstractmethod
    def render(self, element: Dict) -> None:
        """Render a single element."""
        pass
```

#### Specialized Renderers
```python
# src/renderers/wire_renderer.py
class WireRenderer(BaseRenderer):
    def render(self, wire: Dict, stroke_width: float = 1.0) -> None:
        """Render a single wire."""
        pass
        
    def render_t_junction(self, x: float, y: float, dot_size: float) -> None:
        """Render a T-junction dot."""
        pass

# src/renderers/symbol_renderer.py
class SymbolRenderer(BaseRenderer):
    def render(self, symbol: Dict) -> None:
        """Render a single symbol."""
        pass

# src/renderers/text_renderer.py
class TextRenderer(BaseRenderer):
    def render(self, text: Dict, font_size: float = 22.0) -> None:
        """Render a single text element."""
        pass

# src/renderers/shape_renderer.py
class ShapeRenderer(BaseRenderer):
    def render(self, shape: Dict, stroke_width: float = 1.0) -> None:
        """Render a single shape."""
        pass
```

#### Main SVGRenderer Class
```python
# src/generators/svg_renderer.py
class SVGRenderer:
    def __init__(self):
        self.dwg = None
        self.schematic_data = None
        self.view_box = None
        self._renderers = {}
        
    def _initialize_renderers(self):
        """Initialize all renderers."""
        self._renderers = {
            'wire': WireRenderer(self.dwg),
            'symbol': SymbolRenderer(self.dwg),
            'text': TextRenderer(self.dwg),
            'shape': ShapeRenderer(self.dwg)
        }
        
    def load_schematic(self, schematic_data: Dict) -> None:
        self.schematic_data = schematic_data
        self.view_box = self._calculate_viewbox()
        
    def create_drawing(self, output_path: str) -> None:
        self.dwg = svgwrite.Drawing(output_path)
        self.dwg.viewbox(*self.view_box)
        self._initialize_renderers()
        
    def render_wires(self, stroke_width: float = 1.0, dot_size_multiplier: float = 0.75) -> None:
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        wire_renderer = self._renderers['wire']
        for wire in self.schematic_data.get('wires', []):
            wire_renderer.render(wire, stroke_width)
            
        # Add T-junction dots
        t_junctions = self._find_t_junctions(self.schematic_data['wires'])
        for x, y in t_junctions:
            wire_renderer.render_t_junction(x, y, stroke_width * dot_size_multiplier)
            
    def render_symbols(self) -> None:
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        symbol_renderer = self._renderers['symbol']
        for symbol in self.schematic_data.get('symbols', []):
            symbol_renderer.render(symbol)
            
    def render_texts(self, font_size: float = 22.0) -> None:
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        text_renderer = self._renderers['text']
        for text in self.schematic_data.get('texts', []):
            text_renderer.render(text, font_size)
            
    def render_shapes(self, stroke_width: float = 1.0) -> None:
        if not self.schematic_data or not self.dwg:
            raise ValueError("Schematic not loaded or drawing not created")
            
        shape_renderer = self._renderers['shape']
        for shape in self.schematic_data.get('shapes', []):
            shape_renderer.render(shape, stroke_width)
            
    def save(self) -> None:
        if not self.dwg:
            raise ValueError("Drawing not created")
        self.dwg.save()
```

### Key Changes
1. **Modular Design**
   - Each renderer type in its own file
   - Clear separation of concerns
   - Easy to maintain and modify individual renderers

2. **Explicit Rendering Control**
   - Each element type has its own render method
   - Rendering is controlled by method calls rather than configuration flags
   - Clear separation between different rendering operations

3. **Parameter Scoping**
   - Each render method only takes parameters relevant to its operation
   - No need to pass unused parameters
   - Clear which parameters affect which elements

4. **State Management**
   - Clear state transitions (load → create → render → save)
   - Methods check for required state before proceeding
   - Error messages are specific to the operation

5. **Usage Example**
```python
# Create renderer
renderer = SVGRenderer()

# Load schematic
renderer.load_schematic(schematic_data)

# Create drawing
renderer.create_drawing("output.svg")

# Render elements selectively
renderer.render_wires(stroke_width=1.0, dot_size_multiplier=0.75)
renderer.render_symbols()
renderer.render_texts(font_size=22.0)
renderer.render_shapes(stroke_width=1.0)

# Save the result
renderer.save()
```

## Logging System

### Simple Logging Configuration
```python
# src/utils/logger.py
import logging
import os

def setup_logging(log_file: str = 'renderer.log') -> None:
    """Setup simple logging to a single file."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_file
    )
```

### Integration with Renderers
```python
# src/renderers/base_renderer.py
import logging

class BaseRenderer(ABC):
    def __init__(self, dwg: svgwrite.Drawing):
        self.dwg = dwg
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def render(self, element: Dict) -> None:
        """Render a single element."""
        pass

# Example usage in WireRenderer
class WireRenderer(BaseRenderer):
    def render(self, wire: Dict, stroke_width: float = 1.0) -> None:
        try:
            self.logger.info(f"Rendering wire from ({wire['x1']}, {wire['y1']}) to ({wire['x2']}, {wire['y2']})")
            # Rendering logic
        except Exception as e:
            self.logger.error(f"Failed to render wire: {str(e)}")
            raise
```

### Key Logging Points
1. **State Changes**
   - Loading schematic
   - Creating drawing
   - Saving output

2. **Errors**
   - Rendering failures
   - Invalid parameters
   - Missing data

3. **Performance**
   - Long rendering operations
   - Memory usage warnings

### Usage Example
```python
# Main application
from src.utils.logger import setup_logging

# Setup logging
setup_logging('logs/renderer.log')

# In renderer code
class SVGRenderer:
    def __init__(self):
        self.logger = logging.getLogger('SVGRenderer')
        
    def load_schematic(self, schematic_data: Dict) -> None:
        self.logger.info(f"Loading schematic with {len(schematic_data)} elements")
        try:
            self.schematic_data = schematic_data
            self.view_box = self._calculate_viewbox()
        except Exception as e:
            self.logger.error(f"Failed to load schematic: {str(e)}")
            raise
```

### Logging Best Practices
1. **Keep it Simple**
   - Log only important events
   - Use clear, concise messages
   - Avoid excessive detail

2. **Focus on Errors**
   - Log all errors with context
   - Include relevant parameters
   - Don't log successful operations unless necessary

3. **Performance Impact**
   - Log only when needed
   - Keep messages short
   - Avoid complex formatting

## Implementation Plan

### Phase 1: Core Structure
1. Create base renderer class in `src/renderers/base_renderer.py`
2. Create specialized renderer classes in their respective files
3. Create main SVGRenderer class in `src/generators/svg_renderer.py`
4. Implement basic error handling and state checks

### Phase 2: Renderer Implementation
1. Implement WireRenderer
   - Basic wire rendering
   - T-junction dot rendering
2. Implement SymbolRenderer
   - Symbol geometry rendering
   - Symbol text rendering
3. Implement TextRenderer
   - Basic text rendering
   - Text positioning and rotation
4. Implement ShapeRenderer
   - Basic shape rendering
   - Style handling

### Phase 3: Testing
1. Create test structure:
```
tests/
├── test_svg_renderer/
│   ├── test_svg_renderer.py
│   └── results/
├── test_renderers/
│   ├── test_wire_renderer.py
│   ├── test_symbol_renderer.py
│   ├── test_text_renderer.py
│   ├── test_shape_renderer.py
│   └── results/
```
2. Test each renderer independently
3. Test state management and error handling
4. Test parameter combinations
5. Test integration between renderers

### Phase 4: Integration
1. Test with real schematics
2. Document new interface
3. Update examples
4. Plan gradual migration from SVGGenerator to SVGRenderer

### Phase 5: Logging Implementation
1. Create logging configuration
   - Setup basic logging
   - Implement log rotation
   - Create log directories

2. Integrate logging with renderers
   - Add logging to base renderer
   - Implement logging in specialized renderers
   - Add performance monitoring

3. Create logging utilities
   - Implement log parser
   - Create debug viewer
   - Build error reporter

4. Test logging system
   - Verify log output
   - Test log rotation
   - Validate error reporting

## Benefits
1. **Clearer Interface**
   - Explicit control over rendering
   - Better parameter organization
   - Easier to understand and use

2. **Better Maintainability**
   - Each renderer has a single responsibility
   - Smaller, focused files
   - Easier to modify individual components

3. **Improved Testability**
   - Each renderer can be tested independently
   - Easier to mock and verify behavior
   - Clear test boundaries

4. **Enhanced Flexibility**
   - Easy to add new renderers
   - Can render elements in any order
   - Can render elements multiple times with different parameters

5. **Better Code Organization**
   - Clear file structure
   - Logical grouping of related code
   - Easy to find and modify specific functionality

6. **Improved Debugging**
   - Detailed logging of operations
   - Clear error tracking
   - Performance monitoring
   - Easy troubleshooting

## Next Steps
1. Create initial file structure
2. Implement base renderer class
3. Begin implementing specialized renderers one by one
4. Set up test structure
5. Test and refine each implementation
6. Implement logging system
7. Add logging to renderers
8. Create logging utilities 