from setuptools import setup, find_packages

# Provide a simple long description since README may not be available in this context
long_description = "Agothe quantum consciousness framework for multi-agent AI systems"

setup(
    name="agothe-quantum-consciousness",
    version="1.0.0",
    author="Alex Veyu",
    author_email="alex@agothe.ai",
    description="Revolutionary quantum consciousness framework for multi-agent AI systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexveyu/agothe-quantum-consciousness",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Researchers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "streamlit>=1.25.0",
        "plotly>=5.15.0",
        "networkx>=2.8.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "agothe=main:main",
        ],
    },
)