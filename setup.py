from setuptools import setup, find_packages

setup(
    name="financial-analytics-models",
    version="1.0.0",
    description="Financial analytics models including RSI analysis",
    author="Solomon Shortland",
    author_email="solomon.shortland@carbonuw.com",
    packages=find_packages(include=['financial_models', 'financial_models.*', 'financial_models.rsi.*']),
    package_dir={'': '.'},
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0", 
        "yfinance>=0.2.18"
    ],
    extras_require={
        "dev": [
            "jupyter>=1.0.0",
            "matplotlib>=3.4.0",
            "pytest>=7.0.0"
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)