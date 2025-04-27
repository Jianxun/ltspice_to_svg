# Installation

There are several ways to install the LTspice to SVG converter.

## Option 1: Install directly from GitHub (Recommended)

```bash
pip install git+https://github.com/Jianxun/ltspice_to_svg.git
```

After installation, you can use the command-line tool from anywhere:

```bash
ltspice_to_svg your_schematic.asc
```

## Option 2: Clone the repository and install

1. Clone the repository:
```bash
git clone https://github.com/Jianxun/ltspice_to_svg.git
cd ltspice_to_svg
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install as a development package:
```bash
pip install -e .
```

## Requirements

- Python 3.7 or higher
- svgwrite 1.4.3 or higher
- pytest 7.3.1 or higher (for running tests)

## Verifying Installation

To verify that the installation was successful, run:

```bash
ltspice_to_svg --help
```

You should see the help text with all available command line options. 