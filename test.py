from data_fetcher import DataFetcher
from strategy import TradingStrategy

fetcher = DataFetcher(symbol="AAPL")
data = fetcher.get_real_time_data()
strategy = TradingStrategy()
signals = strategy.generate_signals(data)
print(signals.tail())  # View signals