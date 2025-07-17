#!/usr/bin/env python3
"""
RSI Strategy Backtesting - Signal Profitability Assessment

This script demonstrates how to assess whether RSI trading signals
would have been profitable using comprehensive backtesting.
"""

from rsi_backtesting import RSIBacktestModel
import pandas as pd


def main():
    """Run RSI backtesting on multiple stocks"""

    # Initialize the backtesting model
    print("Initializing RSI Backtesting Model...")
    backtest = RSIBacktestModel(period=14, initial_capital=10000)

    # Test stocks
    symbols = ["GOOG", "AAPL", "MSFT", "TSLA", "NVDA"]

    print(f"\nTesting RSI strategy on {len(symbols)} stocks...")
    print("=" * 60)

    results = {}

    for symbol in symbols:
        print(f"\n{'=' * 20} {symbol} {'=' * 20}")
        try:
            # Run backtest
            data, trades, metrics = backtest.backtest_strategy(symbol, period="1y")
            results[symbol] = metrics

            # Print key results
            print(f"Total Return: {metrics['Total_Return_Pct']:.2f}%")
            print(f"Buy & Hold Return: {metrics['Buy_Hold_Return_Pct']:.2f}%")
            print(f"Excess Return: {metrics['Excess_Return_Pct']:.2f}%")
            print(f"Win Rate: {metrics['Win_Rate_Pct']:.2f}%")
            print(f"Total Trades: {metrics['Total_Trades']}")
            print(f"Max Drawdown: {metrics['Max_Drawdown_Pct']:.2f}%")

            # Assess signal quality
            if metrics["Excess_Return_Pct"] > 0:
                print("✅ SIGNALS PROFITABLE: Strategy outperformed buy & hold")
            else:
                print("❌ SIGNALS UNPROFITABLE: Strategy underperformed buy & hold")

            if metrics["Win_Rate_Pct"] > 60:
                print("✅ GOOD WIN RATE: More than 60% of trades were profitable")
            elif metrics["Win_Rate_Pct"] < 40:
                print("❌ POOR WIN RATE: Less than 40% of trades were profitable")
            else:
                print("⚠️  MODERATE WIN RATE: Between 40-60% of trades were profitable")

        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            results[symbol] = None

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY OF SIGNAL PROFITABILITY")
    print("=" * 60)

    profitable_strategies = 0
    total_strategies = 0

    for symbol, metrics in results.items():
        if metrics is not None:
            total_strategies += 1
            if metrics["Excess_Return_Pct"] > 0:
                profitable_strategies += 1
                print(
                    f"✅ {symbol}: +{metrics['Excess_Return_Pct']:.2f}% excess return"
                )
            else:
                print(f"❌ {symbol}: {metrics['Excess_Return_Pct']:.2f}% excess return")

    print(
        f"\nOverall: {profitable_strategies}/{total_strategies} strategies were profitable"
    )

    if profitable_strategies / total_strategies > 0.6:
        print("🎯 CONCLUSION: RSI signals show good profitability potential")
    elif profitable_strategies / total_strategies < 0.4:
        print("⚠️  CONCLUSION: RSI signals show poor profitability potential")
    else:
        print("📊 CONCLUSION: RSI signals show mixed profitability potential")


if __name__ == "__main__":
    main()
