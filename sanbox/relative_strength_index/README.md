# RSI Strategy Backtesting - Signal Profitability Assessment

This project provides a comprehensive backtesting framework to assess whether RSI (Relative Strength Index) trading signals would have been profitable in historical market conditions.

## Overview

The RSI strategy generates:

- **Buy signals**: When RSI crosses above 30 (oversold condition)
- **Sell signals**: When RSI crosses below 70 (overbought condition)

## Key Files

- `rsi_backtesting.py` - Main backtesting model with comprehensive performance analysis
- `run_backtest.py` - Simple script to run backtests on multiple stocks
- `rsi_backtest_demo.ipynb` - Jupyter notebook with detailed examples
- `requirements.txt` - Required Python packages

## Installation

1. **Set up virtual environment** (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Run the script

```bash
python run_backtest.py
```

### Option 2: Use in Jupyter notebook

```python
from rsi_backtesting import RSIBacktestModel

# Initialize model
backtest = RSIBacktestModel(period=14, initial_capital=10000)

# Run backtest on a single stock
data, trades, metrics = backtest.plot_backtest_results('GOOG', period="1y")
```

### Option 3: Custom analysis

```python
from rsi_backtesting import RSIBacktestModel

# Initialize with custom parameters
backtest = RSIBacktestModel(period=14, initial_capital=10000)

# Run backtest without plotting
data, trades, metrics = backtest.backtest_strategy('AAPL', period="1y")

# Access results
print(f"Total Return: {metrics['Total_Return_Pct']:.2f}%")
print(f"Win Rate: {metrics['Win_Rate_Pct']:.2f}%")
print(f"Total Trades: {metrics['Total_Trades']}")
```

## Performance Metrics Explained

### Key Profitability Indicators:

1. **Total Return (%)**: Overall strategy performance
2. **Buy & Hold Return (%)**: Performance of simply buying and holding
3. **Excess Return (%)**: Difference between strategy and buy & hold returns
4. **Win Rate (%)**: Percentage of profitable trades
5. **Total Trades**: Number of completed buy-sell cycles
6. **Max Drawdown (%)**: Maximum peak-to-trough decline
7. **Profit Factor**: Ratio of average win to average loss

### Signal Assessment Criteria:

#### ✅ **Good Signals** (Profitable):

- Win Rate > 60%
- Positive Excess Return
- Low Max Drawdown (< 15%)
- Profit Factor > 1.5

#### ❌ **Poor Signals** (Unprofitable):

- Win Rate < 40%
- Negative Excess Return
- High Max Drawdown (> 25%)
- Profit Factor < 1.0

#### ⚠️ **Mixed Signals**:

- Win Rate 40-60%
- Small positive/negative excess return
- Moderate drawdown

## Example Output

```
============================================================
RSI STRATEGY BACKTEST RESULTS
============================================================
Total Trades: 8
Winning Trades: 5
Losing Trades: 3
Win Rate: 62.50%
Total Return: 15.23%
Buy & Hold Return: 12.45%
Excess Return: 2.78%
Average Win: $245.67
Average Loss: $156.89
Max Win: $456.78
Max Loss: $234.56
Average Return per Trade: 3.45%
Max Drawdown: 8.92%
Profit Factor: 1.57
Final Portfolio Value: $11,523.45
============================================================
```

## Strategy Optimization Ideas

1. **Dynamic RSI Levels**: Adjust overbought/oversold levels based on market volatility
2. **Multiple Timeframes**: Combine RSI signals from different time periods
3. **Confirmation Signals**: Use additional indicators (moving averages, volume)
4. **Risk Management**: Implement stop losses and position sizing
5. **Market Regime Detection**: Adjust strategy based on trending vs ranging markets

## Limitations

- **Past Performance**: Historical results don't guarantee future performance
- **Transaction Costs**: Real trading includes commissions and slippage
- **Market Conditions**: RSI works better in trending markets than sideways markets
- **Look-ahead Bias**: Backtesting uses perfect hindsight for signal generation

## Virtual Environment Setup

To select the right virtual environment for running Jupyter notebooks:

1. **Activate your virtual environment**:

   ```bash
   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Install Jupyter in the virtual environment**:

   ```bash
   pip install jupyter
   ```

3. **Launch Jupyter**:

   ```bash
   jupyter notebook
   ```

4. **Verify the kernel**: In Jupyter, check that the kernel shows your virtual environment name

## Troubleshooting

- **Import errors**: Make sure you're in the correct virtual environment
- **Data download issues**: Check internet connection for yfinance data
- **Plotting issues**: Ensure matplotlib is properly installed
- **Memory issues**: Reduce the number of stocks or time period for testing

## Contributing

Feel free to extend the model with:

- Additional technical indicators
- More sophisticated risk management
- Portfolio-level analysis
- Real-time signal generation
