"""
Tests for schematic text parsing and rendering.
Tests various text elements including:
- Font sizes (0-7)
- Justification modes (Left, Center, Right, Top, Bottom)
- Multi-line text
- SPICE directives
- Comments
- Special characters
"""
import os
from pathlib import Path
from src.parsers.asc_parser import ASCParser
from src.generators.svg_generator import SVGGenerator

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

def test_text_parsing():
    """Test parsing of TEXT elements with different properties."""
    # Parse schematic
    asc_file = PROJECT_ROOT / 'tests' / 'test_schematic_texts' / 'test_sch_texts.asc'
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Verify texts are parsed
    texts = schematic_data['texts']
    assert len(texts) == 21  # Total number of text elements
    
    # Count text types
    spice_directives = [t for t in texts if t['type'] == 'spice']
    comments = [t for t in texts if t['type'] == 'comment']
    assert len(spice_directives) == 3  # SPICE directives
    assert len(comments) == 18  # Comments
    
    # Verify font sizes
    font_sizes = [t for t in texts if 'Font Size' in t['text']]
    assert len(font_sizes) == 8  # Font size samples
    
    # Verify justification modes
    justified_texts = [t for t in texts if 'Justified' in t['text']]
    assert len(justified_texts) == 5  # Justified text samples
    
    # Verify multi-line text
    multi_line_texts = [t for t in texts if '\n' in t['text']]
    assert len(multi_line_texts) == 4  # Multi-line text samples
    
    # Verify special characters
    special_chars = [t for t in texts if 'A#$%^&*()' in t['text']]
    assert len(special_chars) == 1  # Special characters text
    assert special_chars[0]['type'] == 'comment'  # Should be a comment

def test_svg_generation():
    """Test SVG generation with text elements."""
    # Get test case directory
    test_dir = PROJECT_ROOT / 'tests' / 'test_schematic_texts'
    asc_file = test_dir / 'test_sch_texts.asc'
    
    # Parse schematic
    asc_parser = ASCParser(str(asc_file))
    schematic_data = asc_parser.parse()
    
    # Save parsed data as JSON for reference
    json_file = test_dir / 'test_sch_texts_parsed.json'
    asc_parser.export_json(str(json_file))
    print(f"Exported parsed data to {json_file}")
    
    # Generate SVG
    svg_file = test_dir / 'test_sch_texts.svg'
    generator = SVGGenerator(stroke_width=3.0, dot_size_multiplier=1.5, scale=1.0, font_size=16.0)
    generator.generate(schematic_data, str(svg_file), {})
    print(f"Generated SVG: {svg_file}")
    
    # Verify SVG file is created
    assert svg_file.exists()
    assert svg_file.stat().st_size > 0
    
    # Read SVG file to verify content
    with open(svg_file, 'r') as f:
        svg_content = f.read()
        
    # Verify basic SVG structure
    assert '<?xml version="1.0" encoding="utf-8" ?>' in svg_content
    assert '<svg' in svg_content
    assert 'viewBox' in svg_content
    
    # Count text elements in SVG
    # Each multi-line text is split into multiple <text> elements
    text_count = svg_content.count('<text')
    multi_line_count = sum(text.count('\n') for text in [t['text'] for t in schematic_data['texts']])
    expected_text_count = len(schematic_data['texts']) + multi_line_count
    assert text_count == expected_text_count  # All text elements should be rendered
    
    # Verify text content
    assert 'Font Size 7 (7.0x)' in svg_content
    assert 'Left Justified' in svg_content
    assert 'Center Justified' in svg_content
    assert 'Right Justified' in svg_content
    assert 'Top Justified' in svg_content
    assert 'Bottom Justified' in svg_content
    assert '.tran 0 1ms 0 0.1ms' in svg_content
    assert 'A#$%^&amp;*()' in svg_content  # Special characters are escaped in SVG 