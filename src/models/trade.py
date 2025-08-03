from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Trade:
    """Represents a single trade in the simulator."""
    
    time: datetime
    symbol: str
    type: str  # 'buy' or 'sell'
    price: float
    quantity: int
    
    def __post_init__(self):
        """Validate trade data after initialization."""
        if self.type not in ['buy', 'sell']:
            raise ValueError("Trade type must be 'buy' or 'sell'")
        
        if self.price <= 0:
            raise ValueError("Price must be positive")
        
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
    
    def to_dict(self) -> dict:
        """Convert trade to dictionary for JSON serialization."""
        return {
            'time': self.time.isoformat(),
            'symbol': self.symbol,
            'type': self.type,
            'price': self.price,
            'quantity': self.quantity,
            'total_value': self.price * self.quantity
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Trade':
        """Create trade from dictionary."""
        return cls(
            time=datetime.fromisoformat(data['time']),
            symbol=data['symbol'],
            type=data['type'],
            price=float(data['price']),
            quantity=int(data['quantity'])
        )

@dataclass
class PortfolioSnapshot:
    """Represents a portfolio snapshot at a point in time."""
    
    timestamp: datetime
    cash: float
    shares_held: int
    share_price: float
    total_value: float
    
    def __post_init__(self):
        """Calculate total value if not provided."""
        if self.total_value == 0:
            self.total_value = self.cash + (self.shares_held * self.share_price)
    
    def to_dict(self) -> dict:
        """Convert portfolio snapshot to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'cash': self.cash,
            'shares_held': self.shares_held,
            'share_price': self.share_price,
            'total_value': self.total_value
        } 