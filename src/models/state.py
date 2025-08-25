import threading
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

class SimulatorState:
    """Thread-safe state management for the trading simulator."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self._current_data = pd.DataFrame()
        self._current_signals = pd.DataFrame()
        self._portfolio_values: List[float] = []
        self._trades_list: List[Dict[str, Any]] = []
        self._is_simulator_running = False
        self._simulator_thread: Optional[threading.Thread] = None
        self._global_initial_cash = 5000.0
        self._current_symbol = "AAPL"
        self._current_interval = "1m"
        self._current_period = "1d"
        self._logger = logging.getLogger(__name__)
    
    @property
    def current_data(self) -> pd.DataFrame:
        """Get current stock data."""
        with self._lock:
            return self._current_data.copy()
    
    @current_data.setter
    def current_data(self, data: pd.DataFrame):
        """Set current stock data."""
        with self._lock:
            self._current_data = data.copy() if not data.empty else pd.DataFrame()
    
    @property
    def current_signals(self) -> pd.DataFrame:
        """Get current trading signals."""
        with self._lock:
            return self._current_signals.copy()
    
    @current_signals.setter
    def current_signals(self, signals: pd.DataFrame):
        """Set current trading signals."""
        with self._lock:
            self._current_signals = signals.copy() if not signals.empty else pd.DataFrame()
    
    @property
    def portfolio_values(self) -> List[float]:
        """Get portfolio value history."""
        with self._lock:
            return self._portfolio_values.copy()
    
    def add_portfolio_value(self, value: float):
        """Add a new portfolio value."""
        with self._lock:
            self._portfolio_values.append(value)
            # Keep only the last 100 values to prevent memory issues
            if len(self._portfolio_values) > 100:
                self._portfolio_values.pop(0)
    
    def clear_portfolio_values(self):
        """Clear portfolio value history."""
        with self._lock:
            self._portfolio_values.clear()
    
    @property
    def trades_list(self) -> List[Dict[str, Any]]:
        """Get trade history."""
        with self._lock:
            return self._trades_list.copy()
    
    def add_trade(self, trade: Dict[str, Any]):
        """Add a new trade."""
        with self._lock:
            self._trades_list.append(trade.copy())
            self._logger.info(f"Added trade: {trade}")
    
    def clear_trades(self):
        """Clear trade history."""
        with self._lock:
            self._trades_list.clear()
            self._logger.info("Cleared all trades")
    
    @property
    def is_simulator_running(self) -> bool:
        """Check if simulator is running."""
        with self._lock:
            return self._is_simulator_running
    
    @is_simulator_running.setter
    def is_simulator_running(self, running: bool):
        """Set simulator running state."""
        with self._lock:
            self._is_simulator_running = running
            self._logger.info(f"Simulator running state changed to: {running}")
    
    @property
    def simulator_thread(self) -> Optional[threading.Thread]:
        """Get simulator thread."""
        with self._lock:
            return self._simulator_thread
    
    @simulator_thread.setter
    def simulator_thread(self, thread: Optional[threading.Thread]):
        """Set simulator thread."""
        with self._lock:
            self._simulator_thread = thread
    
    @property
    def global_initial_cash(self) -> float:
        """Get initial cash amount."""
        with self._lock:
            return self._global_initial_cash
    
    @global_initial_cash.setter
    def global_initial_cash(self, cash: float):
        """Set initial cash amount."""
        with self._lock:
            self._global_initial_cash = cash
            self._logger.info(f"Initial cash set to: ${cash}")
    
    @property
    def current_symbol(self) -> str:
        """Get current trading symbol."""
        with self._lock:
            return self._current_symbol
    
    @current_symbol.setter
    def current_symbol(self, symbol: str):
        """Set current trading symbol."""
        with self._lock:
            self._current_symbol = symbol
            self._logger.info(f"Trading symbol changed to: {symbol}")
    
    @property
    def current_interval(self) -> str:
        """Get current data interval."""
        with self._lock:
            return self._current_interval
    
    @current_interval.setter
    def current_interval(self, interval: str):
        """Set current data interval."""
        with self._lock:
            self._current_interval = interval
            self._logger.info(f"Data interval changed to: {interval}")
    
    @property
    def current_period(self) -> str:
        """Get current data period."""
        with self._lock:
            return self._current_period
    
    @current_period.setter
    def current_period(self, period: str):
        """Set current data period."""
        with self._lock:
            self._current_period = period
            self._logger.info(f"Data period changed to: {period}")
    
    def reset_state(self):
        """Reset all state to initial values."""
        with self._lock:
            self._current_data = pd.DataFrame()
            self._current_signals = pd.DataFrame()
            self._portfolio_values.clear()
            self._trades_list.clear()
            self._is_simulator_running = False
            self._simulator_thread = None
            self._global_initial_cash = 5000.0
            self._current_symbol = "AAPL"
            self._current_interval = "1m"
            self._current_period = "1d"
            self._logger.info("Simulator state reset")
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get a summary of the current state."""
        with self._lock:
            return {
                'is_running': self._is_simulator_running,
                'symbol': self._current_symbol,
                'interval': self._current_interval,
                'period': self._current_period,
                'initial_cash': self._global_initial_cash,
                'data_points': len(self._current_data),
                'signals_count': len(self._current_signals),
                'portfolio_values_count': len(self._portfolio_values),
                'trades_count': len(self._trades_list),
                'current_portfolio_value': self._portfolio_values[-1] if self._portfolio_values else self._global_initial_cash
            }

# Global state instance
simulator_state = SimulatorState()

def get_simulator_state() -> SimulatorState:
    """Get the global simulator state instance."""
    return simulator_state

