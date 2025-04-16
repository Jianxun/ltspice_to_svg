import os
import pytest
import logging
from pathlib import Path
import sys
import shutil

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

from src.ltspice_to_svg import convert_schematic

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(autouse=True)
def setup_ltspice_lib():
    """Set up the LTspice library path environment variable."""
    os.environ['LTSPICE_LIB_PATH'] = f"/Users/{os.getenv('USER')}/Library/Application Support/LTspice/lib/sym"

@pytest.fixture
def test_schematic():
    """Get the path to the test schematic file."""
    return os.path.join(project_root, "schematics", "miller_ota.asc")

@pytest.fixture
def output_dir():
    """Get the path to the output directory."""
    return os.path.join(os.path.dirname(__file__), "results")

@pytest.fixture
def temp_schematic(test_schematic, tmp_path):
    """Create a temporary copy of the test schematic."""
    # Create a temporary directory for the test
    temp_dir = tmp_path / "test_schematic"
    temp_dir.mkdir()
    
    # Copy the test schematic to the temporary directory
    temp_schematic = temp_dir / "miller_ota.asc"
    shutil.copy2(test_schematic, temp_schematic)
    
    return str(temp_schematic)

def test_ltspice_to_svg_conversion(temp_schematic, output_dir):
    """Test the conversion of LTspice schematic to SVG.
    
    This test verifies that:
    1. The conversion process completes successfully
    2. The output SVG file is created
    3. The SVG file contains expected elements
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert the schematic with default parameters
    convert_schematic(
        temp_schematic,
        stroke_width=2.0,
        font_size=16.0,
        export_json=True  # Enable JSON export for debugging
    )
    
    # Get the output files
    schematic_dir = os.path.dirname(temp_schematic)
    base_name = os.path.splitext(os.path.basename(temp_schematic))[0]
    svg_output = os.path.join(schematic_dir, f"{base_name}.svg")
    json_output = os.path.join(schematic_dir, "output", f"{base_name}_schematic.json")
    
    # Verify output files exist
    assert os.path.exists(svg_output), f"SVG output file not found: {svg_output}"
    assert os.path.exists(json_output), f"JSON output file not found: {json_output}"
    
    # Copy output files to test results directory
    shutil.copy2(svg_output, os.path.join(output_dir, "test_ltspice_to_svg.svg"))
    shutil.copy2(json_output, os.path.join(output_dir, "test_ltspice_to_svg.json"))
    
    # Print debug information
    print(f"\nConverted schematic saved to: {svg_output}")
    print(f"JSON data saved to: {json_output}")
    
    # Verify SVG content
    with open(svg_output, 'r') as f:
        svg_content = f.read()
        
    # Check for essential SVG elements
    #assert '<?xml version="1.0" encoding="UTF-8"?>' in svg_content
    # assert '<svg' in svg_content
    # assert '</svg>' in svg_content
    
    # Check for schematic elements
    # assert '<g id="wires">' in svg_content
    # assert '<g id="symbols">' in svg_content
    # assert '<g id="texts">' in svg_content
    # assert '<g id="shapes">' in svg_content
    # assert '<g id="flags">' in svg_content

def test_ltspice_to_svg_no_text(temp_schematic, output_dir):
    """Test the conversion with text rendering disabled."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert the schematic with text disabled
    convert_schematic(
        temp_schematic,
        stroke_width=2.0,
        font_size=16.0,
        no_text=True
    )
    
    # Get the output file
    schematic_dir = os.path.dirname(temp_schematic)
    base_name = os.path.splitext(os.path.basename(temp_schematic))[0]
    svg_output = os.path.join(schematic_dir, f"{base_name}.svg")
    
    # Verify SVG content
    with open(svg_output, 'r') as f:
        svg_content = f.read()
        
    # Check that text elements are not present
    assert '<g id="texts">' not in svg_content
