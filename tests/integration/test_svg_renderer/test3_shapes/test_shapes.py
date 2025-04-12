import os
import pytest
import xml.etree.ElementTree as ET
import math
from src.generators.svg_renderer import SVGRenderer
from src.parsers.asc_parser import ASCParser

def calculate_angle(x: float, y: float, center_x: float, center_y: float) -> float:
    """Calculate the angle of a point relative to the center."""
    dx = x - center_x
    dy = y - center_y
    angle = math.atan2(dy, dx)
    angle_deg = math.degrees(angle)
    # Normalize to [0, 360) range
    return (angle_deg + 360) % 360

def test_shapes():
    # Setup paths
    test_dir = os.path.dirname(os.path.abspath(__file__))
    schematic_path = os.path.join(test_dir, 'shapes.asc')
    output_path = os.path.join(test_dir, 'results', 'shapes.svg')
    json_path = os.path.join(test_dir, 'results', 'shapes.json')
    
    # Create results directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Parse the schematic and save to JSON
    parser = ASCParser(schematic_path)
    schematic_data = parser.parse()
    parser.export_json(json_path)
    
    # Create SVG renderer
    renderer = SVGRenderer()
    renderer.load_schematic(schematic_data)
    renderer.create_drawing(output_path)
    
    # Render shapes
    renderer.render_shapes(stroke_width=2.0)
    
    # Save the SVG
    renderer.save()
    
    # Verify the shapes in the schematic
    shapes = schematic_data.get('shapes', {})
    
    # Count different types of shapes
    line_count = len(shapes.get('lines', []))
    rectangle_count = len(shapes.get('rectangles', []))
    circle_count = len(shapes.get('circles', []))
    arc_count = len(shapes.get('arcs', []))
    
    # Print shape counts for verification
    print("\nFound shapes:")
    print(f"Lines: {line_count}")
    print(f"Rectangles: {rectangle_count}")
    print(f"Circles: {circle_count}")
    print(f"Arcs: {arc_count}")
    
    # Verify the total number of shapes
    total_shapes = line_count + rectangle_count + circle_count + arc_count
    assert total_shapes == 13, f"Expected 13 shapes, found {total_shapes}"
    
    # Verify individual shape counts
    assert line_count == 5, f"Expected 5 lines, found {line_count}"
    assert rectangle_count == 2, f"Expected 2 rectangles, found {rectangle_count}"
    assert circle_count == 2, f"Expected 2 circles, found {circle_count}"
    assert arc_count == 4, f"Expected 4 arcs, found {arc_count}"
    
    # Parse the generated SVG
    tree = ET.parse(output_path)
    root = tree.getroot()
    
    # Find all arc paths in the SVG
    arc_paths = root.findall(".//{http://www.w3.org/2000/svg}path")
    assert len(arc_paths) == 4, f"Expected 4 arc paths in SVG, found {len(arc_paths)}"
    
    # Extract arc parameters from the schematic for comparison
    arcs = shapes.get('arcs', [])
    
    # Verify each arc's parameters in the rendered SVG
    for i, path in enumerate(arc_paths):
        # Get the path data
        d = path.get('d')
        # Path data format: M start_x start_y A rx ry 0 large_arc sweep end_x end_y
        parts = d.split()
        start_x = float(parts[1])
        start_y = float(parts[2])
        rx = float(parts[4])
        ry = float(parts[5])
        large_arc = int(parts[7])
        sweep = int(parts[8])
        end_x = float(parts[9])
        end_y = float(parts[10])
        
        # Get expected parameters from the schematic
        arc = arcs[i]
        expected_center_x = (arc['x1'] + arc['x2']) / 2
        expected_center_y = (arc['y1'] + arc['y2']) / 2
        expected_rx = abs(arc['x2'] - arc['x1']) / 2
        expected_ry = abs(arc['y2'] - arc['y1']) / 2
        expected_start_angle = arc['start_angle']
        expected_end_angle = arc['end_angle']
        
        # Verify the ellipse parameters
        assert abs(rx - expected_rx) < 1e-6, \
            f"Arc {i+1} radius x mismatch: rendered {rx}, expected {expected_rx}"
        assert abs(ry - expected_ry) < 1e-6, \
            f"Arc {i+1} radius y mismatch: rendered {ry}, expected {expected_ry}"
        
        # Calculate the angle difference
        angle_diff = (expected_end_angle - expected_start_angle + 360) % 360
        
        # Verify the arc direction (sweep flag)
        # For counter-clockwise arcs, sweep should be 1
        assert sweep == 1, f"Arc {i+1} should be rendered counter-clockwise"
        
        # Verify the large arc flag
        # For angles > 180 degrees, large_arc should be 1
        expected_large_arc = 1 if angle_diff > 180 else 0
        assert large_arc == expected_large_arc, \
            f"Arc {i+1} large arc flag mismatch: rendered {large_arc}, expected {expected_large_arc}"
        
        # Print arc information for debugging
        print(f"\nArc {i+1} parameters:")
        print(f"Expected start angle: {expected_start_angle}")
        print(f"Expected end angle: {expected_end_angle}")
        print(f"Angle difference: {angle_diff}")
        print(f"Large arc flag: {large_arc}")
        print(f"Sweep flag: {sweep}") 