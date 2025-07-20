# Installation Guide

This guide explains how to properly install the financial-analytics-models package from GitHub.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: Install from GitHub (Recommended)

```bash
# Install directly from GitHub
pip install git+https://github.com/SolieSoftware/financial-analytics-models.git

# Or install a specific branch
pip install git+https://github.com/SolieSoftware/financial-analytics-models.git@sol-dev-rsi-model
```

### Method 2: Clone and Install Locally

```bash
# Clone the repository
git clone https://github.com/SolieSoftware/financial-analytics-models.git
cd financial-analytics-models

# Install in development mode
pip install -e .
```

### Method 3: Install from Requirements File

```bash
# Clone the repository
git clone https://github.com/SolieSoftware/financial-analytics-models.git
cd financial-analytics-models

# Install dependencies
pip install -r sanbox/relative_strength_index/requirements.txt

# Install the package
pip install -e .
```

## Verification

After installation, test that the package works:

```python
# Test import
from financial_models.rsi import RSIModel

# Test functionality
model = RSIModel()
data = model.analyze_stock("AAPL")
print(f"Latest RSI: {data['RSI'].iloc[-1]:.2f}")
```

## Troubleshooting

### Issue: "No module named 'financial_models'"

**Solution:**

1. Make sure you're in the correct directory
2. Check that the package was installed: `pip list | grep financial`
3. Try reinstalling: `pip uninstall financial-analytics-models && pip install -e .`

### Issue: Missing dependencies

**Solution:**

```bash
pip install pandas numpy yfinance
```

### Issue: Import error in RSIModel

**Solution:**

1. Check that all `__init__.py` files exist
2. Verify the package structure:
   ```
   financial_models/
   ├── __init__.py
   └── rsi/
       ├── __init__.py
       └── model.py
   ```

## Package Structure

The installed package should have this structure:

```
site-packages/financial_models/
├── __init__.py
└── rsi/
    ├── __init__.py
    └── model.py
```

## Usage in Other Projects

Once installed, you can use the RSI model in any Python project:

```python
from financial_models.rsi import RSIModel

# Create model instance
rsi_model = RSIModel(period=14)

# Analyze stocks
data = rsi_model.analyze_stock("GOOG")
latest_rsi = data['RSI'].iloc[-1]

# Generate trading signals
if latest_rsi < 30:
    print("BUY signal - Oversold")
elif latest_rsi > 70:
    print("SELL signal - Overbought")
else:
    print("HOLD - No signal")
```

## Development Installation

For development work:

```bash
# Clone the repository
git clone https://github.com/SolieSoftware/financial-analytics-models.git
cd financial-analytics-models

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e .[dev]
```

## Testing the Installation

Run the test script to verify everything works:

```bash
python test_package_install.py
```

This will check:

- Package structure
- Import functionality
- Basic RSI calculations
- Stock data fetching
