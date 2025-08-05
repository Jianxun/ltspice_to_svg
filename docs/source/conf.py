# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # Add the project root to the path

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LTspice to SVG Converter'
copyright = '2025, Jianxun Zhu'
author = 'Jianxun Zhu'

version = '0.2.0'
release = '0.2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',         # Include documentation from docstrings
    'sphinx.ext.viewcode',        # Add links to highlighted source code
    'sphinx.ext.napoleon',        # Support for NumPy and Google style docstrings
    'sphinx.ext.intersphinx',     # Link to other project's documentation
    'sphinx_rtd_theme',           # Read the Docs theme
    'sphinx.ext.autosummary',     # Generate autodoc summaries
    'sphinx_autodoc_typehints',   # Support for PEP 484 type hints
    'myst_parser',                # Support for Markdown files
    'sphinx_markdown_tables',     # Support for tables in Markdown
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The suffix(es) of source filenames
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
    'navigation_depth': 4,
    'collapse_navigation': False,
}

html_static_path = ['_static']

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = 'bysource'
autoclass_content = 'both'
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'svgwrite': ('https://svgwrite.readthedocs.io/en/latest/', None),
}

# -- Other options -----------------------------------------------------------
# Include both class docstring and __init__ docstring in class documentation
autoclass_content = 'both'

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_attr_annotations = True
