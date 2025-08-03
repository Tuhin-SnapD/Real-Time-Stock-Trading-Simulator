import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self, symbol="AAPL", interval="1m", period="1h", max_retries=5, retry_delay=10):
        self.symbol = symbol
        self.interval = interval
        self.period = period
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.last_data = pd.DataFrame()
        self.last_fetch_time = None

    def get_real_time_data(self):
        """Fetch real-time stock data with retry logic and fallback."""
        for attempt in range(self.max_retries):
            try:
                stock = yf.Ticker(self.symbol)
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
                    
                    # Check if data is new by comparing timestamps
                    if self.last_data.empty or data.index[-1] > self.last_data.index[-1]:
                        self.last_data = data[required_columns]
                        self.last_fetch_time = current_time
                        return self.last_data
                    else:
                        print(f"Data not new (latest timestamp: {data.index[-1]}). Retrying...")
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