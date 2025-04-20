# Publishing ltspice_to_svg to PyPI

This document describes the process for publishing the ltspice_to_svg package to PyPI.

## Prerequisites

- A PyPI account (register at [PyPI](https://pypi.org/account/register/) or [TestPyPI](https://test.pypi.org/account/register/))
- Python 3.6 or later
- Required packages: `build`, `twine`

## Setup PyPI Credentials

### Option 1: Using .pypirc file

Create a `.pypirc` file in your home directory:

```
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcCJDxxxxx  # Your PyPI API token

[testpypi]
username = __token__
password = pypi-AgEIdGVzdC5weXBpLm9yZwIkJxxxxx  # Your TestPyPI API token
```

Make sure to set appropriate permissions:

```bash
chmod 600 ~/.pypirc
```

### Option 2: Using Environment Variables

Set the following environment variables:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcCJDxxxxx  # Your API token
export TWINE_REPOSITORY=testpypi  # or 'pypi' for production
```

## Publishing Process

### Manual Process

1. **Update version number** in `setup.py`

2. **Clean previous builds**:
   ```bash
   rm -rf dist/ build/ *.egg-info/
   ```

3. **Build the package**:
   ```bash
   python -m build
   ```

4. **Upload to TestPyPI** (testing):
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

5. **Verify installation** from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ltspice_to_svg
   ```

6. **Upload to PyPI** (production) once testing is successful:
   ```bash
   python -m twine upload dist/*
   ```

### Using the Helper Script

We provide a helper script to automate the publishing process:

```bash
# Publish to TestPyPI
python tools/publish_to_pypi.py --test

# Publish to production PyPI
python tools/publish_to_pypi.py --production

# Skip build phase (if already built)
python tools/publish_to_pypi.py --test --skip-build

# Skip upload phase (build only)
python tools/publish_to_pypi.py --test --skip-twine
```

## Troubleshooting

### Common Issues

1. **Invalid credentials**:
   - Ensure your API token is correct and not expired
   - Check that you're using the right token for the chosen repository

2. **Package name conflicts**:
   - Check if the package name is already taken on PyPI
   - Use a unique name or contact the owner of the package

3. **Invalid classifiers**:
   - Ensure all classifiers in `setup.py` are from the [official list](https://pypi.org/classifiers/)

4. **Missing required files**:
   - Ensure README, LICENSE, and required files are included in MANIFEST.in
   - Verify package structure with `python setup.py check --restructuredtext`

5. **Version conflicts**:
   - You cannot upload a package with the same version number more than once
   - Always update the version number for new uploads 