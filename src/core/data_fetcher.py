import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self, symbol="AAPL", interval="1m", period="1d", max_retries=5, retry_delay=10, start_date=None):
        self.symbol = symbol
        self.interval = interval
        self.period = period
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.start_date = start_date
        self.last_data = pd.DataFrame()
        self.last_fetch_time = None

    def get_real_time_data(self):
        """Fetch real-time stock data with retry logic and fallback."""
        for attempt in range(self.max_retries):
            try:
                stock = yf.Ticker(self.symbol)
                
                # If a specific start date is provided, use it for historical data
                if self.start_date:
                    # Convert start_date string to datetime
                    start_dt = pd.to_datetime(self.start_date)
                    end_dt = start_dt + timedelta(days=1)  # Get one day of data
                    
                    # Check if the date is in the future
                    if start_dt > datetime.now():
                        print(f"Error: Cannot fetch data for future date {self.start_date}")
                        return pd.DataFrame()
                    
                    # Check if date is within last 30 days for 1m data
                    days_diff = (datetime.now() - start_dt).days
                    if days_diff > 30 and self.interval == "1m":
                        print(f"Warning: 1m data only available for last 30 days. Switching to 1d data for {self.start_date}")
                        # Use daily data for older dates
                        data = stock.history(start=start_dt, end=end_dt, interval="1d")
                    else:
                        data = stock.history(start=start_dt, end=end_dt, interval=self.interval)
                    
                    print(f"Attempt {attempt + 1}: Fetched {len(data)} rows for {self.symbol} on {self.start_date}")
                else:
                    data = stock.history(period=self.period, interval=self.interval)
                    current_time = datetime.now()
                    print(f"Attempt {attempt + 1}: Fetched {len(data)} rows for {self.symbol} at {current_time}")
                
                if not data.empty:
                    # Validate data has required columns
                    required_columns = ["Open", "High", "Low", "Close", "Volume"]
                    if not all(col in data.columns for col in required_columns):
                        print(f"Data missing required columns. Available: {data.columns.tolist()}")
                        if attempt < self.max_retries - 1:
                            time.sleep(self.retry_delay)
                        continue
                    
                    # Use the data if it's available (don't require it to be "new")
                    # This allows the simulator to work with available historical data
                    self.last_data = data[required_columns]
                    self.last_fetch_time = datetime.now()
                    return self.last_data
                else:
                    print(f"Empty data received for {self.symbol}. Retrying...")
            except Exception as e:
                print(f"Error fetching data for {self.symbol} (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                continue
        
        # Fallback to last valid data if available
        if not self.last_data.empty:
            print(f"No new data. Using last valid data ({len(self.last_data)} rows, fetched at {self.last_fetch_time})")
            return self.last_data
        
        print(f"Failed to fetch data for {self.symbol} after {self.max_retries} attempts.")
        return pd.DataFrame()

    def get_latest_price(self):
        """Get the most recent closing price."""
        data = self.get_real_time_data()
        if not data.empty:
            return data["Close"].iloc[-1]
        return None