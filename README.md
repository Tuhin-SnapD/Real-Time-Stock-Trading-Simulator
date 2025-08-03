# Real-Time Stock Trading Simulator

A Python-based real-time stock trading simulator that fetches live market data using `yfinance`, executes trades based on a moving average crossover strategy, stores trades in an SQLite database, and generates performance reports with key metrics like total return, Sharpe ratio, and max drawdown. Built to demonstrate e-trading system development, data integration, and performance analysis for financial applications.

## 🚀 Recent Updates

**Latest Version**: Enhanced with comprehensive bug fixes and improvements:
- ✅ **Fixed Critical Strategy Logic Bug** - Trading signals now generate correctly
- ✅ **Enhanced Error Handling** - Robust handling of API failures and data issues
- ✅ **Improved Data Validation** - Better quality checks for market data
- ✅ **Division by Zero Protection** - Safe calculation of performance metrics
- ✅ **Virtual Environment Support** - Isolated dependency management
- ✅ **Comprehensive Testing** - All components verified and working

See [BUGFIXES.md](BUGFIXES.md) for detailed information about all fixes and improvements.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Sample Output](#sample-output)
- [Troubleshooting](#troubleshooting)
- [Bug Fixes](#bug-fixes)
- [Future Improvements](#future-improvements)
- [License](#license)

## Features
- **Real-Time Data Fetching**: Integrates `yfinance` to retrieve live 1-minute stock data during US market hours (9:30 AM–4:00 PM ET).
- **Trading Strategy**: Implements a moving average crossover strategy (short=2, long=5) to generate buy/sell signals.
- **Portfolio Management**: Tracks cash, holdings, and portfolio value with transaction costs (0.1% per trade).
- **Database Storage**: Saves trade details (timestamp, symbol, type, price, quantity) in an SQLite database.
- **Performance Reporting**: Generates reports with metrics including total return, Sharpe ratio, and max drawdown.
- **Visualization**: Plots price trends, moving averages, and portfolio value over time using Plotly.
- **Robust Error Handling**: Comprehensive error handling for API failures, data validation, and edge cases.
- **Virtual Environment Support**: Isolated dependency management for consistent deployment.

## Prerequisites
- **Python**: Version 3.8 or higher.
- **US Market Hours**: For real-time data, run during 9:30 AM–4:00 PM ET (7:00 PM–1:30 AM IST).
- **Dependencies**: All dependencies are managed via `requirements.txt`

## Installation

### Option 1: Using Virtual Environment (Recommended)
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/stock-trading-simulator.git
   cd stock-trading-simulator
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Direct Installation
```bash
pip install yfinance pandas numpy plotly requests
```

4. **Verify Setup**:
   ```bash
   python -c "import main, data_fetcher, strategy, portfolio, database, visualizer, report; print('✅ All modules imported successfully')"
   ```

## Project Structure
```
stock-trading-simulator/
│
├── main.py              # Main simulator loop for real-time trading
├── data_fetcher.py      # Fetches real-time data using yfinance
├── strategy.py          # Implements moving average crossover strategy
├── portfolio.py         # Manages portfolio (cash, holdings, metrics)
├── database.py          # Stores trades in SQLite database
├── visualizer.py        # Plots price trends and portfolio value
├── report.py            # Generates performance reports
├── requirements.txt     # Python dependencies with exact versions
├── BUGFIXES.md          # Detailed documentation of all fixes
├── trades.db            # SQLite database for trade storage
├── portfolio_values.txt # Stores portfolio value history
├── performance_report.txt # Output of performance report
├── venv/                # Virtual environment (created during setup)
└── README.md            # Project documentation
```

## Usage
### Run the Simulator
Run during US market hours (7:00 PM–1:30 AM IST for India) for real-time data:
```bash
python main.py --symbol AAPL --interval 1m --period 1h --cash 50000 --iterations 100
```
- `--symbol`: Stock ticker (e.g., `AAPL`, `MSFT`, `TSLA`).
- `--interval`: Data interval (e.g., `1m`, `5m`).
- `--period`: Data period (e.g., `1h`, `1d`).
- `--cash`: Initial cash balance (default: `50000`).
- `--iterations`: Number of iterations (default: `100`).

This fetches data, generates signals, executes trades, saves them to `trades.db`, and logs portfolio values to `portfolio_values.txt`. A plot is displayed after the run.

### Generate Performance Report
After running the simulator, generate a report:
```bash
python report.py
```
This reads `portfolio_values.txt` and `trades.db` to produce `performance_report.txt` with metrics and trade summaries.

### Example Commands
- Run with Tesla stock for 50 iterations:
  ```bash
  python main.py --symbol TSLA --interval 1m --period 1h --cash 100000 --iterations 50
  ```
- Generate report:
  ```bash
  python report.py
  ```

## Sample Output
### Simulator Output
```
Attempt 1: Fetched 60 rows for AAPL at 2025-05-08 19:30:00
Iteration 0: Data received with 60 rows
Latest signal: 1, Latest price: 197.85
Executed buy for AAPL at 197.85
Portfolio value: $49802.15, Holdings: {'AAPL': 1}
Attempt 1: Fetched 61 rows for AAPL at 2025-05-08 19:31:00
Iteration 1: Data received with 61 rows
Latest signal: 0, Latest price: 198.00
No trade signal (signal=0)
Portfolio value: $49802.30, Holdings: {'AAPL': 1}
```

### Performance Report (`performance_report.txt`)
```
Performance Report for AAPL
========================================
Initial Cash: $50000.00
Portfolio values loaded: 50 entries
Found 4 trades
Total Trades: 4
Buy Trades: 2
Sell Trades: 2
Average Trade Price: $197.75
Total Return: 0.85%
Sharpe Ratio: 0.62
Max Drawdown: 1.20%
========================================
Trade Summary:
time                 symbol type  price  quantity
2025-05-08T19:30:00  AAPL  buy   197.85  1
2025-05-08T19:35:00  AAPL  sell  198.10  1
2025-05-08T19:40:00  AAPL  buy   197.50  1
2025-05-08T19:45:00  AAPL  sell  197.55  1
```

### Visualization
A plot showing price, moving averages, and portfolio value is displayed after the simulation.

## Troubleshooting
- **Portfolio Value Stuck at `$50000.00`**:
  - Ensure you're running during US market hours (7:00 PM–1:30 AM IST).
  - Check console output for `Fetched X rows`. If `X` is low or timestamps are old, try `--interval 5m` or `--period 2h`.
  - Update `yfinance`: `pip install yfinance --upgrade`.
- **"No trades found in database"**:
  - Run the simulator first to populate `trades.db`.
  - Verify trades in console (`Executed buy/sell`).
  - Delete `trades.db` to reset the database if schema issues occur.
- **Import Errors**:
  - Ensure virtual environment is activated: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
  - Install dependencies: `pip install -r requirements.txt`
- **No Signals**:
  - Reduce strategy windows in `main.py` (e.g., `short_window=1`, `long_window=3`).
  - Try a volatile stock: `--symbol TSLA`.
- **Share Issues**:
  - Provide console output, `performance_report.txt`, and `portfolio_values.txt` contents.

## Bug Fixes
This project has been extensively tested and debugged. Key fixes include:

- **Critical Strategy Logic**: Fixed broken signal generation algorithm
- **Error Handling**: Added comprehensive error handling for all components
- **Data Validation**: Enhanced validation for API responses and data quality
- **Performance Metrics**: Protected against division by zero errors
- **Visualization**: Fixed array length mismatches in plotting

See [BUGFIXES.md](BUGFIXES.md) for complete details.

## Future Improvements
- Add support for multiple stocks in a single run.
- Implement alternative strategies (e.g., RSI, MACD).
- Generate PDF reports using LaTeX for professional output.
- Deploy as a cloud-based application with API integration.
- Add backtesting capabilities for historical data analysis.
- Implement risk management features (stop-loss, position sizing).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.