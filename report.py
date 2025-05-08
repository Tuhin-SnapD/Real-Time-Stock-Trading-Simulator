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
            portfolio.portfolio_values = [float(line.strip()) for line in f if line.strip()]
        print(f"Loaded {len(portfolio.portfolio_values)} portfolio values")
    except FileNotFoundError:
        portfolio_values_status = "Warning: portfolio_values.txt not found. Run the simulator first."
    except ValueError:
        portfolio_values_status = "Warning: Invalid data in portfolio_values.txt."
    else:
        portfolio_values_status = f"Portfolio values loaded: {len(portfolio.portfolio_values)} entries"

    # Load trades from database
    trades = db.get_trades()
    trades_status = "No trades found in database. Run the simulator during US market hours (7:00 PM–1:30 AM IST)." if trades.empty else f"Found {len(trades)} trades"

    # Calculate metrics
    total_return = portfolio.calculate_total_return()
    sharpe_ratio = portfolio.calculate_sharpe_ratio()
    max_drawdown = portfolio.calculate_max_drawdown()

    # Trade statistics
    total_trades = len(trades)
    buy_trades = len(trades[trades["type"] == "buy"]) if not trades.empty else 0
    sell_trades = len(trades[trades["type"] == "sell"]) if not trades.empty else 0
    avg_trade_price = trades["price"].mean() if not trades.empty else 0.0

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
{trades[['time', 'symbol', 'type', 'price', 'quantity']].to_string(index=False) if not trades.empty else "No trades available."}
    """
    return report

if __name__ == "__main__":
    report = generate_performance_report()
    print(report)
    # Save report to file
    with open("performance_report.txt", "w") as f:
        f.write(report)