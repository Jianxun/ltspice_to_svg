# Renderers API Documentation

This document describes the API of all renderers used in the LTspice to SVG conversion system.

## Base Renderer

The base renderer class that all other renderers inherit from.

```python
class BaseRenderer(ABC):
    def __init__(self, dwg: svgwrite.Drawing):
        self.dwg = dwg
        self.logger = logging.getLogger(self.__class__.__name__)
```

## Wire Renderer

Renders wire elements in the schematic.

```python
class WireRenderer(BaseRenderer):
    def render(self, wire: dict, stroke_width: float = 1.0) -> None:
        """
        Render a wire element.
        
        Args:
            wire: Dictionary containing wire coordinates
                {
                    'x1': float,  # Start x coordinate
                    'y1': float,  # Start y coordinate
                    'x2': float,  # End x coordinate
                    'y2': float   # End y coordinate
                }
            stroke_width: Width of the wire line
        """
    
    def render_t_junction(self, x: float, y: float, dot_size: float) -> None:
        """
        Render a T-junction dot at the specified coordinates.
        
        Args:
            x: X coordinate of the junction
            y: Y coordinate of the junction
            dot_size: Size of the junction dot
        """
```

## Text Renderer

Renders text elements in the schematic.

```python
class TextRenderer(BaseRenderer):
    # Font size multiplier mapping
    SIZE_MULTIPLIERS = {
        0: 0.625,  # 0.625x base size
        1: 1.0,    # 1.0x base size
        2: 1.5,    # 1.5x base size (default)
        3: 2.0,    # 2.0x base size
        4: 2.5,    # 2.5x base size
        5: 3.5,    # 3.5x base size
        6: 5.0,    # 5.0x base size
        7: 7.0     # 7.0x base size
    }
    
    def render(self, text: Dict, font_size: float = 22.0, target_group: Optional[svgwrite.container.Group] = None) -> None:
        """
        Render a text element.
        
        Args:
            text: Dictionary containing text properties:
                - x: X coordinate
                - y: Y coordinate
                - text: Text content
                - justification: Text alignment ('Left', 'Right', 'Center', 'Top', 'Bottom')
                - size_multiplier: Font size multiplier index (0-7)
            font_size: Base font size in pixels
            target_group: Optional group to add the text to. If None, adds to drawing.
        """
```

## Shape Renderer

Renders various shape types in the schematic.

```python
class ShapeRenderer(BaseRenderer):
    # Line style patterns
    LINE_STYLE_SOLID = None  # No dash array for solid lines
    LINE_STYLE_DASH = "4,2"  # 4 units dash, 2 units gap
    LINE_STYLE_DOT = "0.001,2"  # Very small dash to create dots, 2 units gap
    LINE_STYLE_DASH_DOT = "4,2,0.001,2"  # Dash, gap, dot, gap
    LINE_STYLE_DASH_DOT_DOT = "4,2,0.001,2,0.001,2"  # Dash, gap, dot, gap, dot, gap
    
    def render(self, shape: Dict, stroke_width: float = 1.0, target_group: Optional[svgwrite.container.Group] = None) -> None:
        """
        Render a single shape based on its type.
        
        Args:
            shape: Dictionary containing shape properties
            stroke_width: Width of the stroke
            target_group: Optional group to add the shape to. If None, adds to drawing.
            
        Shape types supported:
        - line: {'type': 'line', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        - circle: {'type': 'circle', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2} or {'type': 'circle', 'cx': cx, 'cy': cy, 'r': r}
        - rectangle: {'type': 'rectangle', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        - arc: {'type': 'arc', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'start_angle': angle, 'end_angle': angle}
        """
```

## Symbol Renderer

Renders LTspice symbols as SVG groups.

```python
class SymbolRenderer(BaseRenderer):
    def __init__(self, dwg: svgwrite.Drawing):
        """
        Initialize the symbol renderer.
        
        Args:
            dwg: The SVG drawing to render into
        """
    
    def create_group(self) -> svgwrite.container.Group:
        """
        Create a new group for a symbol.
        
        Returns:
            An SVG group element
        """
    
    def set_transformation(self, rotation: str, translation: Tuple[float, float]) -> None:
        """
        Set the transformation for the current group.
        
        Args:
            rotation: Rotation string (e.g. 'R0', 'M90')
            translation: Tuple of (x, y) coordinates
        """
    
    def render_shapes(self, shapes: Dict, stroke_width: float = 1.0) -> None:
        """
        Render shapes for the current symbol.
        
        Args:
            shapes: Dictionary containing shape definitions
            stroke_width: Width of lines
        """
    
    def render_texts(self, texts: Dict, font_size: float = 22.0,
                    size_multipliers: Optional[Dict[int, float]] = None) -> None:
        """
        Render texts for the current symbol.
        
        Args:
            texts: Dictionary containing text definitions
            font_size: Base font size in pixels
            size_multipliers: Dictionary mapping size indices to font size multipliers
        """
    
    def add_to_drawing(self) -> None:
        """
        Add the current group to the drawing.
        
        This should be called after all rendering operations are complete.
        """
```

## Usage Example

Here's an example of how to use the renderers together:

```python
# Create drawing
dwg = svgwrite.Drawing()

# Create symbol renderer
symbol_renderer = SymbolRenderer(dwg)

# Create a group for the symbol
symbol_renderer.create_group()

# Set transformation (e.g., rotate 90 degrees at position (100, 100))
symbol_renderer.set_transformation('R90', (100, 100))

# Define shapes
shapes = {
    'lines': [
        {'x1': 0, 'y1': 0, 'x2': 10, 'y2': 10},
        {'x1': 10, 'y1': 0, 'x2': 0, 'y2': 10}
    ],
    'circles': [
        {'cx': 5, 'cy': 5, 'r': 2}
    ]
}

# Render shapes
symbol_renderer.render_shapes(shapes, stroke_width=2.0)

# Define texts
texts = [
    {
        'x': 0,
        'y': -16,
        'text': 'Test',
        'justification': 'Center',
        'size_multiplier': 2
    }
]

# Render texts
symbol_renderer.render_texts(texts, font_size=22.0)

# Add to drawing
symbol_renderer.add_to_drawing()

# Save the result
dwg.saveas('output.svg')
```

## Standalone Usage Examples

### Shape Renderer Example

Here's how to use the Shape Renderer directly to render shapes onto a drawing:

```python
# Create drawing
dwg = svgwrite.Drawing()

# Create shape renderer
shape_renderer = ShapeRenderer(dwg)

# Render a line
line = {
    'type': 'line',
    'x1': 0,
    'y1': 0,
    'x2': 100,
    'y2': 100,
    'style': ShapeRenderer.LINE_STYLE_DASH  # Optional: use dashed line style
}
shape_renderer.render(line, stroke_width=2.0)

# Render a circle using center-radius format
circle = {
    'type': 'circle',
    'cx': 50,
    'cy': 50,
    'r': 20
}
shape_renderer.render(circle, stroke_width=1.5)

# Render a rectangle
rectangle = {
    'type': 'rectangle',
    'x1': 10,
    'y1': 10,
    'x2': 90,
    'y2': 90,
    'style': ShapeRenderer.LINE_STYLE_DOT  # Optional: use dotted line style
}
shape_renderer.render(rectangle, stroke_width=1.0)

# Render an arc
arc = {
    'type': 'arc',
    'x1': 0,
    'y1': 0,
    'x2': 100,
    'y2': 100,
    'start_angle': 0,
    'end_angle': 90
}
shape_renderer.render(arc, stroke_width=1.0)

# Save the result
dwg.saveas('shapes.svg')
```

### Text Renderer Example

Here's how to use the Text Renderer directly to render text onto a drawing:

```python
# Create drawing
dwg = svgwrite.Drawing()

# Create text renderer
text_renderer = TextRenderer(dwg)

# Render a simple text
simple_text = {
    'x': 50,
    'y': 50,
    'text': 'Hello World',
    'justification': 'Center',
    'size_multiplier': 2  # 1.5x base size
}
text_renderer.render(simple_text, font_size=22.0)

# Render a multiline text
multiline_text = {
    'x': 50,
    'y': 100,
    'text': 'Line 1\nLine 2\nLine 3',
    'justification': 'Left',
    'size_multiplier': 1  # 1.0x base size
}
text_renderer.render(multiline_text, font_size=22.0)

# Render text with different justifications
texts = [
    {
        'x': 50,
        'y': 150,
        'text': 'Left',
        'justification': 'Left',
        'size_multiplier': 2
    },
    {
        'x': 50,
        'y': 200,
        'text': 'Center',
        'justification': 'Center',
        'size_multiplier': 2
    },
    {
        'x': 50,
        'y': 250,
        'text': 'Right',
        'justification': 'Right',
        'size_multiplier': 2
    }
]

for text in texts:
    text_renderer.render(text, font_size=22.0)

# Save the result
dwg.saveas('texts.svg')
```

### Wire Renderer Example

Here's how to use the Wire Renderer directly to render wires and T-junctions:

```python
# Create drawing
dwg = svgwrite.Drawing()

# Create wire renderer
wire_renderer = WireRenderer(dwg)

# Render a simple wire
wire = {
    'x1': 0,
    'y1': 0,
    'x2': 100,
    'y2': 100
}
wire_renderer.render(wire, stroke_width=2.0)

# Render a T-junction dot
wire_renderer.render_t_junction(50, 50, dot_size=3.0)

# Save the result
dwg.saveas('wires.svg')
``` 