import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.parsers.asc_parser import ASCParser

def main():
    # Setup paths
    test_dir = os.path.dirname(os.path.abspath(__file__))
    schematic_path = os.path.join(test_dir, 'test2_texts.asc')
    json_path = os.path.join(test_dir, 'results', 'test2_texts.json')
    
    # Create results directory if it doesn't exist
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    # Parse the schematic and save to JSON
    parser = ASCParser(schematic_path)
    schematic_data = parser.parse()
    parser.export_json(json_path)
    
    print(f"Parsed schematic saved to {json_path}")

if __name__ == "__main__":
    main() 