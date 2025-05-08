import pandas as pd
import numpy as np

class Portfolio:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.holdings = {}  # {symbol: quantity}
        self.trades = []    # List of trade records
        self.transaction_cost = 0.001  # 0.1% per trade
        self.portfolio_values = []  # Track portfolio values over time

    def execute_trade(self, symbol, price, signal, quantity=1):
        """Execute a buy or sell trade."""
        print(f"Attempting trade: {symbol}, signal={signal}, price={price}, quantity={quantity}")
        if signal == 1:  # Buy
            cost = price * quantity * (1 + self.transaction_cost)
            if self.cash >= cost:
                self.cash -= cost
                self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
                self.trades.append({"time": pd.Timestamp.now(), "symbol": symbol, "type": "buy", "price": price, "quantity": quantity})
                print(f"Buy successful: {quantity} shares of {symbol}")
                return True
            else:
                print(f"Buy failed: Insufficient cash ({self.cash} < {cost})")
        elif signal == -1:  # Sell
            if symbol in self.holdings and self.holdings[symbol] >= quantity:
                revenue = price * quantity * (1 - self.transaction_cost)
                self.cash += revenue
                self.holdings[symbol] -= quantity
                if self.holdings[symbol] == 0:
                    del self.holdings[symbol]
                self.trades.append({"time": pd.Timestamp.now(), "symbol": symbol, "type": "sell", "price": price, "quantity": quantity})
                print(f"Sell successful: {quantity} shares of {symbol}")
                return True
            else:
                print(f"Sell failed: Insufficient holdings for {symbol}")
        else:
            print(f"Invalid signal: {signal}")
        return False

    def get_portfolio_value(self, current_price, symbol="AAPL"):
        """Calculate total portfolio value and store it."""
        holdings_value = sum(qty * current_price for sym, qty in self.holdings.items() if sym == symbol)
        total_value = self.cash + holdings_value
        self.portfolio_values.append(total_value)
        return total_value

    def calculate_total_return(self):
        """Calculate total return as a percentage."""
        if not self.portfolio_values:
            return 0.0
        initial_value = self.portfolio_values[0]
        final_value = self.portfolio_values[-1]
        return ((final_value - initial_value) / initial_value) * 100

    def calculate_sharpe_ratio(self, risk_free_rate=0.01):
        """Calculate annualized Sharpe ratio."""
        if len(self.portfolio_values) < 2:
            return 0.0
        returns = pd.Series(self.portfolio_values).pct_change().dropna()
        if len(returns) == 0:
            return 0.0
        return (returns.mean() - risk_free_rate) / returns.std() * np.sqrt(252)

    def calculate_max_drawdown(self):
        """Calculate maximum drawdown as a percentage."""
        if not self.portfolio_values:
            return 0.0
        values = np.array(self.portfolio_values)
        peak = np.maximum.accumulate(values)
        drawdowns = (peak - values) / peak
        return np.max(drawdowns) * 100