from setuptools import setup, find_packages

setup(
    name="ltspice_to_svg",
    version="0.1.0",
    packages=find_packages(),
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
    author="Jianxun Zhu",
    author_email="user@example.com",  # Replace with actual email
    url="https://github.com/jianxunzhu/ltspice_to_svg",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
) 