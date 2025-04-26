import os
from typing import Dict, Optional
from .asc_parser import ASCParser
from .asy_parser import ASYParser
import json

class SchematicParser:
    """Parser that handles schematic and symbol data integration.
    
    This parser combines the functionality of ASCParser and ASYParser to provide
    a unified interface for accessing both schematic and symbol data.
    """
    
    def __init__(self, schematic_path: str, lib_path: Optional[str] = None):
        """Initialize the schematic parser.
        
        Args:
            schematic_path: Path to the schematic file (.asc)
            lib_path: Optional path to the LTspice symbol library
        """
        self.schematic_path = schematic_path
        self.lib_path = lib_path or os.getenv('LTSPICE_LIB_PATH')
        self.schematic = None
        self.symbols_data = {}
        
    def find_symbol_file(self, symbol_name: str) -> str:
        """Find the symbol file for a given symbol name.
        
        Args:
            symbol_name: Name of the symbol to find
            
        Returns:
            Path to the symbol file
            
        Raises:
            FileNotFoundError: If the symbol file cannot be found
        """
        # First check in the schematic directory
        schematic_dir = os.path.dirname(self.schematic_path)
        asy_file = os.path.join(schematic_dir, f"{symbol_name}.asy")
        if os.path.exists(asy_file):
            return asy_file
            
        # Then check in the LTspice symbol library
        if self.lib_path:
            asy_file = os.path.join(self.lib_path, f"{symbol_name}.asy")
            if os.path.exists(asy_file):
                return asy_file
                
        raise FileNotFoundError(f"Symbol file not found for {symbol_name}")
        
    def load_symbol(self, symbol_name: str) -> Dict:
        """Load and parse a symbol file.
        
        Args:
            symbol_name: Name of the symbol to load
            
        Returns:
            Parsed symbol data
            
        Raises:
            FileNotFoundError: If the symbol file cannot be found
        """
        if symbol_name in self.symbols_data:
            return self.symbols_data[symbol_name]
            
        asy_file = self.find_symbol_file(symbol_name)
        asy_parser = ASYParser(asy_file)
        symbol_data = asy_parser.parse()
        self.symbols_data[symbol_name] = symbol_data
        return symbol_data
        
    def parse(self) -> Dict:
        """Parse the schematic and all required symbols.
        
        Returns:
            Dictionary containing the schematic data and symbol definitions
        """
        # Parse the schematic
        asc_parser = ASCParser(self.schematic_path)
        self.schematic = asc_parser.parse()
        
        # Load all required symbols
        for symbol in self.schematic['symbols']:
            symbol_name = symbol['symbol_name']
            try:
                self.load_symbol(symbol_name)
            except FileNotFoundError as e:
                print(f"Warning: {str(e)}")
                
        return {
            'schematic': self.schematic,
            'symbols': self.symbols_data
        }
        
    def export_json(self, output_path: str) -> None:
        """Export the parsed data to a JSON file.
        
        Args:
            output_path: Path to save the JSON file
        """
        if self.schematic is None:
            self.parse()
            
        data = {
            'schematic': self.schematic,
            'symbols': self.symbols_data
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2) 