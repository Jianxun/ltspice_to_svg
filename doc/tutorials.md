# Step-by-Step Tutorials

This document provides practical tutorials for common use cases of the LTspice to SVG converter.

## Tutorial 1: Basic Schematic Conversion

This tutorial walks you through the process of converting a basic LTspice schematic to SVG.

### Prerequisites
- LTspice installed
- LTspice to SVG converter installed
- A simple schematic (.asc file)

### Steps

1. **Create or open a schematic in LTspice**

   Open LTspice and create a simple circuit or open an existing .asc file.

2. **Save the schematic**

   Save your schematic file (e.g., `simple_circuit.asc`).

3. **Open a terminal/command prompt**

   Navigate to the directory containing your schematic file.

4. **Run the conversion command**

   ```bash
   ltspice_to_svg simple_circuit.asc
   ```

5. **Verify the output**

   Check the same directory for the generated `simple_circuit.svg` file.

6. **View the SVG**

   Open the SVG file in a web browser or vector graphics editor to see the result.

## Tutorial 2: Customizing the Visual Style

This tutorial shows how to customize the appearance of the generated SVG.

### Steps

1. **Adjust line thickness**

   For thicker lines:
   ```bash
   ltspice_to_svg simple_circuit.asc --stroke-width 3.0
   ```

   For thinner lines:
   ```bash
   ltspice_to_svg simple_circuit.asc --stroke-width 1.0
   ```

2. **Change the font size**

   For larger text:
   ```bash
   ltspice_to_svg simple_circuit.asc --base-font-size 20.0
   ```

   For smaller text:
   ```bash
   ltspice_to_svg simple_circuit.asc --base-font-size 12.0
   ```

3. **Change the font family**

   ```bash
   ltspice_to_svg simple_circuit.asc --font-family "Helvetica"
   ```

4. **Adjust junction dot size**

   ```bash
   ltspice_to_svg simple_circuit.asc --dot-size 2.0
   ```

5. **Combine multiple style options**

   ```bash
   ltspice_to_svg simple_circuit.asc --stroke-width 2.5 --base-font-size 18.0 --font-family "Arial" --dot-size 1.75
   ```

6. **Adjust margins around the schematic**

   For a tight fit with no margin:
   ```bash
   ltspice_to_svg simple_circuit.asc --margin 0.0
   ```

   For a larger margin:
   ```bash
   ltspice_to_svg simple_circuit.asc --margin 15.0
   ```

## Tutorial 3: Selective Text Rendering

This tutorial demonstrates how to control which text elements are included in the SVG.

### Steps

1. **Hide all text**

   ```bash
   ltspice_to_svg simple_circuit.asc --no-text
   ```

2. **Hide only schematic comments**

   ```bash
   ltspice_to_svg simple_circuit.asc --no-schematic-comment
   ```

3. **Hide SPICE directives**

   ```bash
   ltspice_to_svg simple_circuit.asc --no-spice-directive
   ```

4. **Hide component values but keep names**

   ```bash
   ltspice_to_svg simple_circuit.asc --no-component-value
   ```

5. **Hide component names but keep values**

   ```bash
   ltspice_to_svg simple_circuit.asc --no-component-name
   ```

6. **Hide net labels**

   ```bash
   ltspice_to_svg simple_circuit.asc --no-net-label
   ```

7. **Hide I/O pin text**

   ```bash
   ltspice_to_svg simple_circuit.asc --no-pin-name
   ```

8. **Combining text options**

   Hide comments and SPICE directives:
   ```bash
   ltspice_to_svg simple_circuit.asc --no-schematic-comment --no-spice-directive
   ```

## Tutorial 4: Working with Symbol Libraries

This tutorial explains how to handle symbol library paths and missing symbols.

### Steps

1. **Specify a custom symbol library path**

   ```bash
   ltspice_to_svg simple_circuit.asc --ltspice-lib /path/to/ltspice/lib
   ```

2. **Set up an environment variable for the symbol path**

   On Linux/macOS:
   ```bash
   export LTSPICE_LIB_PATH=/path/to/ltspice/lib
   ltspice_to_svg simple_circuit.asc
   ```

   On Windows:
   ```cmd
   set LTSPICE_LIB_PATH=C:\path\to\ltspice\lib
   ltspice_to_svg simple_circuit.asc
   ```

3. **Handle missing symbols**

   If you encounter "Symbol not found" errors:
   
   a. Look for the missing symbol name in the error message
   
   b. Find the .asy file for that symbol in your LTspice installation
   
   c. Copy it to the same directory as your schematic or to a custom library folder
   
   d. Run the conversion again, specifying the path if necessary

## Tutorial 5: Creating Publication-Ready Schematics

This tutorial shows how to create clean, professional-looking schematics for publications.

### Steps

1. **Create a clean schematic with minimal text**

   ```bash
   ltspice_to_svg complex_circuit.asc --no-schematic-comment --no-spice-directive --no-net-label
   ```

2. **Optimize font size and line width**

   ```bash
   ltspice_to_svg complex_circuit.asc --base-font-size 14.0 --stroke-width 1.5 --font-family "Times New Roman"
   ```

3. **Use tight margins for better space utilization**

   ```bash
   ltspice_to_svg complex_circuit.asc --margin 5.0
   ```

4. **Post-process in a vector graphics editor**

   a. Open the generated SVG in Inkscape or Adobe Illustrator
   
   b. Make final adjustments to text positioning and styling
   
   c. Add additional annotations or highlights as needed
   
   d. Export to PDF or other publication formats

5. **Using the SVG in a publication**

   a. For LaTeX documents, include the SVG using:
   ```latex
   \begin{figure}
       \centering
       \includegraphics[width=0.8\textwidth]{complex_circuit.pdf}
       \caption{Circuit diagram for the complex design.}
       \label{fig:complex_circuit}
   \end{figure}
   ```
   
   b. For web publications, use the SVG directly:
   ```html
   <figure>
     <img src="complex_circuit.svg" alt="Complex circuit diagram">
     <figcaption>Circuit diagram for the complex design.</figcaption>
   </figure>
   ```

## Tutorial 6: Debugging SVG Generation Issues

This tutorial explains how to troubleshoot common issues with SVG generation.

### Steps

1. **Export JSON for debugging**

   ```bash
   ltspice_to_svg problematic_circuit.asc --export-json
   ```

2. **Check encoding issues**

   If you encounter encoding errors:
   
   ```bash
   python tools/fix_encoding.py problematic_circuit.asc
   ltspice_to_svg problematic_circuit.asc
   ```

3. **Isolate text rendering issues**

   ```bash
   ltspice_to_svg problematic_circuit.asc --no-text
   ```
   
   If this works correctly, gradually enable text elements to find the problematic one.

4. **Fix viewbox issues**

   If parts of your circuit are cut off:
   
   ```bash
   ltspice_to_svg problematic_circuit.asc --margin 20.0
   ```

5. **Examine the generated SVG code**

   Open the SVG file in a text editor to inspect the structure and attributes.

## Tutorial 7: Batch Processing Multiple Schematics

This tutorial shows how to convert multiple schematic files in a batch process.

### Steps

1. **Create a simple bash script (Linux/macOS)**

   Create a file named `convert_all.sh`:
   
   ```bash
   #!/bin/bash
   
   # Define common options
   OPTIONS="--stroke-width 2.0 --base-font-size 16.0 --font-family Arial"
   
   # Process all .asc files in the current directory
   for file in *.asc; do
       echo "Converting $file..."
       ltspice_to_svg "$file" $OPTIONS
   done
   
   echo "All conversions complete."
   ```

2. **Make the script executable**

   ```bash
   chmod +x convert_all.sh
   ```

3. **Run the batch conversion**

   ```bash
   ./convert_all.sh
   ```

4. **Create a batch script for Windows**

   Create a file named `convert_all.bat`:
   
   ```batch
   @echo off
   
   REM Define common options
   set OPTIONS=--stroke-width 2.0 --base-font-size 16.0 --font-family Arial
   
   REM Process all .asc files in the current directory
   for %%f in (*.asc) do (
       echo Converting %%f...
       ltspice_to_svg "%%f" %OPTIONS%
   )
   
   echo All conversions complete.
   ```

5. **Run the Windows batch script**

   ```cmd
   convert_all.bat
   ```

These tutorials cover the most common use cases for the LTspice to SVG converter. For more advanced usage or custom requirements, refer to the API documentation or open an issue on the project's GitHub repository. 