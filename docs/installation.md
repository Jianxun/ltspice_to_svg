# Installing ltspice_to_svg

There are several ways to install the `ltspice_to_svg` package depending on your needs.

## Installing from GitHub

You can install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/jianxunzhu/ltspice_to_svg.git
```

This will automatically install the package and its dependencies. After installation, you should be able to run the command-line tool:

```bash
ltspice_to_svg your_schematic.asc
```

You can also specify a specific branch, tag, or commit:

```bash
# Install from a specific branch
pip install git+https://github.com/jianxunzhu/ltspice_to_svg.git@branch_name

# Install from a specific tag
pip install git+https://github.com/jianxunzhu/ltspice_to_svg.git@v0.1.0

# Install from a specific commit
pip install git+https://github.com/jianxunzhu/ltspice_to_svg.git@commit_hash
```

## Installing from PyPI

Once the package is available on PyPI, you can install it using:

```bash
pip install ltspice_to_svg
```

## Installing from TestPyPI

For testing purposes, you can install from the Test PyPI repository:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ltspice_to_svg
```

## Development Installation

For development, you should clone the repository and install it in development mode:

```bash
git clone https://github.com/jianxunzhu/ltspice_to_svg.git
cd ltspice_to_svg
pip install -e .
```

This creates an "editable" installation where changes to the code are immediately reflected in the installed package.

## Running without Installation

If you prefer not to install the package, you can also run it directly:

### Using the shell script

```bash
./ltspice_to_svg.sh your_schematic.asc
```

### Setting PYTHONPATH manually

```bash
PYTHONPATH=. python src/ltspice_to_svg.py your_schematic.asc
```

## Requirements

- Python 3.6 or later
- svgwrite 