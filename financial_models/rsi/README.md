# RSI Model - Import Guide

This directory contains the RSI (Relative Strength Index) model that can be imported and used in other repositories.

## Quick Import

### Method 1: Direct Import (Recommended)

```python
import sys
sys.path.append('/path/to/financial-analytics-models')

from financial_models.rsi import RSIModel

# Create model instance
rsi_model = RSIModel(period=14)

# Analyze a stock
data = rsi_model.analyze_stock("AAPL")
print(f"Latest RSI: {data['RSI'].iloc[-1]:.2f}")
```

### Method 2: Install as Package

```bash
# From the financial-analytics-models directory
pip install -e .
```

Then import:

```python
from financial_models.rsi import RSIModel
```

## Usage Examples

### Basic Usage

```python
from financial_models.rsi import RSIModel

# Initialize with default period (14)
rsi_model = RSIModel()

# Analyze a single stock
data = rsi_model.analyze_stock("GOOG")

# Get the latest RSI value
latest_rsi = data['RSI'].iloc[-1]
print(f"Current RSI: {latest_rsi:.2f}")
```

### Advanced Usage

```python
from financial_models.rsi import RSIModel

# Custom period for different sensitivity
rsi_model = RSIModel(period=21)  # Less sensitive

# Analyze multiple stocks
symbols = ["AAPL", "MSFT", "TSLA"]
results = {}

for symbol in symbols:
    data = rsi_model.analyze_stock(symbol)
    latest_rsi = data['RSI'].iloc[-1]

    # Determine trading signal
    if latest_rsi < 30:
        signal = "BUY (Oversold)"
    elif latest_rsi > 70:
        signal = "SELL (Overbought)"
    else:
        signal = "HOLD"

    results[symbol] = {
        'rsi': latest_rsi,
        'signal': signal
    }

    print(f"{symbol}: RSI {latest_rsi:.2f} - {signal}")
```

### Custom Data Period

```python
from financial_models.rsi import RSIModel

rsi_model = RSIModel(period=14)

# Get stock data for different periods
data_1y = rsi_model.get_stock_data("AAPL", period="1y")
data_6mo = rsi_model.get_stock_data("AAPL", period="6mo")
data_1mo = rsi_model.get_stock_data("AAPL", period="1mo")

# Calculate RSI for custom data
rsi_values = rsi_model.calculate_rsi(data_1y['Close'])
```

## Model Methods

### `RSIModel(period=14)`

- **period**: RSI calculation period (default: 14)

### `analyze_stock(symbol, period="1y")`

- **symbol**: Stock ticker symbol
- **period**: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- **Returns**: DataFrame with price data and RSI values

### `get_stock_data(symbol, period="1y")`

- **symbol**: Stock ticker symbol
- **period**: Data period
- **Returns**: DataFrame with OHLCV data

### `calculate_rsi(prices)`

- **prices**: Series of price data
- **Returns**: Series of RSI values

## Dependencies

The model requires these packages:

- `pandas>=2.0.0`
- `numpy>=1.24.0`
- `yfinance>=0.2.18`

## Error Handling

```python
from financial_models.rsi import RSIModel

try:
    rsi_model = RSIModel()
    data = rsi_model.analyze_stock("INVALID_SYMBOL")
except Exception as e:
    print(f"Error: {e}")
    # Handle the error appropriately
```

## Integration with Schedulers

```python
# For use in scheduled tasks
from financial_models.rsi import RSIModel

def daily_rsi_check():
    rsi_model = RSIModel()
    symbols = ["AAPL", "GOOG", "MSFT"]

    for symbol in symbols:
        data = rsi_model.analyze_stock(symbol)
        latest_rsi = data['RSI'].iloc[-1]

        if latest_rsi < 30:
            print(f"BUY signal for {symbol}")
        elif latest_rsi > 70:
            print(f"SELL signal for {symbol}")

# Run daily at 9 AM
# schedule.every().day.at("09:00").do(daily_rsi_check)
```

## Testing the Import

Run the example file to test the import:

```bash
python financial_models/rsi/example_import.py
```

This will demonstrate both basic and advanced usage of the RSI model.
