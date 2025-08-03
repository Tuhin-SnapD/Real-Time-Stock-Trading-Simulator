import asyncio
import argparse
import pandas as pd
from data_fetcher import DataFetcher
from strategy import TradingStrategy
from portfolio import Portfolio
from database import TradeDatabase
from visualizer import plot_results

async def run_simulator_async(symbol="AAPL", interval="1m", period="1d", initial_cash=50000, max_iterations=100):
    fetcher = DataFetcher(symbol=symbol, interval=interval, period=period)
    strategy = TradingStrategy(short_window=2, long_window=5)  # Sensitive for faster signals
    portfolio = Portfolio(initial_cash=initial_cash)
    db = TradeDatabase()

    portfolio_values = []

    # Clear portfolio_values.txt at the start of simulation
    with open("portfolio_values.txt", "w") as f:
        f.write("")

    iteration = 0
    while iteration < max_iterations:
        try:
            # Reset fetcher cache to force fresh data
            fetcher.last_data = pd.DataFrame()
            fetcher.last_fetch_time = None

            # Fetch data
            data = fetcher.get_real_time_data()
            print(f"Iteration {iteration}: Data received with {len(data)} rows")
            if data.empty:
                print("No data received. Retrying...")
                await asyncio.sleep(60)
                continue

            # Validate data has required columns
            required_columns = ["Open", "High", "Low", "Close", "Volume"]
            if not all(col in data.columns for col in required_columns):
                print(f"Data missing required columns. Available: {data.columns.tolist()}")
                await asyncio.sleep(60)
                continue

            # Generate signals
            signals = strategy.generate_signals(data)
            if signals.empty:
                print("No signals generated. Retrying...")
                await asyncio.sleep(60)
                continue
                
            latest_signal = int(signals["signal"].iloc[-1])  # Ensure integer signal
            latest_price = signals["price"].iloc[-1]
            
            # Validate price is reasonable
            if latest_price <= 0 or pd.isna(latest_price):
                print(f"Invalid price: {latest_price}. Retrying...")
                await asyncio.sleep(60)
                continue
                
            print(f"Latest signal: {latest_signal}, Latest price: {latest_price}")
            print(f"Signal details: {signals[['price', 'short_ma', 'long_ma', 'signal']].tail(5)}")

            # Execute trades
            if latest_signal != 0:
                success = portfolio.execute_trade(symbol, latest_price, latest_signal)
                if success:
                    trade = {
                        "time": pd.Timestamp.now().isoformat(),  # Convert Timestamp to string
                        "symbol": symbol,
                        "type": "buy" if latest_signal == 1 else "sell",
                        "price": latest_price,
                        "quantity": 1
                    }
                    db.save_trade(trade)
                    print(f"Executed {trade['type']} for {symbol} at {latest_price}")
                else:
                    print(f"Trade failed for signal {latest_signal} at price {latest_price}")
            else:
                print("No trade signal (signal=0)")

            # Track portfolio value
            portfolio_value = portfolio.get_portfolio_value(latest_price)
            portfolio_values.append(portfolio_value)
            print(f"Portfolio value: ${portfolio_value:.2f}, Holdings: {portfolio.holdings}")

            # Save portfolio value to file
            with open("portfolio_values.txt", "a") as f:
                f.write(f"{portfolio_value}\n")

            iteration += 1
            if iteration >= max_iterations:
                print(f"Stopping after {max_iterations} iterations")
                plot_results(signals, portfolio_values, symbol)
                break

            await asyncio.sleep(60)  # Wait 1 minute for real-time data

        except Exception as e:
            print(f"Error in simulator loop: {e}")
            import traceback
            traceback.print_exc()
            await asyncio.sleep(60)  # Wait before retrying

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Real-Time Stock Trading Simulator")
    parser.add_argument("--symbol", default="AAPL", help="Stock symbol (e.g., AAPL)")
    parser.add_argument("--interval", default="1m", help="Data interval (e.g., 1m, 5m)")
    parser.add_argument("--period", default="1d", help="Data period (e.g., 1d, 5d, 1mo)")
    parser.add_argument("--cash", type=float, default=50000, help="Initial cash balance")
    parser.add_argument("--iterations", type=int, default=100, help="Max iterations")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_simulator_async(args.symbol, args.interval, args.period, args.cash))