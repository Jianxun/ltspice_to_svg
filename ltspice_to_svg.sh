#!/bin/bash
# Script to run the ltspice_to_svg tool

# Check for required arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <schematic.asc> [options]"
    echo "Run with --help for full options list"
    exit 1
fi

# Set the Python path to include the project directory
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the tool with all arguments passed to this script
python src/ltspice_to_svg.py "$@"

# Check if the command was successful
if [ $? -ne 0 ]; then
    echo "Error: The conversion failed. Please check the error message above."
    exit 1
fi

echo "Conversion completed successfully." 