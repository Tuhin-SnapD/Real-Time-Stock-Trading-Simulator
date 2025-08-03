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
        
        # Create crossover signals
        # When short MA crosses above long MA: buy signal (1)
        # When short MA crosses below long MA: sell signal (-1)
        signals["crossover"] = (signals["short_ma"] > signals["long_ma"]).astype(int)
        signals["signal"] = signals["crossover"].diff().fillna(0)
        
        # Clean up the signal column
        signals = signals.drop("crossover", axis=1)
        
        print(signals[["price", "short_ma", "long_ma", "signal"]].tail())
        return signals[["price", "short_ma", "long_ma", "signal"]]