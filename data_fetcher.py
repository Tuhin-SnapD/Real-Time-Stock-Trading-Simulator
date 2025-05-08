import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self, symbol="AAPL", interval="1m", period="1d"):
        self.symbol = symbol
        self.interval = interval  # 1-minute candles
        self.period = period      # 1 day of data

    def get_real_time_data(self):
        """Fetch real-time stock data."""
        try:
            stock = yf.Ticker(self.symbol)
            data = stock.history(period=self.period, interval=self.interval)
            return data[["Open", "High", "Low", "Close", "Volume"]]
        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()

    def get_latest_price(self):
        """Get the most recent closing price."""
        data = self.get_real_time_data()
        if not data.empty:
            return data["Close"].iloc[-1]
        return None