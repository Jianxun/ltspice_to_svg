from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# All the subpackages
packages = find_packages(include=["src", "src.*"])

# Ensure 'src.renderers.flag_definitions' is included
if "src.renderers" not in packages:
    packages.append("src.renderers")
if "src.renderers.flag_definitions" not in packages:
    packages.append("src.renderers.flag_definitions")

setup(
    name="ltspice_to_svg",
    version="0.2.0",
    packages=packages,
    package_data={
        "src": ["renderers/flag_definitions/flags.json"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ltspice_to_svg=src.ltspice_to_svg:main",
        ],
    },
    install_requires=[
        "svgwrite",
    ],
    python_requires=">=3.6",
    description="Convert LTspice schematics to SVG format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jianxun Zhu",
    author_email="zhujianxun.bupt@gmail.com",  # Replace with your PyPI registered email
    url="https://github.com/Jianxun/ltspice_to_svg",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="ltspice, svg, schematic, circuit, eda, electronics",
) 