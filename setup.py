"""
Setup script for Elli Digital Brain.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="elli-digital-brain",
    version="0.1.0",
    author="kutO-O",
    description="Autonomous digital being with brain-inspired cognitive architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kutO-O/elli-digital-brain",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "torch>=2.0.0",
        "brian2>=2.5.0",
        "gym>=0.26.0",
        "stable-baselines3>=2.0.0",
        "chromadb>=0.4.0",
        "redis>=5.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "loguru>=0.7.0",
        "matplotlib>=3.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
)
