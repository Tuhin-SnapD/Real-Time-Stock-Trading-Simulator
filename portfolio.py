class Portfolio:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.holdings = {}  # {symbol: quantity}
        self.trades = []    # List of trade records
        self.transaction_cost = 0.001  # 0.1% per trade

    def execute_trade(self, symbol, price, signal, quantity=1):
        """Execute a buy or sell trade."""
        if signal == 1:  # Buy
            cost = price * quantity * (1 + self.transaction_cost)
            if self.cash >= cost:
                self.cash -= cost
                self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
                self.trades.append({"time": pd.Timestamp.now(), "symbol": symbol, "type": "buy", "price": price, "quantity": quantity})
                return True
        elif signal == -1:  # Sell
            if symbol in self.holdings and self.holdings[symbol] >= quantity:
                revenue = price * quantity * (1 - self.transaction_cost)
                self.cash += revenue
                self.holdings[symbol] -= quantity
                if self.holdings[symbol] == 0:
                    del self.holdings[symbol]
                self.trades.append({"time": pd.Timestamp.now(), "symbol": symbol, "type": "sell", "price": price, "quantity": quantity})
                return True
        return False

    def get_portfolio_value(self, current_price, symbol="AAPL"):
        """Calculate total portfolio value."""
        holdings_value = sum(qty * current_price for sym, qty in self.holdings.items() if sym == symbol)
        return self.cash + holdings_value