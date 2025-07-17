from setuptools import setup, find_packages

setup(
    name="financial-analytics-models",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0", 
        "yfinance>=0.2.18"
    ]
)