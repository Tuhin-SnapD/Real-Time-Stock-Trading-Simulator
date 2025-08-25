import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class InputValidator:
    """Input validation utilities for the trading simulator."""
    
    # Valid stock symbols (basic pattern)
    SYMBOL_PATTERN = re.compile(r'^[A-Z]{1,5}$')
    
    # Valid intervals
    VALID_INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    
    # Valid periods
    VALID_PERIODS = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    
    # Available stocks for validation
    AVAILABLE_STOCKS = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
        'AMD', 'INTC', 'CRM', 'ORCL', 'ADBE', 'PYPL', 'UBER', 'LYFT',
        'SPOT', 'ZM', 'SQ', 'SHOP', 'ROKU', 'PINS', 'SNAP', 'TWTR',
        'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'JNJ', 'PFE', 'UNH',
        'HD', 'DIS', 'V', 'MA', 'PG', 'KO', 'PEP', 'WMT', 'COST'
    ]
    
    @classmethod
    def validate_symbol(cls, symbol: str) -> str:
        """Validate and sanitize stock symbol."""
        if not symbol:
            raise ValidationError("Stock symbol cannot be empty")
        
        # Convert to uppercase and strip whitespace
        symbol = symbol.strip().upper()
        
        # Check basic pattern
        if not cls.SYMBOL_PATTERN.match(symbol):
            raise ValidationError(f"Invalid stock symbol format: {symbol}")
        
        # Check if symbol is in available list
        if symbol not in cls.AVAILABLE_STOCKS:
            logger.warning(f"Symbol {symbol} not in available stocks list")
        
        return symbol
    
    @classmethod
    def validate_interval(cls, interval: str) -> str:
        """Validate data interval."""
        if not interval:
            raise ValidationError("Interval cannot be empty")
        
        interval = interval.strip().lower()
        
        if interval not in cls.VALID_INTERVALS:
            raise ValidationError(f"Invalid interval: {interval}. Valid intervals: {cls.VALID_INTERVALS}")
        
        return interval
    
    @classmethod
    def validate_period(cls, period: str) -> str:
        """Validate data period."""
        if not period:
            raise ValidationError("Period cannot be empty")
        
        period = period.strip().lower()
        
        if period not in cls.VALID_PERIODS:
            raise ValidationError(f"Invalid period: {period}. Valid periods: {cls.VALID_PERIODS}")
        
        return period
    
    @classmethod
    def validate_initial_cash(cls, cash: Any) -> float:
        """Validate initial cash amount."""
        try:
            cash_float = float(cash)
        except (ValueError, TypeError):
            raise ValidationError("Initial cash must be a valid number")
        
        if cash_float <= 0:
            raise ValidationError("Initial cash must be positive")
        
        if cash_float > 1000000:  # $1M limit
            raise ValidationError("Initial cash cannot exceed $1,000,000")
        
        return round(cash_float, 2)
    
    @classmethod
    def validate_short_window(cls, window: Any) -> int:
        """Validate short moving average window."""
        try:
            window_int = int(window)
        except (ValueError, TypeError):
            raise ValidationError("Short window must be a valid integer")
        
        if window_int < 1:
            raise ValidationError("Short window must be at least 1")
        
        if window_int > 50:
            raise ValidationError("Short window cannot exceed 50")
        
        return window_int
    
    @classmethod
    def validate_long_window(cls, window: Any, short_window: int) -> int:
        """Validate long moving average window."""
        try:
            window_int = int(window)
        except (ValueError, TypeError):
            raise ValidationError("Long window must be a valid integer")
        
        if window_int < 1:
            raise ValidationError("Long window must be at least 1")
        
        if window_int > 200:
            raise ValidationError("Long window cannot exceed 200")
        
        if window_int <= short_window:
            raise ValidationError("Long window must be greater than short window")
        
        return window_int
    
    @classmethod
    def validate_profit_threshold(cls, threshold: Any) -> float:
        """Validate profit threshold."""
        try:
            threshold_float = float(threshold)
        except (ValueError, TypeError):
            raise ValidationError("Profit threshold must be a valid number")
        
        if threshold_float <= 0:
            raise ValidationError("Profit threshold must be positive")
        
        if threshold_float > 0.5:  # 50% limit
            raise ValidationError("Profit threshold cannot exceed 50%")
        
        return round(threshold_float, 4)
    
    @classmethod
    def validate_stop_loss(cls, stop_loss: Any) -> float:
        """Validate stop loss."""
        try:
            stop_loss_float = float(stop_loss)
        except (ValueError, TypeError):
            raise ValidationError("Stop loss must be a valid number")
        
        if stop_loss_float <= 0:
            raise ValidationError("Stop loss must be positive")
        
        if stop_loss_float > 0.5:  # 50% limit
            raise ValidationError("Stop loss cannot exceed 50%")
        
        return round(stop_loss_float, 4)
    
    @classmethod
    def validate_date(cls, date_str: str) -> str:
        """Validate and format date string."""
        if not date_str:
            raise ValidationError("Date cannot be empty")
        
        try:
            # Try to parse the date
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Check if date is in the future
            if parsed_date > datetime.now():
                raise ValidationError("Date cannot be in the future")
            
            # Check if date is too old (more than 10 years ago)
            if parsed_date < datetime.now() - timedelta(days=3650):
                raise ValidationError("Date cannot be more than 10 years ago")
            
            return date_str
        except ValueError:
            raise ValidationError("Invalid date format. Use YYYY-MM-DD")
    
    @classmethod
    def validate_simulator_params(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all simulator parameters."""
        validated_params = {}
        
        try:
            # Validate required parameters
            validated_params['symbol'] = cls.validate_symbol(params.get('symbol', 'AAPL'))
            validated_params['interval'] = cls.validate_interval(params.get('interval', '1m'))
            validated_params['period'] = cls.validate_period(params.get('period', '1d'))
            validated_params['initial_cash'] = cls.validate_initial_cash(params.get('initial_cash', 50000))
            validated_params['short_window'] = cls.validate_short_window(params.get('short_window', 5))
            validated_params['long_window'] = cls.validate_long_window(
                params.get('long_window', 20), 
                validated_params['short_window']
            )
            validated_params['profit_threshold'] = cls.validate_profit_threshold(params.get('profit_threshold', 0.015))
            validated_params['stop_loss'] = cls.validate_stop_loss(params.get('stop_loss', 0.01))
            
            # Validate optional parameters
            if 'selected_date' in params and params['selected_date']:
                validated_params['selected_date'] = cls.validate_date(params['selected_date'])
            
            return validated_params
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
    
    @classmethod
    def sanitize_string(cls, text: str, max_length: int = 100) -> str:
        """Sanitize string input."""
        if not text:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', str(text))
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized.strip()
    
    @classmethod
    def validate_json_payload(cls, payload: Dict[str, Any], required_fields: List[str] = None) -> Dict[str, Any]:
        """Validate JSON payload structure."""
        if not isinstance(payload, dict):
            raise ValidationError("Payload must be a JSON object")
        
        if required_fields:
            missing_fields = [field for field in required_fields if field not in payload]
            if missing_fields:
                raise ValidationError(f"Missing required fields: {missing_fields}")
        
        return payload

def validate_request_data(request_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """Validate request data and return (is_valid, error_message, validated_data)."""
    try:
        validated_data = InputValidator.validate_simulator_params(request_data)
        return True, None, validated_data
    except ValidationError as e:
        return False, str(e), {}
    except Exception as e:
        logger.error(f"Unexpected validation error: {e}")
        return False, "Internal validation error", {}

