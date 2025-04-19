#!/bin/bash
# Script to run the ltspice_to_svg tool

# Set the Python path to include the project directory
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the tool with all arguments passed to this script
python src/ltspice_to_svg.py "$@" 