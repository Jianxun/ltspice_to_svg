"""
Test cases for command line switches in ltspice_to_svg.py
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.ltspice_to_svg import main, get_ltspice_lib_path

@pytest.fixture
def mock_renderer():
    """Fixture to mock the SVGRenderer class"""
    with patch('src.ltspice_to_svg.SVGRenderer') as mock:
        renderer_instance = MagicMock()
        mock.return_value = renderer_instance
        yield mock

@pytest.fixture
def mock_renderer_instance():
    """Fixture to mock the SVGRenderer instance"""
    with patch('src.ltspice_to_svg.SVGRenderer') as mock_class:
        renderer_instance = MagicMock()
        mock_class.return_value = renderer_instance
        yield renderer_instance

@pytest.fixture
def mock_parser():
    """Fixture to mock the SchematicParser class"""
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
    with patch('src.ltspice_to_svg.Path') as mock:
        path_instance = MagicMock()
        mock.return_value = path_instance
        path_instance.parent = MagicMock()
        path_instance.stem = 'test_schematic'
        yield path_instance

@pytest.fixture
def mock_config():
    """Fixture to mock the RenderingConfig class"""
    with patch('src.ltspice_to_svg.RenderingConfig') as mock:
        config_instance = MagicMock()
        mock.return_value = config_instance
        yield mock

def test_default_parameters(mock_renderer, mock_parser, mock_path, mock_config):
    """Test conversion with default parameters"""
    test_args = ['ltspice_to_svg.py', 'test.asc']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify renderer was created with the config
    mock_renderer.assert_called_once()
    args, kwargs = mock_renderer.call_args
    assert len(args) == 1
    assert isinstance(args[0], MagicMock)  # The config instance

def test_custom_stroke_width(mock_renderer, mock_parser, mock_path, mock_config):
    """Test custom stroke width parameter"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--stroke-width', '2.0']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify config was created with the stroke width
    mock_config.assert_called_once()
    args, kwargs = mock_config.call_args
    assert kwargs['stroke_width'] == 2.0

def test_custom_dot_size(mock_renderer, mock_parser, mock_path, mock_config):
    """Test custom dot size parameter"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--dot-size', '2.0']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify config was created with the dot size
    mock_config.assert_called_once()
    args, kwargs = mock_config.call_args
    assert kwargs['dot_size_multiplier'] == 2.0

def test_custom_base_font_size(mock_renderer, mock_parser, mock_path, mock_config):
    """Test custom base font size parameter"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--base-font-size', '14.0']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify config was created with the base font size
    mock_config.assert_called_once()
    args, kwargs = mock_config.call_args
    assert kwargs['base_font_size'] == 14.0

def test_no_text(mock_renderer_instance, mock_parser, mock_path, mock_config):
    """Test no-text parameter"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--no-text']
    
    with patch('sys.argv', test_args):
        main()
    
    # Verify render_texts is not called
    mock_renderer_instance.render_texts.assert_not_called()

def test_text_rendering_options(mock_renderer_instance, mock_parser, mock_path, mock_config):
    """Test individual text rendering options"""
    test_args = [
        'ltspice_to_svg.py', 'test.asc',
        '--no-schematic-comment',
        '--no-spice-directive',
        '--no-nested-symbol-text',
        '--no-component-name',
        '--no-component-value'
    ]
    
    with patch('sys.argv', test_args), patch('src.ltspice_to_svg.create_config_from_args') as mock_create_config:
        # Return the mock_config directly to ensure we can track it
        mock_create_config.return_value = mock_config.return_value
        main()
    
    # Verify config was created with all the text options set to True
    mock_create_config.assert_called_once()
    args, _ = mock_create_config.call_args
    assert args[0].no_schematic_comment is True
    assert args[0].no_spice_directive is True
    assert args[0].no_nested_symbol_text is True
    assert args[0].no_component_name is True
    assert args[0].no_component_value is True
    
    # For backward compatibility, ensure the set_text_rendering_options method is still called
    # This allows for a smooth transition to the new approach
    mock_renderer_instance.set_text_rendering_options.assert_called_once_with(
        no_schematic_comment=True,
        no_spice_directive=True,
        no_nested_symbol_text=True,
        no_component_name=True,
        no_component_value=True
    )

def test_export_json(mock_renderer_instance, mock_parser, mock_path, mock_config):
    """Test JSON export functionality"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--export-json']
    
    with patch('sys.argv', test_args):
        main()
    
    mock_parser.export_json.assert_called_once()

def test_ltspice_lib_path(mock_renderer_instance, mock_parser, mock_path, mock_config):
    """Test custom LTspice library path"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--ltspice-lib', '/custom/path']
    
    with patch('sys.argv', test_args):
        main()
    
    assert os.environ['LTSPICE_LIB_PATH'] == '/custom/path'

def test_scale_deprecation_warning(mock_renderer_instance, mock_parser, mock_path, mock_config):
    """Test scale parameter deprecation warning"""
    test_args = ['ltspice_to_svg.py', 'test.asc', '--scale', '2.0']
    
    with patch('sys.argv', test_args), \
         pytest.warns(DeprecationWarning, match="The 'scale' parameter is deprecated"):
        main()

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