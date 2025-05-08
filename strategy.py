import pandas as pd

class TradingStrategy:
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        """Generate buy/sell signals based on moving average crossover."""
        signals = pd.DataFrame(index=data.index)
        signals["price"] = data["Close"]
        
        # Calculate moving averages
        signals["short_ma"] = data["Close"].rolling(window=self.short_window).mean()
        signals["long_ma"] = data["Close"].rolling(window=self.long_window).mean()
        
        # Generate signals: 1 for buy, -1 for sell, 0 for hold
        signals["signal"] = 0
        signals["signal"] = signals["short_ma"].gt(signals["long_ma"]).astype(int)
        signals["signal"] = signals["signal"].diff().fillna(0)
        signals["signal"] = signals["signal"].replace({1: 1, -1: -1, 0: 0})
        
        return signals[["price", "short_ma", "long_ma", "signal"]]