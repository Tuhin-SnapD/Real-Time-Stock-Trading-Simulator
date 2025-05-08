# In main.py or a test script
from data_fetcher import DataFetcher

fetcher = DataFetcher(symbol="AAPL")
data = fetcher.get_real_time_data()
print(data.tail())  # Last 5 rows of data
print(f"Latest price: {fetcher.get_latest_price()}")