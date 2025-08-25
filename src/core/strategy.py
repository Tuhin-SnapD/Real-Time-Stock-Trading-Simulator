import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SignalResult:
    """Container for signal generation results."""
    signals: pd.DataFrame
    buy_signals: int
    sell_signals: int
    total_signals: int
    success: bool
    error_message: Optional[str] = None

class TradingStrategy:
    """Optimized trading strategy with enhanced performance and error handling."""
    
    def __init__(self, short_window=5, long_window=20, profit_threshold=0.02, stop_loss=0.01, rsi_window=14):
        self.short_window = short_window
        self.long_window = long_window
        self.profit_threshold = profit_threshold
        self.stop_loss = stop_loss
        self.rsi_window = rsi_window
        self.previous_signal = 0
        self.entry_price = None
        self.position_open = False
        self._signal_cache = {}
        self._last_calculation_time = None
        
        # Validate parameters
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Validate strategy parameters."""
        if self.short_window >= self.long_window:
            raise ValueError("Short window must be less than long window")
        
        if self.short_window < 1 or self.long_window < 1:
            raise ValueError("Window sizes must be positive")
        
        if not (0 < self.profit_threshold < 1):
            raise ValueError("Profit threshold must be between 0 and 1")
        
        if not (0 < self.stop_loss < 1):
            raise ValueError("Stop loss must be between 0 and 1")
        
        if self.rsi_window < 1:
            raise ValueError("RSI window must be positive")
    
    def generate_signals(self, data: pd.DataFrame) -> SignalResult:
        """Generate buy/sell signals with improved performance and error handling."""
        try:
            if data.empty:
                return SignalResult(
                    signals=pd.DataFrame(),
                    buy_signals=0,
                    sell_signals=0,
                    total_signals=0,
                    success=False,
                    error_message="Empty data provided"
                )
            
            if len(data) < self.long_window:
                return SignalResult(
                    signals=pd.DataFrame(),
                    buy_signals=0,
                    sell_signals=0,
                    total_signals=0,
                    success=False,
                    error_message=f"Insufficient data. Need at least {self.long_window} points, got {len(data)}"
                )
            
            # Create signals DataFrame with optimized operations
            signals = self._create_signals_dataframe(data)
            
            # Calculate technical indicators efficiently
            signals = self._calculate_indicators(signals)
            
            # Generate trading signals
            signals = self._generate_trading_signals(signals)
            
            # Count signals
            buy_signals = len(signals[signals['signal'] == 1])
            sell_signals = len(signals[signals['signal'] == -1])
            total_signals = buy_signals + sell_signals
            
            logger.info(f"Generated {total_signals} signals ({buy_signals} buy, {sell_signals} sell)")
            
            return SignalResult(
                signals=signals,
                buy_signals=buy_signals,
                sell_signals=sell_signals,
                total_signals=total_signals,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error generating signals: {e}")
            return SignalResult(
                signals=pd.DataFrame(),
                buy_signals=0,
                sell_signals=0,
                total_signals=0,
                success=False,
                error_message=str(e)
            )
    
    def _create_signals_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create optimized signals DataFrame."""
        # Use only required columns to reduce memory usage
        required_columns = ["Close"]
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Data missing required columns. Available: {data.columns.tolist()}")
        
        signals = pd.DataFrame(index=data.index)
        signals["price"] = data["Close"].astype(float)
        
        return signals
    
    def _calculate_indicators(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators efficiently."""
        try:
            # Calculate moving averages with optimized rolling operations
            signals["short_ma"] = signals["price"].rolling(
                window=self.short_window, 
                min_periods=1
            ).mean()
            
            signals["long_ma"] = signals["price"].rolling(
                window=self.long_window, 
                min_periods=1
            ).mean()
            
            # Calculate RSI
            signals["rsi"] = self._calculate_rsi_optimized(signals["price"])
            
            # Calculate volatility (rolling standard deviation)
            signals["volatility"] = signals["price"].rolling(window=20).std()
            
            # Calculate momentum indicators
            signals["price_momentum"] = signals["price"].pct_change(periods=3)
            signals["ma_momentum"] = signals["short_ma"].pct_change(periods=2)
            
            # Fill NaN values with 0 for momentum indicators
            signals["price_momentum"] = signals["price_momentum"].fillna(0)
            signals["ma_momentum"] = signals["ma_momentum"].fillna(0)
            
            return signals
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            raise
    
    def _calculate_rsi_optimized(self, prices: pd.Series) -> pd.Series:
        """Calculate RSI with optimized performance."""
        try:
            if len(prices) < self.rsi_window + 1:
                return pd.Series([np.nan] * len(prices), index=prices.index)
            
            # Calculate price changes
            delta = prices.diff()
            
            # Separate gains and losses
            gains = delta.where(delta > 0, 0)
            losses = -delta.where(delta < 0, 0)
            
            # Calculate average gains and losses using exponential moving average
            avg_gains = gains.ewm(span=self.rsi_window, adjust=False).mean()
            avg_losses = losses.ewm(span=self.rsi_window, adjust=False).mean()
            
            # Calculate RS and RSI
            rs = avg_gains / avg_losses
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return pd.Series([np.nan] * len(prices), index=prices.index)
    
    def _generate_trading_signals(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals with improved logic."""
        try:
            # Initialize signal columns
            signals["crossover"] = 0
            signals["signal"] = 0
            
            # Detect crossovers efficiently using vectorized operations
            signals = self._detect_crossovers(signals)
            
            # Apply signal generation logic
            for i in range(len(signals)):
                current_price = signals["price"].iloc[i]
                rsi = signals["rsi"].iloc[i]
                crossover = signals["crossover"].iloc[i]
                price_momentum = signals["price_momentum"].iloc[i]
                ma_momentum = signals["ma_momentum"].iloc[i]
                
                # Buy signal conditions
                if self._should_buy(crossover, rsi, price_momentum, ma_momentum):
                    signals.loc[signals.index[i], "signal"] = 1
                    self.previous_signal = 1
                    self.entry_price = current_price
                    self.position_open = True
                    logger.debug(f"Buy signal generated at price ${current_price:.2f}")
                
                # Sell signal conditions
                elif self._should_sell(crossover, rsi, current_price):
                    signals.loc[signals.index[i], "signal"] = -1
                    self.previous_signal = -1
                    self.position_open = False
                    self.entry_price = None
                    logger.debug(f"Sell signal generated at price ${current_price:.2f}")
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating trading signals: {e}")
            raise
    
    def _detect_crossovers(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Detect moving average crossovers efficiently."""
        try:
            # Calculate crossover conditions
            short_above_long = signals["short_ma"] > signals["long_ma"]
            short_below_long = signals["short_ma"] < signals["long_ma"]
            
            # Detect crossovers using shift operations
            prev_short_above_long = short_above_long.shift(1)
            prev_short_below_long = short_below_long.shift(1)
            
            # Golden cross (short MA crosses above long MA)
            golden_cross = short_above_long & prev_short_below_long
            
            # Death cross (short MA crosses below long MA)
            death_cross = short_below_long & prev_short_above_long
            
            # Set crossover values
            signals.loc[golden_cross, "crossover"] = 1
            signals.loc[death_cross, "crossover"] = -1
            
            return signals
            
        except Exception as e:
            logger.error(f"Error detecting crossovers: {e}")
            raise
    
    def _should_buy(self, crossover: int, rsi: float, price_momentum: float, ma_momentum: float) -> bool:
        """Determine if a buy signal should be generated."""
        # Handle NaN values
        if pd.isna(rsi) or pd.isna(price_momentum) or pd.isna(ma_momentum):
            return False
        
        # Primary buy condition: golden cross
        if crossover == 1 and rsi < 75 and self.previous_signal != 1 and price_momentum > 0:
            return True
        
        # Secondary buy condition: momentum-based
        if (rsi < 70 and price_momentum > 0.01 and ma_momentum > 0 and 
            self.previous_signal != 1 and not self.position_open):
            return True
        
        return False
    
    def _should_sell(self, crossover: int, rsi: float, current_price: float) -> bool:
        """Determine if a sell signal should be generated."""
        # Handle NaN values
        if pd.isna(rsi) or pd.isna(current_price):
            return False
        
        # Death cross condition
        if crossover == -1 and rsi > 25 and self.previous_signal != -1:
            return True
        
        # Profit taking condition
        if (self.position_open and self.entry_price and 
            current_price >= self.entry_price * (1 + self.profit_threshold)):
            return True
        
        # Stop loss condition
        if (self.position_open and self.entry_price and 
            current_price <= self.entry_price * (1 - self.stop_loss)):
            return True
        
        return False
    
    def get_position_size(self, cash: float, price: float, risk_per_trade: float = 0.02) -> int:
        """Calculate position size based on risk management."""
        try:
            if price <= 0 or cash <= 0:
                return 0
            
            # Calculate minimum position size (at least 1 share)
            min_shares = 1
            
            # Risk 2% of portfolio per trade, but ensure minimum position
            risk_amount = cash * risk_per_trade
            position_size = int(risk_amount / price)
            
            # Ensure we don't exceed available cash
            max_shares = int(cash / price)
            
            # Use the larger of minimum shares or risk-based calculation
            final_size = max(min_shares, min(position_size, max_shares))
            
            # Ensure we have enough cash for at least 1 share
            if final_size * price > cash:
                final_size = max_shares
            
            logger.debug(f"Position size calculated: {final_size} shares (cash: ${cash}, price: ${price})")
            return final_size
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0
    
    def get_strategy_summary(self) -> Dict[str, Any]:
        """Get a summary of the current strategy state."""
        return {
            'short_window': self.short_window,
            'long_window': self.long_window,
            'profit_threshold': self.profit_threshold,
            'stop_loss': self.stop_loss,
            'rsi_window': self.rsi_window,
            'previous_signal': self.previous_signal,
            'entry_price': self.entry_price,
            'position_open': self.position_open,
            'cache_size': len(self._signal_cache)
        }
    
    def reset_strategy(self):
        """Reset strategy state."""
        self.previous_signal = 0
        self.entry_price = None
        self.position_open = False
        self._signal_cache.clear()
        self._last_calculation_time = None
        logger.info("Strategy state reset")
    
    def update_parameters(self, **kwargs):
        """Update strategy parameters with validation."""
        try:
            if 'short_window' in kwargs:
                self.short_window = kwargs['short_window']
            if 'long_window' in kwargs:
                self.long_window = kwargs['long_window']
            if 'profit_threshold' in kwargs:
                self.profit_threshold = kwargs['profit_threshold']
            if 'stop_loss' in kwargs:
                self.stop_loss = kwargs['stop_loss']
            if 'rsi_window' in kwargs:
                self.rsi_window = kwargs['rsi_window']
            
            # Validate updated parameters
            self._validate_parameters()
            
            # Clear cache when parameters change
            self._signal_cache.clear()
            
            logger.info(f"Strategy parameters updated: {kwargs}")
            
        except Exception as e:
            logger.error(f"Error updating strategy parameters: {e}")
            raise