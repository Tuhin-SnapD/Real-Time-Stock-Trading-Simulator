import os
from typing import Dict, Any

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Trading settings
    DEFAULT_SYMBOL = 'AAPL'
    DEFAULT_INTERVAL = '1m'
    DEFAULT_PERIOD = '1d'
    DEFAULT_INITIAL_CASH = 50000
    
    # Data fetching settings
    MAX_RETRIES = 5
    RETRY_DELAY = 10
    
    # Strategy settings
    DEFAULT_SHORT_WINDOW = 2
    DEFAULT_LONG_WINDOW = 5
    
    # Available stocks for the simulator
    AVAILABLE_STOCKS = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
        'AMD', 'INTC', 'CRM', 'ORCL', 'ADBE', 'PYPL', 'UBER', 'LYFT',
        'SPOT', 'ZM', 'SQ', 'SHOP', 'ROKU', 'PINS', 'SNAP', 'TWTR',
        'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'JNJ', 'PFE', 'UNH',
        'HD', 'DIS', 'V', 'MA', 'PG', 'KO', 'PEP', 'WMT', 'COST'
    ]
    
    # Chart settings
    MAX_PORTFOLIO_VALUES = 100
    CHART_UPDATE_INTERVAL = 5000  # milliseconds
    
    @classmethod
    def get_trading_config(cls) -> Dict[str, Any]:
        """Get trading configuration."""
        return {
            'default_symbol': cls.DEFAULT_SYMBOL,
            'default_interval': cls.DEFAULT_INTERVAL,
            'default_period': cls.DEFAULT_PERIOD,
            'default_initial_cash': cls.DEFAULT_INITIAL_CASH,
            'available_stocks': cls.AVAILABLE_STOCKS
        }
    
    @classmethod
    def get_strategy_config(cls) -> Dict[str, Any]:
        """Get strategy configuration."""
        return {
            'short_window': cls.DEFAULT_SHORT_WINDOW,
            'long_window': cls.DEFAULT_LONG_WINDOW
        }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 