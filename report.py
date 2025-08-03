import pandas as pd
from portfolio import Portfolio
from database import TradeDatabase

def generate_performance_report(symbol="AAPL", initial_cash=50000):
    """Generate a performance report with key metrics."""
    # Initialize portfolio and database
    portfolio = Portfolio(initial_cash=initial_cash)
    db = TradeDatabase()

    # Load portfolio values from file
    try:
        with open("portfolio_values.txt", "r") as f:
            portfolio_values_raw = [line.strip() for line in f if line.strip()]
            portfolio.portfolio_values = [float(value) for value in portfolio_values_raw if value.replace('.', '').replace('-', '').isdigit()]
        print(f"Loaded {len(portfolio.portfolio_values)} portfolio values")
        portfolio_values_status = f"Portfolio values loaded: {len(portfolio.portfolio_values)} entries"
    except FileNotFoundError:
        portfolio.portfolio_values = []
        portfolio_values_status = "Warning: portfolio_values.txt not found. Run the simulator first."
    except ValueError as e:
        portfolio.portfolio_values = []
        portfolio_values_status = f"Warning: Invalid data in portfolio_values.txt: {e}"
    except Exception as e:
        portfolio.portfolio_values = []
        portfolio_values_status = f"Warning: Error reading portfolio_values.txt: {e}"

    # Load trades from database
    try:
        trades = db.get_trades()
        trades_status = "No trades found in database. Run the simulator during US market hours (7:00 PM–1:30 AM IST)." if trades.empty else f"Found {len(trades)} trades"
    except Exception as e:
        trades = pd.DataFrame()
        trades_status = f"Error loading trades from database: {e}"

    # Calculate metrics with error handling
    try:
        total_return = portfolio.calculate_total_return()
    except Exception as e:
        total_return = 0.0
        print(f"Error calculating total return: {e}")
    
    try:
        sharpe_ratio = portfolio.calculate_sharpe_ratio()
    except Exception as e:
        sharpe_ratio = 0.0
        print(f"Error calculating Sharpe ratio: {e}")
    
    try:
        max_drawdown = portfolio.calculate_max_drawdown()
    except Exception as e:
        max_drawdown = 0.0
        print(f"Error calculating max drawdown: {e}")

    # Trade statistics
    total_trades = len(trades)
    buy_trades = len(trades[trades["type"] == "buy"]) if not trades.empty else 0
    sell_trades = len(trades[trades["type"] == "sell"]) if not trades.empty else 0
    avg_trade_price = trades["price"].mean() if not trades.empty and "price" in trades.columns else 0.0

    # Generate report
    report = f"""
Performance Report for {symbol}
{'=' * 40}
Initial Cash: ${initial_cash:.2f}
{portfolio_values_status}
{trades_status}
Total Trades: {total_trades}
Buy Trades: {buy_trades}
Sell Trades: {sell_trades}
Average Trade Price: ${avg_trade_price:.2f}
Total Return: {total_return:.2f}%
Sharpe Ratio: {sharpe_ratio:.2f}
Max Drawdown: {max_drawdown:.2f}%
{'=' * 40}
Trade Summary:
{trades[['time', 'symbol', 'type', 'price', 'quantity']].to_string(index=False) if not trades.empty and all(col in trades.columns for col in ['time', 'symbol', 'type', 'price', 'quantity']) else "No trades available."}
    """
    return report

if __name__ == "__main__":
    report = generate_performance_report()
    print(report)
    # Save report to file
    with open("performance_report.txt", "w") as f:
        f.write(report)