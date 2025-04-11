import unittest
import svgwrite
from src.renderers.shape_renderer import ShapeRenderer

class TestLineStyles(unittest.TestCase):
    """Test cases for line style patterns in ShapeRenderer."""
    
    def setUp(self):
        """Set up test environment."""
        self.dwg = svgwrite.Drawing()
        self.renderer = ShapeRenderer(self.dwg)
        
    def test_solid_line(self):
        """Test solid line style (no dash array)."""
        pattern = ShapeRenderer.LINE_STYLE_SOLID
        stroke_width = 2.0
        result = self.renderer._scale_dash_array(pattern, stroke_width)
        self.assertEqual(result, "")
        
    def test_dash_pattern(self):
        """Test dash line style."""
        pattern = ShapeRenderer.LINE_STYLE_DASH
        stroke_width = 2.0
        result = self.renderer._scale_dash_array(pattern, stroke_width)
        self.assertEqual(result, "8.0,4.0")
        
    def test_dot_pattern(self):
        """Test dot line style."""
        pattern = ShapeRenderer.LINE_STYLE_DOT
        stroke_width = 2.0
        result = self.renderer._scale_dash_array(pattern, stroke_width)
        self.assertEqual(result, "0.002,4.0")
        
    def test_dash_dot_pattern(self):
        """Test dash-dot line style."""
        pattern = ShapeRenderer.LINE_STYLE_DASH_DOT
        stroke_width = 2.0
        result = self.renderer._scale_dash_array(pattern, stroke_width)
        self.assertEqual(result, "8.0,4.0,0.002,4.0")
        
    def test_dash_dot_dot_pattern(self):
        """Test dash-dot-dot line style."""
        pattern = ShapeRenderer.LINE_STYLE_DASH_DOT_DOT
        stroke_width = 2.0
        result = self.renderer._scale_dash_array(pattern, stroke_width)
        self.assertEqual(result, "8.0,4.0,0.002,4.0,0.002,4.0")
        
    def test_empty_pattern(self):
        """Test empty pattern handling."""
        pattern = ""
        stroke_width = 2.0
        result = self.renderer._scale_dash_array(pattern, stroke_width)
        self.assertEqual(result, "")
        
    def test_invalid_pattern(self):
        """Test invalid pattern handling."""
        pattern = "invalid"
        stroke_width = 2.0
        with self.assertRaises(ValueError):
            self.renderer._scale_dash_array(pattern, stroke_width)

    def test_visual_line_styles(self):
        """Test visual rendering of all line styles."""
        # Create a new drawing for visual test
        dwg = svgwrite.Drawing('test_line_styles.svg', size=('400px', '200px'))
        renderer = ShapeRenderer(dwg)
        
        # Define line parameters
        y_spacing = 30
        start_x = 50
        end_x = 350
        stroke_width = 2.0
        
        # Render each line style
        styles = [
            (ShapeRenderer.LINE_STYLE_SOLID, "Solid Line"),
            (ShapeRenderer.LINE_STYLE_DASH, "Dash Pattern"),
            (ShapeRenderer.LINE_STYLE_DOT, "Dot Pattern"),
            (ShapeRenderer.LINE_STYLE_DASH_DOT, "Dash-Dot Pattern"),
            (ShapeRenderer.LINE_STYLE_DASH_DOT_DOT, "Dash-Dot-Dot Pattern")
        ]
        
        for i, (style, label) in enumerate(styles):
            y = 50 + i * y_spacing
            
            # Add the line
            line = {
                'type': 'line',
                'x1': start_x,
                'y1': y,
                'x2': end_x,
                'y2': y,
                'style': style
            }
            renderer.render(line, stroke_width)
            
            # Add label
            dwg.add(dwg.text(label, insert=(start_x - 40, y + 5), 
                           font_size='12px', text_anchor='end'))
        
        # Save the drawing
        dwg.save()
        
        # Verify the file was created
        import os
        self.assertTrue(os.path.exists('test_line_styles.svg'))

if __name__ == '__main__':
    unittest.main() 