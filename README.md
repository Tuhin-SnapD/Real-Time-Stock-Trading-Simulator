# 📈 Real-Time Stock Trading Simulator

A sophisticated Python-based real-time stock trading simulator that demonstrates automated trading system development with live market data integration, advanced strategy implementation, and comprehensive performance analytics.

## 🎯 Overview

This project simulates real-time stock trading using live market data from Yahoo Finance (`yfinance`). It implements a moving average crossover strategy, manages portfolio positions, stores trade history in SQLite, and generates detailed performance reports with key financial metrics.

### Key Features
- 🔄 **Real-Time Data Integration**: Live 1-minute stock data during US market hours
- 📊 **Advanced Trading Strategy**: Moving average crossover algorithm with configurable parameters
- 💼 **Portfolio Management**: Cash tracking, position management, and transaction cost handling
- 🗄️ **Data Persistence**: SQLite database for trade history and portfolio tracking
- 📈 **Performance Analytics**: Comprehensive reporting with Sharpe ratio, drawdown analysis
- 📊 **Interactive Visualization**: Real-time charts using Plotly
- 🛡️ **Robust Error Handling**: Comprehensive error management and data validation

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **US Market Hours**: For real-time data, run during 9:30 AM–4:00 PM ET
- **Internet Connection**: Required for live data fetching

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Real-Time-Stock-Trading-Simulator.git
   cd Real-Time-Stock-Trading-Simulator
   ```

2. **Set Up Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python -c "import main, data_fetcher, strategy, portfolio, database, visualizer, report; print('✅ All modules imported successfully')"
   ```

## 📁 Project Structure

```
Real-Time-Stock-Trading-Simulator/
├── 📄 main.py              # Main simulator orchestrator
├── 📄 data_fetcher.py      # Real-time data fetching (yfinance)
├── 📄 strategy.py          # Trading strategy implementation
├── 📄 portfolio.py         # Portfolio and position management
├── 📄 database.py          # SQLite trade storage
├── 📄 visualizer.py        # Interactive charts (Plotly)
├── 📄 report.py            # Performance analytics
├── 📄 requirements.txt     # Python dependencies
├── 📄 README.md           # Project documentation
├── 📄 LICENSE             # MIT License
├── 🗄️ trades.db           # Trade history database
├── 📊 portfolio_values.txt # Portfolio value tracking
└── 📈 performance_report.txt # Generated reports
```

## 🎮 Usage

### Running the Simulator

**Basic Usage:**
```bash
python main.py --symbol AAPL --interval 1m --period 1h --cash 50000 --iterations 100
```

**Parameters:**
- `--symbol`: Stock ticker symbol (e.g., `AAPL`, `MSFT`, `TSLA`, `GOOGL`)
- `--interval`: Data interval (`1m`, `5m`, `15m`, `1h`)
- `--period`: Data period (`1h`, `1d`, `5d`, `1mo`)
- `--cash`: Initial cash balance (default: `$50,000`)
- `--iterations`: Number of trading iterations (default: `100`)

### Example Commands

**High-Frequency Trading (Tesla):**
```bash
python main.py --symbol TSLA --interval 1m --period 1h --cash 100000 --iterations 50
```

**Conservative Trading (Microsoft):**
```bash
python main.py --symbol MSFT --interval 5m --period 1d --cash 75000 --iterations 200
```

**Quick Test Run:**
```bash
python main.py --symbol AAPL --interval 1m --period 1h --cash 25000 --iterations 25
```

### Generating Performance Reports

After running the simulator:
```bash
python report.py
```

This generates `performance_report.txt` with detailed analytics.

## 📊 Sample Output

### Simulator Console Output
```
Attempt 1: Fetched 60 rows for AAPL at 2025-01-15 19:30:00
Iteration 0: Data received with 60 rows
Latest signal: 1, Latest price: 197.85
Executed buy for AAPL at 197.85
Portfolio value: $49802.15, Holdings: {'AAPL': 1}

Iteration 1: Data received with 61 rows
Latest signal: 0, Latest price: 198.00
No trade signal (signal=0)
Portfolio value: $49802.30, Holdings: {'AAPL': 1}
```

### Performance Report
```
Performance Report for AAPL
========================================
Initial Cash: $50000.00
Portfolio values loaded: 50 entries
Found 4 trades

📈 Performance Metrics:
Total Return: 0.85%
Sharpe Ratio: 0.62
Max Drawdown: 1.20%
Win Rate: 50.00%

📊 Trade Summary:
time                 symbol type  price  quantity
2025-01-15T19:30:00  AAPL  buy   197.85  1
2025-01-15T19:35:00  AAPL  sell  198.10  1
2025-01-15T19:40:00  AAPL  buy   197.50  1
2025-01-15T19:45:00  AAPL  sell  197.55  1
```

## 🔧 Trading Strategy

### Moving Average Crossover
The simulator implements a classic moving average crossover strategy:

- **Short MA**: 2-period moving average (sensitive to recent price changes)
- **Long MA**: 5-period moving average (trend indicator)
- **Buy Signal**: When short MA crosses above long MA
- **Sell Signal**: When short MA crosses below long MA
- **Hold**: When no crossover occurs

### Strategy Parameters
```python
# Configurable in main.py
strategy = TradingStrategy(short_window=2, long_window=5)
```

### Transaction Costs
- **Commission**: 0.1% per trade
- **Slippage**: Not currently modeled
- **Minimum Trade Size**: 1 share

## 🛠️ Technical Architecture

### Data Flow
1. **Data Fetching**: `yfinance` API → Real-time OHLCV data
2. **Signal Generation**: Moving average calculations → Buy/Sell signals
3. **Trade Execution**: Portfolio management → Position updates
4. **Data Storage**: SQLite database → Trade history
5. **Analytics**: Performance calculations → Reports & charts

### Key Components

#### DataFetcher (`data_fetcher.py`)
- Real-time data retrieval from Yahoo Finance
- Retry logic with fallback mechanisms
- Data validation and quality checks

#### TradingStrategy (`strategy.py`)
- Moving average crossover algorithm
- Signal generation (1 = buy, -1 = sell, 0 = hold)
- Configurable window parameters

#### Portfolio (`portfolio.py`)
- Cash and position tracking
- Trade execution logic
- Portfolio value calculations

#### TradeDatabase (`database.py`)
- SQLite-based trade storage
- Transaction history management
- Data persistence

## 📈 Performance Metrics

The system calculates comprehensive performance metrics:

- **Total Return**: Percentage gain/loss from initial investment
- **Sharpe Ratio**: Risk-adjusted return measure
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Average Trade Price**: Mean execution price
- **Trade Frequency**: Number of trades per period

## 🔍 Troubleshooting

### Common Issues

**❌ No Data Received**
```bash
# Check market hours (US: 9:30 AM - 4:00 PM ET)
# Try different intervals
python main.py --symbol AAPL --interval 5m --period 2h
```

**❌ No Trading Signals**
```bash
# Reduce strategy sensitivity
# Edit main.py: short_window=1, long_window=3
# Try volatile stocks: TSLA, NVDA
```

**❌ Import Errors**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**❌ Database Issues**
```bash
# Reset database
rm trades.db
python main.py
```

### Debug Mode
Enable verbose logging by modifying `main.py`:
```python
# Add debug prints
print(f"Debug: Data shape {data.shape}")
print(f"Debug: Signals {signals.tail()}")
```

## 🚀 Advanced Usage

### Custom Strategies
Extend `strategy.py` to implement alternative strategies:

```python
class RSITradingStrategy(TradingStrategy):
    def generate_signals(self, data):
        # Implement RSI strategy
        pass

class MACDTradingStrategy(TradingStrategy):
    def generate_signals(self, data):
        # Implement MACD strategy
        pass
```

### Multiple Symbols
Modify `main.py` to trade multiple stocks simultaneously:

```python
symbols = ["AAPL", "MSFT", "GOOGL"]
for symbol in symbols:
    # Run simulator for each symbol
    pass
```

### Backtesting
Use historical data for strategy validation:

```python
# Modify data_fetcher.py for historical data
data = stock.history(start="2024-01-01", end="2024-12-31")
```

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `yfinance` | 0.2.65 | Real-time stock data |
| `pandas` | 2.3.1 | Data manipulation |
| `numpy` | 2.3.2 | Numerical computations |
| `plotly` | 6.2.0 | Interactive charts |
| `requests` | 2.32.4 | HTTP requests |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This is a simulation for educational purposes only.**

- Not financial advice
- Past performance doesn't guarantee future results
- Real trading involves significant risks
- Use at your own risk
- Consider paper trading before live trading

## 🔗 Related Projects

- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance market data
- [pandas](https://pandas.pydata.org/) - Data analysis library
- [plotly](https://plotly.com/python/) - Interactive plotting

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/Real-Time-Stock-Trading-Simulator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/Real-Time-Stock-Trading-Simulator/discussions)
- **Email**: your-email@example.com

---

⭐ **Star this repository if you find it helpful!**