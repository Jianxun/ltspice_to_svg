# Text Rendering Options Design Proposal

## Problem Statement

The current implementation of text rendering options in the SVGRenderer class has several issues:

1. The SVGRenderer class has too many responsibilities
2. The code is getting too long and complex
3. The text rendering filtering logic is separate from the renderers that actually perform the rendering
4. Multiple renderers (SVGRenderer, SymbolRenderer, FlagRenderer) invoke the TextRenderer, making a global configuration solution complex

## Proposed Design: Parameter-Based Filtering

This proposal suggests a parameter-based approach to text filtering where options are passed down through the rendering pipeline.

### Modify SVGRenderer.render_symbols()

```python
def render_symbols(self, property_id: Optional[str] = None) -> None:
    """Render all symbols in the schematic.
    
    Args:
        property_id: Optional property ID to render. If provided, only renders window text for this property.
                    If None, renders all defined window texts.
    """
    if not self.schematic_data or not self.dwg:
        raise ValueError("Schematic not loaded or drawing not created")
        
    symbol_renderer = self._renderers['symbol']
    symbols = self.schematic_data.get('symbols', [])
    self.logger.info(f"Found {len(symbols)} symbols to render")
    
    # Apply text rendering filters
    # If component names should be hidden, override property_id filter
    if self.no_component_name and property_id == '0':
        self.logger.debug("Skipping component names (property_id=0) due to rendering configuration")
        return
        
    # If component values should be hidden, override property_id filter
    if self.no_component_value and property_id == '3':
        self.logger.debug("Skipping component values (property_id=3) due to rendering configuration")
        return
    
    # Create text rendering options to pass to symbol renderer
    text_options = {
        'no_nested_symbol_text': self.no_nested_symbol_text,
        'no_component_name': self.no_component_name,
        'no_component_value': self.no_component_value
    }
    
    for i, symbol in enumerate(symbols):
        # ... existing code ...
        
        # Create symbol data for rendering
        render_data = {
            # ... existing data ...
            'property_id': property_id,  # Add property_id for window text rendering
            'text_options': text_options  # Add text rendering options
        }
        
        # Render the symbol
        symbol_renderer.render(render_data, self._stroke_width)
```

### Update SymbolRenderer to Use Text Options

```python
def render(self, symbol: Dict, stroke_width: float = None) -> svgwrite.container.Group:
    # ... existing code ...
    
    # Extract text rendering options
    text_options = symbol.get('text_options', {})
    no_nested_symbol_text = text_options.get('no_nested_symbol_text', False)
    no_component_name = text_options.get('no_component_name', False)
    no_component_value = text_options.get('no_component_value', False)
    
    # Render symbol texts (unless disabled)
    if not no_nested_symbol_text:
        self._render_symbol_texts(symbol, group)
    
    # Render window texts (unless disabled)
    property_id = symbol.get('property_id')
    if property_id == '0' and no_component_name:
        # Skip component names
        pass
    elif property_id == '3' and no_component_value:
        # Skip component values
        pass
    else:
        self._render_window_texts(symbol, group)
    
    # ... rest of method ...
```

### Similarly Update SVGRenderer.render_texts()

```python
def render_texts(self) -> None:
    """Render all text elements in the schematic."""
    if not self.schematic_data or not self.dwg:
        raise ValueError("Schematic not loaded or drawing not created")
        
    text_renderer = self._renderers['text']
    texts = self.schematic_data.get('texts', [])
    self.logger.info(f"Found {len(texts)} text elements to render")
    
    for i, text in enumerate(texts):
        # Skip rendering based on text type and options
        text_type = text.get('type', 'comment')
        if text_type == 'comment' and self.no_schematic_comment:
            self.logger.debug(f"Skipping schematic comment: {text.get('text', '')}")
            continue
        elif text_type == 'spice' and self.no_spice_directive:
            self.logger.debug(f"Skipping SPICE directive: {text.get('text', '')}")
            continue
                
        self.logger.info(f"Rendering text {i+1}/{len(texts)}:")
        text_renderer.render(text)
```

### Update FlagRenderer (if needed)

Pass rendering options to the FlagRenderer in a similar way if it needs to handle filtering.

## Advantages of This Approach

1. **Maintains Existing Architecture**: Works within the current renderer structure
2. **Improves Separation of Concerns**: Each renderer applies filtering for its domain
3. **Reduces Complexity in SVGRenderer**: By delegating filtering to appropriate renderers
4. **No Global State**: Avoids introducing shared global configuration
5. **Consistent Pattern**: Matches existing approach used for property_id filtering
6. **Better Encapsulation**: Keeps filtering logic close to its use

## Alternative Approaches (Not Recommended)

### Shared Configuration Object

Create a shared TextRenderingConfig object that all renderers access:

```python
class TextRenderingConfig:
    """Configuration for text rendering options."""
    
    def __init__(self):
        self.no_schematic_comment = False
        self.no_spice_directive = False
        self.no_nested_symbol_text = False
        self.no_component_name = False
        self.no_component_value = False
    
    def should_render(self, text):
        """Determine if a text element should be rendered."""
        # Filtering logic
```

**Drawbacks**: Introduces global state, creates tight coupling between renderers.

### Observer Pattern

Make TextRenderingConfig observable and have renderers observe it:

```python
class TextRenderingConfig:
    """Observable configuration for text rendering."""
    
    def __init__(self):
        self.observers = []
        # Options...
        
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def notify_observers(self):
        for observer in self.observers:
            observer.config_updated()
```

**Drawbacks**: Overly complex for this use case, introduces observer management overhead.

### Singleton Configuration

Use a singleton pattern for TextRenderingConfig:

```python
class TextRenderingConfig:
    """Singleton configuration for text rendering options."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TextRenderingConfig, cls).__new__(cls)
            # Initialize options...
        return cls._instance
```

**Drawbacks**: Introduces global state, makes testing more difficult, creates implicit dependencies.

## Implementation Strategy

1. Add direct properties to SVGRenderer (as already implemented)
2. Update render_symbols() to pass options to SymbolRenderer
3. Update render_texts() to filter texts in-place
4. Update SymbolRenderer to respect the passed options
5. Update tests to verify filtering behavior

## Conclusion

The parameter-based filtering approach is recommended as it maintains the existing architecture while improving separation of concerns. It avoids introducing global state or complex patterns, and keeps the filtering logic close to where it's used. 