import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class RSIBacktestModel:
    def __init__(self, period=14, initial_capital=10000):
        self.period = period
        self.initial_capital = initial_capital

    def calculate_rsi(self, prices):
        """Calculate RSI for a series of prices"""
        # Calculate price changes
        delta = prices.diff()

        # Separate gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()

        # Calculate RS and RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def get_stock_data(self, symbol, period="1y"):
        """Fetch stock data"""
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data

    def generate_signals(self, rsi):
        """Generate buy/sell signals based on RSI"""
        signals = pd.Series(index=rsi.index, dtype="object")

        # Buy signals (RSI crosses above 30)
        signals.loc[(rsi.shift(1) < 30) & (rsi >= 30)] = "BUY"

        # Sell signals (RSI crosses below 70)
        signals.loc[(rsi.shift(1) > 70) & (rsi <= 70)] = "SELL"

        return signals

    def backtest_strategy(self, symbol, period="1y"):
        """Backtest the RSI strategy and calculate performance metrics"""
        # Get stock data
        data = self.get_stock_data(symbol, period)

        # Calculate RSI
        data["RSI"] = self.calculate_rsi(data["Close"])

        # Generate signals
        data["Signal"] = self.generate_signals(data["RSI"])

        # Initialize backtest variables
        data["Position"] = 0
        data["Cash"] = self.initial_capital
        data["Shares"] = 0
        data["Portfolio_Value"] = self.initial_capital

        # Track trades
        trades = []
        current_position = 0
        entry_price = 0
        entry_date = None

        # Simulate trading
        for i in range(1, len(data)):
            current_signal = data["Signal"].iloc[i]
            current_price = data["Close"].iloc[i]
            current_date = data.index[i]

            # Execute buy signal
            if current_signal == "BUY" and current_position == 0:
                shares_to_buy = data["Cash"].iloc[i - 1] / current_price
                data.loc[data.index[i], "Shares"] = shares_to_buy
                data.loc[data.index[i], "Cash"] = 0
                data.loc[data.index[i], "Position"] = 1
                current_position = 1
                entry_price = current_price
                entry_date = current_date

                trades.append(
                    {
                        "Entry_Date": entry_date,
                        "Entry_Price": entry_price,
                        "Shares": shares_to_buy,
                        "Type": "BUY",
                    }
                )

            # Execute sell signal
            elif current_signal == "SELL" and current_position == 1:
                shares_to_sell = data["Shares"].iloc[i - 1]
                cash_received = shares_to_sell * current_price
                data.loc[data.index[i], "Cash"] = cash_received
                data.loc[data.index[i], "Shares"] = 0
                data.loc[data.index[i], "Position"] = 0
                current_position = 0

                # Calculate trade profit/loss
                trade_pnl = (current_price - entry_price) * shares_to_sell

                trades.append(
                    {
                        "Exit_Date": current_date,
                        "Exit_Price": current_price,
                        "Trade_PnL": trade_pnl,
                        "Return_Pct": ((current_price - entry_price) / entry_price)
                        * 100,
                        "Type": "SELL",
                    }
                )

            # Carry forward position if no signal
            else:
                data.loc[data.index[i], "Cash"] = data["Cash"].iloc[i - 1]
                data.loc[data.index[i], "Shares"] = data["Shares"].iloc[i - 1]
                data.loc[data.index[i], "Position"] = current_position

            # Calculate portfolio value
            portfolio_value = data["Cash"].iloc[i] + (
                data["Shares"].iloc[i] * current_price
            )
            data.loc[data.index[i], "Portfolio_Value"] = portfolio_value

        # Calculate performance metrics
        performance_metrics = self.calculate_performance_metrics(data, trades)

        return data, trades, performance_metrics

    def calculate_performance_metrics(self, data, trades):
        """Calculate comprehensive performance metrics"""
        # Convert trades to DataFrame for easier analysis
        trades_df = pd.DataFrame(trades)

        # Basic metrics
        total_trades = len([t for t in trades if t["Type"] == "SELL"])
        winning_trades = len(
            [t for t in trades if t["Type"] == "SELL" and t["Trade_PnL"] > 0]
        )
        losing_trades = len(
            [t for t in trades if t["Type"] == "SELL" and t["Trade_PnL"] < 0]
        )

        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        # Calculate returns
        initial_value = self.initial_capital
        final_value = data["Portfolio_Value"].iloc[-1]
        total_return = ((final_value - initial_value) / initial_value) * 100

        # Buy and hold comparison
        buy_hold_return = (
            (data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0]
        ) * 100

        # Calculate trade statistics
        if len(trades_df) > 0:
            profitable_trades = trades_df[trades_df["Type"] == "SELL"]
            if len(profitable_trades) > 0:
                avg_win = profitable_trades[profitable_trades["Trade_PnL"] > 0][
                    "Trade_PnL"
                ].mean()
                avg_loss = profitable_trades[profitable_trades["Trade_PnL"] < 0][
                    "Trade_PnL"
                ].mean()
                max_win = profitable_trades["Trade_PnL"].max()
                max_loss = profitable_trades["Trade_PnL"].min()
                avg_return_pct = profitable_trades["Return_Pct"].mean()
            else:
                avg_win = avg_loss = max_win = max_loss = avg_return_pct = 0
        else:
            avg_win = avg_loss = max_win = max_loss = avg_return_pct = 0

        # Calculate drawdown
        data["Cumulative_Return"] = (
            data["Portfolio_Value"] - initial_value
        ) / initial_value
        data["Peak"] = data["Cumulative_Return"].expanding().max()
        data["Drawdown"] = (data["Cumulative_Return"] - data["Peak"]) * 100
        max_drawdown = data["Drawdown"].min()

        metrics = {
            "Total_Trades": total_trades,
            "Winning_Trades": winning_trades,
            "Losing_Trades": losing_trades,
            "Win_Rate_Pct": win_rate,
            "Total_Return_Pct": total_return,
            "Buy_Hold_Return_Pct": buy_hold_return,
            "Excess_Return_Pct": total_return - buy_hold_return,
            "Avg_Win": avg_win,
            "Avg_Loss": avg_loss,
            "Max_Win": max_win,
            "Max_Loss": max_loss,
            "Avg_Return_Pct": avg_return_pct,
            "Max_Drawdown_Pct": max_drawdown,
            "Final_Portfolio_Value": final_value,
            "Profit_Factor": abs(avg_win / avg_loss) if avg_loss != 0 else float("inf"),
        }

        return metrics

    def plot_backtest_results(self, symbol, period="1y"):
        """Plot comprehensive backtest results"""
        data, trades, metrics = self.backtest_strategy(symbol, period)

        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # Plot 1: Price and signals
        ax1.plot(data.index, data["Close"], label="Close Price", linewidth=2)

        # Plot buy/sell signals
        buy_signals = data[data["Signal"] == "BUY"]
        sell_signals = data[data["Signal"] == "SELL"]

        ax1.scatter(
            buy_signals.index,
            buy_signals["Close"],
            color="green",
            marker="^",
            s=100,
            label="Buy Signal",
        )
        ax1.scatter(
            sell_signals.index,
            sell_signals["Close"],
            color="red",
            marker="v",
            s=100,
            label="Sell Signal",
        )

        ax1.set_title(f"{symbol} Price with RSI Signals")
        ax1.set_ylabel("Price ($)")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: RSI
        ax2.plot(data.index, data["RSI"], color="purple", linewidth=2)
        ax2.axhline(y=70, color="r", linestyle="--", alpha=0.7, label="Overbought (70)")
        ax2.axhline(y=30, color="g", linestyle="--", alpha=0.7, label="Oversold (30)")
        ax2.axhline(y=50, color="gray", linestyle="-", alpha=0.5, label="Neutral (50)")

        ax2.set_title("RSI Oscillator")
        ax2.set_ylabel("RSI")
        ax2.set_ylim(0, 100)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Plot 3: Portfolio value vs buy and hold
        buy_hold_value = self.initial_capital * (data["Close"] / data["Close"].iloc[0])
        ax3.plot(data.index, data["Portfolio_Value"], label="RSI Strategy", linewidth=2)
        ax3.plot(data.index, buy_hold_value, label="Buy & Hold", linewidth=2, alpha=0.7)
        ax3.set_title("Portfolio Value Comparison")
        ax3.set_ylabel("Portfolio Value ($)")
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # Plot 4: Drawdown
        ax4.fill_between(data.index, data["Drawdown"], 0, alpha=0.3, color="red")
        ax4.plot(data.index, data["Drawdown"], color="red", linewidth=1)
        ax4.set_title("Drawdown")
        ax4.set_ylabel("Drawdown (%)")
        ax4.set_xlabel("Date")
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        # Print performance summary
        self.print_performance_summary(metrics, trades)

        return data, trades, metrics

    def print_performance_summary(self, metrics, trades):
        """Print detailed performance summary"""
        print("=" * 60)
        print("RSI STRATEGY BACKTEST RESULTS")
        print("=" * 60)
        print(f"Total Trades: {metrics['Total_Trades']}")
        print(f"Winning Trades: {metrics['Winning_Trades']}")
        print(f"Losing Trades: {metrics['Losing_Trades']}")
        print(f"Win Rate: {metrics['Win_Rate_Pct']:.2f}%")
        print(f"Total Return: {metrics['Total_Return_Pct']:.2f}%")
        print(f"Buy & Hold Return: {metrics['Buy_Hold_Return_Pct']:.2f}%")
        print(f"Excess Return: {metrics['Excess_Return_Pct']:.2f}%")
        print(f"Average Win: ${metrics['Avg_Win']:.2f}")
        print(f"Average Loss: ${metrics['Avg_Loss']:.2f}")
        print(f"Max Win: ${metrics['Max_Win']:.2f}")
        print(f"Max Loss: ${metrics['Max_Loss']:.2f}")
        print(f"Average Return per Trade: {metrics['Avg_Return_Pct']:.2f}%")
        print(f"Max Drawdown: {metrics['Max_Drawdown_Pct']:.2f}%")
        print(f"Profit Factor: {metrics['Profit_Factor']:.2f}")
        print(f"Final Portfolio Value: ${metrics['Final_Portfolio_Value']:.2f}")
        print("=" * 60)

        # Print individual trades
        if trades:
            print("\nINDIVIDUAL TRADES:")
            print("-" * 60)
            for i, trade in enumerate(trades):
                if trade["Type"] == "SELL":
                    print(
                        f"Trade {i // 2 + 1}: {trade['Entry_Date'].strftime('%Y-%m-%d')} → "
                        f"{trade['Exit_Date'].strftime('%Y-%m-%d')} | "
                        f"${trade['Entry_Price']:.2f} → ${trade['Exit_Price']:.2f} | "
                        f"PnL: ${trade['Trade_PnL']:.2f} ({trade['Return_Pct']:.2f}%)"
                    )


# Example usage
if __name__ == "__main__":
    # Initialize the backtest model
    backtest = RSIBacktestModel(period=14, initial_capital=10000)

    # Run backtest on multiple stocks
    symbols = ["GOOG", "AAPL", "MSFT", "TSLA"]

    for symbol in symbols:
        print(f"\n{'=' * 20} {symbol} {'=' * 20}")
        data, trades, metrics = backtest.plot_backtest_results(symbol, period="1y")
