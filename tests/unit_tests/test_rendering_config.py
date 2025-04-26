"""
Unit tests for the RenderingConfig class.
"""
import pytest
from src.renderers.rendering_config import RenderingConfig


class TestRenderingConfig:
    """Test cases for the RenderingConfig class."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        config = RenderingConfig()
        
        # Check default text options
        assert config.get_option("no_schematic_comment") is False
        assert config.get_option("no_spice_directive") is False
        assert config.get_option("no_nested_symbol_text") is False
        assert config.get_option("no_component_name") is False
        assert config.get_option("no_component_value") is False
        
        # Check default rendering options
        assert config.get_option("stroke_width") == 3.0
        assert config.get_option("base_font_size") == 16.0
        assert config.get_option("dot_size_multiplier") == 1.5

    def test_init_with_overrides(self):
        """Test initialization with override values."""
        config = RenderingConfig(
            stroke_width=5.0,
            base_font_size=20.0,
            no_schematic_comment=True
        )
        
        # Check overridden values
        assert config.get_option("stroke_width") == 5.0
        assert config.get_option("base_font_size") == 20.0
        assert config.get_option("no_schematic_comment") is True
        
        # Check defaults for non-overridden values
        assert config.get_option("no_spice_directive") is False
        assert config.get_option("dot_size_multiplier") == 1.5

    def test_update_options(self):
        """Test updating multiple options at once."""
        config = RenderingConfig()
        
        # Update multiple options
        config.update_options(
            stroke_width=4.0,
            no_component_name=True,
            no_component_value=True
        )
        
        # Check updated values
        assert config.get_option("stroke_width") == 4.0
        assert config.get_option("no_component_name") is True
        assert config.get_option("no_component_value") is True
        
        # Check unchanged values
        assert config.get_option("base_font_size") == 16.0
        assert config.get_option("no_schematic_comment") is False

    def test_set_option(self):
        """Test setting a single option."""
        config = RenderingConfig()
        
        # Set a single option
        config.set_option("base_font_size", 18.0)
        
        # Check the updated value
        assert config.get_option("base_font_size") == 18.0
        
        # Check that other options are unchanged
        assert config.get_option("stroke_width") == 3.0

    def test_get_option_with_default(self):
        """Test getting an option with a default value."""
        config = RenderingConfig()
        
        # Get a non-existent option with a default
        value = config.get_option("non_existent", default="default_value")
        
        # Check that the default is returned
        assert value == "default_value"

    def test_set_text_options(self):
        """Test setting multiple text options at once."""
        config = RenderingConfig()
        
        # Set text options
        config.set_text_options(
            no_schematic_comment=True,
            no_spice_directive=True,
            no_nested_symbol_text=True
        )
        
        # Check updated values
        assert config.get_option("no_schematic_comment") is True
        assert config.get_option("no_spice_directive") is True
        assert config.get_option("no_nested_symbol_text") is True
        
        # Check unchanged text options
        assert config.get_option("no_component_name") is False
        assert config.get_option("no_component_value") is False

    def test_get_all_options(self):
        """Test getting all options."""
        config = RenderingConfig(stroke_width=4.0)
        
        # Get all options
        options = config.get_all_options()
        
        # Check that all options are included
        assert len(options) == len(RenderingConfig.DEFAULT_OPTIONS)
        
        # Check that values are correct
        assert options["stroke_width"] == 4.0
        assert options["base_font_size"] == 16.0
        
        # Check that the returned dict is a copy
        options["stroke_width"] = 10.0
        assert config.get_option("stroke_width") == 4.0

    def test_invalid_option_name(self):
        """Test that invalid option names raise ValueError."""
        config = RenderingConfig()
        
        # Try to set an invalid option
        with pytest.raises(ValueError, match="Unknown configuration option"):
            config.set_option("invalid_option", "value")
            
        # Try to update with invalid options
        with pytest.raises(ValueError, match="Unknown configuration options"):
            config.update_options(invalid_option="value")

    def test_set_text_options_with_non_text_option(self):
        """Test that set_text_options rejects non-text options."""
        config = RenderingConfig()
        
        # Try to set a non-text option via set_text_options
        with pytest.raises(ValueError, match="Not text rendering options"):
            config.set_text_options(stroke_width=4.0)

    def test_invalid_option_type(self):
        """Test that invalid option types raise ValueError."""
        config = RenderingConfig()
        
        # Try to set a text option with a non-boolean value
        with pytest.raises(ValueError, match="must be a boolean"):
            config.set_option("no_schematic_comment", "not_a_boolean")
            
        # Try to set a numeric option with a non-numeric value
        with pytest.raises(ValueError, match="must be a number"):
            config.set_option("stroke_width", "not_a_number")
            
        # Try to set a numeric option with a non-positive value
        with pytest.raises(ValueError, match="must be positive"):
            config.set_option("stroke_width", 0)
            
        with pytest.raises(ValueError, match="must be positive"):
            config.set_option("base_font_size", -1.0) 