"""
Test cases for command line switches in ltspice_to_svg.py
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
import json

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.ltspice_to_svg import main, get_ltspice_lib_path

@pytest.fixture
def mock_svg_renderer():
    """Fixture to mock the SVGRenderer module import so we can verify it's being called correctly"""
    with patch('src.ltspice_to_svg.SVGRenderer') as mock:
        renderer_instance = MagicMock()
        mock.return_value = renderer_instance
        yield mock, renderer_instance

@pytest.fixture
def mock_config():
    """Fixture to mock the RenderingConfig module import"""
    with patch('src.ltspice_to_svg.RenderingConfig') as mock:
        config_instance = MagicMock()
        mock.return_value = config_instance
        yield mock

@pytest.fixture
def mock_parser():
    """Fixture to mock the SchematicParser module import"""
    with patch('src.ltspice_to_svg.SchematicParser') as mock:
        parser_instance = MagicMock()
        mock.return_value = parser_instance
        parser_instance.parse.return_value = {
            'schematic': {'test': 'data'},
            'symbols': {'test': 'symbols'}
        }
        yield parser_instance

@pytest.fixture
def mock_path():
    """Fixture to mock Path operations"""
    with patch('src.ltspice_to_svg.Path') as mock_path_class:
        path_instance = MagicMock()
        mock_path_class.return_value = path_instance
        
        # Configure the path object behavior
        path_instance.parent = MagicMock()
        path_instance.stem = 'test'
        
        # Configure parent/mkdir behavior
        parent_dir = MagicMock()
        path_instance.parent.__truediv__.return_value = parent_dir
        parent_dir.mkdir.return_value = None
        
        yield path_instance

@pytest.fixture
def mock_open_file():
    """Fixture to mock opening files to prevent FileNotFoundError"""
    mock_json_data = {
        "ground": {
            "name": "Ground",
            "description": "Ground symbol",
            "lines": [
                {
                    "start": [-16, 0],
                    "end": [16, 0]
                },
                {
                    "start": [-16, 0],
                    "end": [0, 16]
                },
                {
                    "start": [16, 0],
                    "end": [0, 16]
                }
            ],
            "text": {}
        },
        "net_label": {
            "name": "Net Label",
            "description": "Net label for wire connections",
            "lines": [],
            "text": {
                "anchor": {
                    "x": 0,
                    "y": 0
                },
                "justification": "Bottom"
            }
        },
        "io_pin": {
            "name": "IO Pin",
            "description": "Input/Output pin with direction indicators",
            "directions": {
                "In": {
                    "lines": [
                        {
                            "start": [0, 0],
                            "end": [16, 16]
                        }
                    ],
                    "text": {
                        "anchor": {
                            "x": 0,
                            "y": 38
                        },
                        "justification": "VRight"
                    }
                },
                "Out": {
                    "lines": [
                        {
                            "start": [-16, 32],
                            "end": [0, 48]
                        }
                    ],
                    "text": {
                        "anchor": {
                            "x": 0,
                            "y": 52
                        },
                        "justification": "VRight"
                    }
                },
                "BiDir": {
                    "lines": [
                        {
                            "start": [16, 16],
                            "end": [0, 0]
                        }
                    ],
                    "text": {
                        "anchor": {
                            "x": 0,
                            "y": 52
                        },
                        "justification": "VRight"
                    }
                }
            }
        }
    }
    
    # Create a file-like mock that returns the JSON data
    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = json.dumps(mock_json_data)
    
    def mock_open_side_effect(*args, **kwargs):
        # Check if we're trying to open the flags.json file
        if len(args) > 0 and isinstance(args[0], str) and 'flags.json' in args[0]:
            return mock_file
        # For all other files, return a simple MagicMock
        return MagicMock()
    
    with patch('builtins.open', side_effect=mock_open_side_effect):
        yield

def test_default_parameters(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test conversion with default parameters"""
    test_args = ['ltspice_to_svg.py', 'test.asc']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify renderer was created with the config
    mock_renderer_class, mock_renderer_instance = mock_svg_renderer
    mock_renderer_class.assert_called_once()

def test_custom_stroke_width(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test custom stroke width parameter"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--stroke-width', '2.0']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify config was created with the stroke width
    mock_config.assert_called_once()
    _, kwargs = mock_config.call_args
    assert kwargs['stroke_width'] == 2.0

def test_custom_dot_size(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test custom dot size parameter"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--dot-size', '2.0']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify config was created with the dot size
    mock_config.assert_called_once()
    _, kwargs = mock_config.call_args
    assert kwargs['dot_size_multiplier'] == 2.0

def test_custom_base_font_size(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test custom base font size parameter"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--base-font-size', '14.0']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify config was created with the base font size
    mock_config.assert_called_once()
    _, kwargs = mock_config.call_args
    assert kwargs['base_font_size'] == 14.0

def test_no_text(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test no-text parameter"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--no-text']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify render_texts is not called
    _, mock_renderer_instance = mock_svg_renderer
    mock_renderer_instance.render_texts.assert_not_called()
    
    # Verify that all text-related options are set to True
    mock_renderer_instance.set_text_rendering_options.assert_called_once()
    _, kwargs = mock_renderer_instance.set_text_rendering_options.call_args
    
    # Check all text-related options are True
    expected_options = {
        "no_schematic_comment": True,
        "no_spice_directive": True,
        "no_nested_symbol_text": True,
        "no_component_name": True,
        "no_component_value": True,
        "no_net_label": True,
        "no_pin_name": True
    }
    assert kwargs == expected_options

def test_text_rendering_options(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test individual text rendering options"""
    test_args = [
        'ltspice_to_svg.py', 'test.asc',
        '--no-schematic-comment',
        '--no-spice-directive',
        '--no-nested-symbol-text',
        '--no-component-name',
        '--no-component-value',
        '--no-net-label',
        '--no-pin-name'
    ]
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify set_text_rendering_options is called with the right params
    _, mock_renderer_instance = mock_svg_renderer
    mock_renderer_instance.set_text_rendering_options.assert_called_once_with(
        no_schematic_comment=True,
        no_spice_directive=True,
        no_nested_symbol_text=True,
        no_component_name=True,
        no_component_value=True,
        no_net_label=True,
        no_pin_name=True
    )

def test_export_json(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test JSON export functionality"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--export-json']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify export_json is called
    mock_parser.export_json.assert_called_once()

def test_ltspice_lib_path(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test custom LTspice library path"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--ltspice-lib', '/custom/path']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify environment variable is set
    assert os.environ['LTSPICE_LIB_PATH'] == '/custom/path'

def test_get_ltspice_lib_path():
    """Test LTspice library path detection"""
    with patch('platform.system', return_value='Darwin'), \
         patch('os.getenv', side_effect=lambda x: 'testuser' if x in ['USERNAME', 'USER'] else None):
        path = get_ltspice_lib_path()
        assert path == "/Users/testuser/Library/Application Support/LTspice/lib/sym"
    
    with patch('platform.system', return_value='Windows'), \
         patch('os.getenv', side_effect=lambda x: 'testuser' if x in ['USERNAME', 'USER'] else None):
        path = get_ltspice_lib_path()
        assert path == "C:\\Users\\testuser\\AppData\\Local\\LTspice\\lib\\sym"
    
    with patch('platform.system', return_value='Linux'):
        with pytest.raises(OSError, match="Unsupported operating system: Linux"):
            get_ltspice_lib_path()

def test_no_net_label(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test --no-net-label option to skip rendering net label flags"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--no-net-label']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify configuration was created with the no_net_label option
    mock_config.assert_called_once()
    _, kwargs = mock_config.call_args
    assert kwargs['no_net_label'] == True

def test_no_pin_name(mock_svg_renderer, mock_parser, mock_path, mock_config, mock_open_file):
    """Test --no-pin-name option to skip rendering I/O pin text"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--no-pin-name']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify configuration was created with the no_pin_name option
    mock_config.assert_called_once()
    _, kwargs = mock_config.call_args
    assert kwargs['no_pin_name'] == True 