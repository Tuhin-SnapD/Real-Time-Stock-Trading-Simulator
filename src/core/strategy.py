import pandas as pd
import numpy as np

class TradingStrategy:
    def __init__(self, short_window=5, long_window=20, profit_threshold=0.02, stop_loss=0.01):
        self.short_window = short_window
        self.long_window = long_window
        self.profit_threshold = profit_threshold  # 2% profit target
        self.stop_loss = stop_loss  # 1% stop loss
        self.previous_signal = 0
        self.entry_price = None
        self.position_open = False

    def generate_signals(self, data):
        """Generate buy/sell signals based on improved moving average crossover strategy."""
        if data.empty or len(data) < self.long_window:
            return pd.DataFrame()
        
        signals = pd.DataFrame(index=data.index)
        signals["price"] = data["Close"]
        
        # Calculate moving averages with better handling of NaN values
        signals["short_ma"] = data["Close"].rolling(window=self.short_window, min_periods=1).mean()
        signals["long_ma"] = data["Close"].rolling(window=self.long_window, min_periods=1).mean()
        
        # Calculate additional technical indicators
        signals["rsi"] = self.calculate_rsi(data["Close"], window=14)
        signals["volatility"] = data["Close"].rolling(window=20).std()
        
        # Calculate momentum indicators
        signals["price_momentum"] = data["Close"].pct_change(periods=3)
        signals["ma_momentum"] = signals["short_ma"].pct_change(periods=2)
        
        # Generate crossover signals with confirmation
        signals["crossover"] = 0
        signals["signal"] = 0
        
        # Detect crossovers more accurately
        for i in range(1, len(signals)):
            prev_short = signals["short_ma"].iloc[i-1]
            prev_long = signals["long_ma"].iloc[i-1]
            curr_short = signals["short_ma"].iloc[i]
            curr_long = signals["long_ma"].iloc[i]
            
            # Golden cross (short MA crosses above long MA)
            if prev_short <= prev_long and curr_short > curr_long:
                signals.loc[signals.index[i], "crossover"] = 1
            # Death cross (short MA crosses below long MA)
            elif prev_short >= prev_long and curr_short < curr_long:
                signals.loc[signals.index[i], "crossover"] = -1
        
        # Apply additional filters for better signal quality
        for i in range(len(signals)):
            current_price = signals["price"].iloc[i]
            rsi = signals["rsi"].iloc[i]
            volatility = signals["volatility"].iloc[i]
            crossover = signals["crossover"].iloc[i]
            price_momentum = signals["price_momentum"].iloc[i]
            ma_momentum = signals["ma_momentum"].iloc[i]
            
            # Buy signal conditions - more aggressive
            if (crossover == 1 and 
                rsi < 75 and  # Not extremely overbought
                self.previous_signal != 1 and  # No duplicate signals
                price_momentum > 0):  # Positive momentum
                
                signals.loc[signals.index[i], "signal"] = 1
                self.previous_signal = 1
                self.entry_price = current_price
                self.position_open = True
                
            # Alternative buy signal - when short MA is above long MA and momentum is positive
            elif (signals["short_ma"].iloc[i] > signals["long_ma"].iloc[i] and
                  rsi < 70 and
                  price_momentum > 0.01 and  # 1% positive momentum
                  ma_momentum > 0 and
                  self.previous_signal != 1 and
                  not self.position_open):
                
                signals.loc[signals.index[i], "signal"] = 1
                self.previous_signal = 1
                self.entry_price = current_price
                self.position_open = True
                
            # Sell signal conditions
            elif (crossover == -1 and 
                  rsi > 25 and  # Not extremely oversold
                  self.previous_signal != -1):  # No duplicate signals
                
                signals.loc[signals.index[i], "signal"] = -1
                self.previous_signal = -1
                self.position_open = False
                self.entry_price = None
                
            # Profit taking
            elif (self.position_open and 
                  self.entry_price and 
                  current_price >= self.entry_price * (1 + self.profit_threshold)):
                
                signals.loc[signals.index[i], "signal"] = -1
                self.previous_signal = -1
                self.position_open = False
                self.entry_price = None
                
            # Stop loss
            elif (self.position_open and 
                  self.entry_price and 
                  current_price <= self.entry_price * (1 - self.stop_loss)):
                
                signals.loc[signals.index[i], "signal"] = -1
                self.previous_signal = -1
                self.position_open = False
                self.entry_price = None
        
        # Clean up the signal column and remove temporary columns
        result_signals = signals[["price", "short_ma", "long_ma", "signal", "rsi"]].copy()
        
        print(f"Generated signals: {len(result_signals[result_signals['signal'] != 0])} trading signals")
        if not result_signals.empty:
            print(result_signals[["price", "short_ma", "long_ma", "signal", "rsi"]].tail())
        
        return result_signals

    def calculate_rsi(self, prices, window=14):
        """Calculate Relative Strength Index."""
        if len(prices) < window + 1:
            return pd.Series([np.nan] * len(prices), index=prices.index)
        
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def get_position_size(self, cash, price, risk_per_trade=0.02):
        """Calculate position size based on risk management."""
        if price <= 0:
            return 0
        
        # Risk 2% of portfolio per trade
        risk_amount = cash * risk_per_trade
        position_size = int(risk_amount / price)
        
        # Ensure we don't exceed available cash
        max_shares = int(cash / price)
        return min(position_size, max_shares)