# Real-Time Stock Trading Simulator

A modern, professional web-based real-time stock trading simulator with interactive charts, live data visualization, and advanced trading strategies. Built with Flask, Plotly, and Yahoo Finance API.

![Trading Simulator Dashboard](https://img.shields.io/badge/Status-Active-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue)
![Flask Version](https://img.shields.io/badge/Flask-2.3+-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Features

### Core Trading Features
- **Real-time Stock Data**: Live stock price monitoring with Yahoo Finance integration
- **Advanced Trading Strategy**: Moving average crossover strategy with configurable parameters
- **Portfolio Tracking**: Real-time portfolio value updates and performance metrics
- **Historical Mode**: Run simulations on historical data for backtesting
- **Multiple Stocks**: Support for 40+ popular stocks and ETFs

### User Interface
- **Interactive Charts**: Beautiful Plotly charts showing price movements and trading signals
- **Responsive Design**: Modern UI that works seamlessly on desktop and mobile
- **Real-time Updates**: Live data updates with smooth animations
- **Dark Mode Support**: Automatic dark mode detection and styling
- **Professional Dashboard**: Clean, intuitive interface with comprehensive trading information

### Technical Features
- **Modular Architecture**: Well-organized codebase with separation of concerns
- **API-First Design**: RESTful API endpoints for all trading operations
- **Error Handling**: Robust error handling and retry mechanisms
- **Configuration Management**: Environment-based configuration system
- **Testing Suite**: Comprehensive unit tests for core functionality

## 📁 Project Structure

```
Real-Time-Stock-Trading-Simulator/
├── src/                          # Main source code
│   ├── core/                     # Core trading functionality
│   │   ├── __init__.py
│   │   ├── data_fetcher.py      # Stock data fetching
│   │   └── strategy.py          # Trading strategy implementation
│   ├── api/                      # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py            # Flask routes and API handlers
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   └── config.py            # Configuration management
│   └── models/                   # Data models
│       ├── __init__.py
│       └── trade.py             # Trade and portfolio models
├── static/                       # Static assets
│   ├── css/                     # Stylesheets
│   │   └── main.css             # Main application styles
│   ├── js/                      # JavaScript files
│   │   └── app.js               # Main application logic
│   ├── images/                  # Image assets
│   └── templates/               # HTML templates
│       └── index.html           # Main dashboard template
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_data_fetcher.py     # Data fetcher tests
│   └── test_strategy.py         # Strategy tests
├── docs/                         # Documentation
├── app.py                       # Main application entry point
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── Makefile                     # Development tasks
├── env.example                  # Environment variables example
└── README.md                    # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/real-time-stock-trading-simulator.git
   cd real-time-stock-trading-simulator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

### Development Setup

For development with additional tools:

```bash
# Install development dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Lint code
make lint
```

## 🎯 Usage

### Basic Trading

1. **Select Stock**: Choose from 40+ available stocks and ETFs
2. **Configure Parameters**: Set interval, period, and initial cash amount
3. **Start Simulation**: Click "Start Simulator" to begin real-time trading
4. **Monitor Results**: Watch live charts and trade updates
5. **Stop Simulation**: Click "Stop Simulator" when finished

### Historical Mode

1. **Enable Historical Mode**: Check the "Historical Mode" checkbox
2. **Select Date**: Choose a specific date for backtesting
3. **Run Simulation**: Start the simulator to see how your strategy would have performed

### Trading Strategy

The simulator uses a **Moving Average Crossover** strategy:
- **Buy Signal**: When short-term moving average crosses above long-term moving average
- **Sell Signal**: When short-term moving average crosses below long-term moving average
- **Configurable Parameters**: Adjust short and long window periods

## 🔧 Configuration

### Environment Variables

Copy `env.example` to `.env` and modify as needed:

```bash
# Flask Configuration
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=5000

# Trading Configuration
DEFAULT_SYMBOL=AAPL
DEFAULT_INTERVAL=1m
DEFAULT_PERIOD=1d
DEFAULT_INITIAL_CASH=50000

# Strategy Configuration
DEFAULT_SHORT_WINDOW=2
DEFAULT_LONG_WINDOW=5
```

### Available Stocks

The simulator supports 40+ popular stocks and ETFs including:
- **Technology**: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA
- **Finance**: JPM, BAC, WFC, GS, MS, C
- **Healthcare**: JNJ, PFE, UNH
- **Consumer**: HD, DIS, V, MA, PG, KO, PEP, WMT, COST
- **And many more...**

## 📊 API Endpoints

### Core Endpoints
- `GET /` - Main dashboard
- `GET /api/simulator-status` - Get simulation status

### Trading Endpoints
- `POST /api/start-simulator` - Start trading simulation
- `POST /api/stop-simulator` - Stop simulation
- `POST /api/clear-trades` - Clear all trades

### Data Endpoints
- `GET /api/stock-data` - Get current stock data and signals
- `GET /api/trades` - Get trade history
- `GET /api/portfolio-values` - Get portfolio value history

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run specific test file
python -m pytest tests/test_data_fetcher.py -v
```

## 🚀 Deployment

### Local Development
```bash
make run-dev
```

### Production
```bash
# Set production environment
export FLASK_DEBUG=False
export SECRET_KEY=your-production-secret-key

# Run application
python app.py
```

### Docker Deployment
```bash
# Build Docker image
make docker-build

# Run Docker container
make docker-run
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Yahoo Finance**: For providing real-time stock data
- **Plotly**: For interactive charting capabilities
- **Flask**: For the web framework
- **Bootstrap**: For responsive UI components

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/real-time-stock-trading-simulator/issues)
- **Documentation**: [Project Wiki](https://github.com/yourusername/real-time-stock-trading-simulator/wiki)
- **Email**: your.email@example.com

## 🔄 Changelog

### Version 1.0.0
- Initial release with real-time trading simulation
- Interactive charts and portfolio tracking
- Historical mode for backtesting
- Modular architecture and comprehensive testing

---

**Disclaimer**: This is a simulation tool for educational purposes only. It does not provide financial advice or guarantee investment returns. Always do your own research before making investment decisions.