#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup configuration for DocConvert-CLI."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="docconvert-cli",
    version="1.0.0",
    author="DocConvert Team",
    author_email="docconvert@example.com",
    description="A lightweight, cross-platform document format conversion tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/docconvert-cli",
    py_modules=["docconvert"],
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "full": [
            "markdown>=3.4.0",
            "beautifulsoup4>=4.11.0",
            "python-docx>=0.8.11",
            "pymupdf>=1.21.0",
            "pypandoc>=1.6.3",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "docconvert=docconvert:cli",
            "dconv=docconvert:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    keywords="document conversion markdown html pdf docx cli tool",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/docconvert-cli/issues",
        "Source": "https://github.com/yourusername/docconvert-cli",
    },
)
