from setuptools import setup, find_packages

setup(
    name="artw-stylekit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "pymupdf>=1.23.0",
        "python-docx>=1.1.0",
        "spacy>=3.7.0",
        "jsonlines>=4.0.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "loguru>=0.7.0",
        "pyyaml>=6.0.0",
        "jinja2>=3.1.0",
        "tenacity>=8.2.0",
        "ratelimit>=2.2.1",
        "networkx>=3.2.0",
        "openai>=1.0.0",
        "google-generativeai>=0.3.0",
        "anthropic>=0.18.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "ruff>=0.1.0",
            "black>=23.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "artw=artw.cli:cli",
        ],
    },
)
