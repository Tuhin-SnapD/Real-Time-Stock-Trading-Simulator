import unittest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.data_fetcher import DataFetcher

class TestDataFetcher(unittest.TestCase):
    """Test cases for the optimized DataFetcher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fetcher = DataFetcher(symbol="AAPL", interval="1m", period="1d")
        
        # Mock data for testing
        self.mock_data = pd.DataFrame({
            'Open': [150.0, 151.0, 152.0],
            'High': [153.0, 154.0, 155.0],
            'Low': [149.0, 150.0, 151.0],
            'Close': [151.0, 152.0, 153.0],
            'Volume': [1000000, 1100000, 1200000]
        }, index=pd.date_range('2024-01-01', periods=3, freq='1min'))
    
    def test_initialization(self):
        """Test DataFetcher initialization."""
        self.assertEqual(self.fetcher.symbol, "AAPL")
        self.assertEqual(self.fetcher.interval, "1m")
        self.assertEqual(self.fetcher.period, "1d")
        self.assertEqual(self.fetcher.max_retries, 5)
        self.assertEqual(self.fetcher.retry_delay, 10)
    
    def test_initialization_with_invalid_symbol(self):
        """Test initialization with invalid symbol."""
        with self.assertRaises(ValueError):
            DataFetcher(symbol="")
        
        with self.assertRaises(ValueError):
            DataFetcher(symbol="A" * 15)  # Too long
    
    def test_initialization_with_invalid_interval(self):
        """Test initialization with invalid interval."""
        with self.assertRaises(ValueError):
            DataFetcher(interval="invalid")
    
    def test_initialization_with_invalid_retries(self):
        """Test initialization with invalid retry parameters."""
        with self.assertRaises(ValueError):
            DataFetcher(max_retries=0)
        
        with self.assertRaises(ValueError):
            DataFetcher(retry_delay=0)
    
    def test_validate_data(self):
        """Test data validation."""
        # Valid data
        self.assertTrue(self.fetcher._validate_data(self.mock_data))
        
        # Empty data
        empty_data = pd.DataFrame()
        self.assertFalse(self.fetcher._validate_data(empty_data))
        
        # Missing columns
        invalid_data = pd.DataFrame({'Open': [150.0]})
        self.assertFalse(self.fetcher._validate_data(invalid_data))
        
        # Negative volume
        bad_volume_data = self.mock_data.copy()
        bad_volume_data.loc[0, 'Volume'] = -1000
        self.assertFalse(self.fetcher._validate_data(bad_volume_data))
    
    def test_cache_operations(self):
        """Test cache operations."""
        # Test cache key generation
        cache_key = self.fetcher._get_cache_key()
        expected_key = "AAPL_1m_1d_None"
        self.assertEqual(cache_key, expected_key)
        
        # Test cache validity
        cache_entry = {
            'data': self.mock_data,
            'timestamp': datetime.now().timestamp()
        }
        self.assertTrue(self.fetcher._is_cache_valid(cache_entry))
        
        # Test expired cache
        old_cache_entry = {
            'data': self.mock_data,
            'timestamp': (datetime.now() - timedelta(minutes=2)).timestamp()
        }
        self.assertFalse(self.fetcher._is_cache_valid(old_cache_entry))
    
    @patch('core.data_fetcher.yf.Ticker')
    def test_get_real_time_data_success(self, mock_ticker):
        """Test successful data fetching."""
        # Mock the yfinance Ticker
        mock_stock = Mock()
        mock_stock.history.return_value = self.mock_data
        mock_ticker.return_value = mock_stock
        
        # Test data fetching
        result = self.fetcher.get_real_time_data()
        
        # Verify results
        self.assertFalse(result.empty)
        # Note: Length might be different due to synthetic data points being added
        self.assertGreaterEqual(len(result), 3)
        self.assertIn('Close', result.columns)
        
        # Verify cache was used
        cached_result = self.fetcher.get_real_time_data()
        self.assertTrue(result.equals(cached_result))
    
    @patch('core.data_fetcher.yf.Ticker')
    def test_get_real_time_data_failure(self, mock_ticker):
        """Test data fetching with failures."""
        # Mock the yfinance Ticker to raise exception
        mock_stock = Mock()
        mock_stock.history.side_effect = Exception("API Error")
        mock_ticker.return_value = mock_stock
        
        # Test data fetching with failure
        result = self.fetcher.get_real_time_data()
        
        # Should return empty DataFrame after all retries
        self.assertTrue(result.empty)
        self.assertEqual(self.fetcher._consecutive_failures, 5)
    
    def test_get_latest_price(self):
        """Test getting latest price."""
        # Set up mock data
        self.fetcher.last_data = self.mock_data
        
        # Test getting latest price
        price = self.fetcher.get_latest_price()
        self.assertEqual(price, 153.0)
    
    @patch('core.data_fetcher.yf.Ticker')
    def test_get_latest_price_with_mock(self, mock_ticker):
        """Test getting latest price with proper mocking."""
        # Mock the yfinance Ticker
        mock_stock = Mock()
        mock_stock.history.return_value = self.mock_data
        mock_ticker.return_value = mock_stock
        
        # Test getting latest price
        price = self.fetcher.get_latest_price()
        self.assertEqual(price, 153.0)
    
    def test_get_latest_price_with_nan(self):
        """Test getting latest price with NaN values."""
        # Create data with NaN
        nan_data = self.mock_data.copy()
        nan_data.loc[2, 'Close'] = float('nan')
        self.fetcher.last_data = nan_data
        
        # Test getting latest price
        price = self.fetcher.get_latest_price()
        self.assertIsNone(price)
    
    @patch('core.data_fetcher.yf.Ticker')
    def test_get_latest_price_with_nan_mock(self, mock_ticker):
        """Test getting latest price with NaN values using proper mocking."""
        # Create data with NaN
        nan_data = self.mock_data.copy()
        nan_data.loc[2, 'Close'] = float('nan')
        
        # Mock the yfinance Ticker
        mock_stock = Mock()
        mock_stock.history.return_value = nan_data
        mock_ticker.return_value = mock_stock
        
        # Test getting latest price
        price = self.fetcher.get_latest_price()
        self.assertIsNone(price)
    
    def test_get_data_summary(self):
        """Test getting data summary."""
        # Set up some data
        self.fetcher.last_data = self.mock_data
        self.fetcher.last_fetch_time = datetime.now()
        self.fetcher._consecutive_failures = 2
        self.fetcher._last_error = "Test error"
        
        # Get summary
        summary = self.fetcher.get_data_summary()
        
        # Verify summary
        self.assertEqual(summary['symbol'], 'AAPL')
        self.assertEqual(summary['interval'], '1m')
        self.assertEqual(summary['period'], '1d')
        self.assertEqual(summary['data_points'], 3)
        self.assertEqual(summary['consecutive_failures'], 2)
        self.assertEqual(summary['last_error'], 'Test error')
    
    def test_clear_cache(self):
        """Test cache clearing."""
        # Add some data to cache
        self.fetcher._cache['test_key'] = {'data': self.mock_data, 'timestamp': datetime.now().timestamp()}
        self.assertEqual(len(self.fetcher._cache), 1)
        
        # Clear cache
        self.fetcher.clear_cache()
        self.assertEqual(len(self.fetcher._cache), 0)
    
    def test_reset_error_counters(self):
        """Test resetting error counters."""
        # Set up error state
        self.fetcher._consecutive_failures = 5
        self.fetcher._last_error = "Test error"
        
        # Reset counters
        self.fetcher.reset_error_counters()
        
        # Verify reset
        self.assertEqual(self.fetcher._consecutive_failures, 0)
        self.assertIsNone(self.fetcher._last_error)
    
    def test_historical_data_fetching(self):
        """Test historical data fetching."""
        historical_fetcher = DataFetcher(
            symbol="AAPL", 
            interval="1m", 
            period="1d", 
            start_date="2024-01-01"
        )
        
        # Test cache key for historical data
        cache_key = historical_fetcher._get_cache_key()
        expected_key = "AAPL_1m_1d_2024-01-01"
        self.assertEqual(cache_key, expected_key)
    
    def test_future_date_validation(self):
        """Test validation of future dates."""
        future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        future_fetcher = DataFetcher(
            symbol="AAPL", 
            interval="1m", 
            period="1d", 
            start_date=future_date
        )
        
        # Test fetching data for future date
        result = future_fetcher._fetch_historical_data(Mock(), 1)
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()

