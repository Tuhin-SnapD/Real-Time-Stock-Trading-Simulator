from flask import Blueprint, jsonify, request
import pandas as pd
from datetime import datetime
import threading
import time

# Import from core modules
from ..core.data_fetcher import DataFetcher
from ..core.strategy import TradingStrategy

# Create Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Global variables for real-time data and in-memory trade storage
current_data = pd.DataFrame()
current_signals = pd.DataFrame()
portfolio_values = []
trades_list = []  # In-memory storage for trades
is_simulator_running = False
simulator_thread = None
global_initial_cash = 5000  # Default initial cash

def run_simulator_background(symbol="AAPL", interval="1m", period="1d", initial_cash=50000, selected_date=None):
    """Run the simulator in a background thread."""
    global current_data, current_signals, portfolio_values, trades_list, is_simulator_running
    
    # Use more conservative strategy parameters for better profitability
    strategy = TradingStrategy(short_window=5, long_window=20, profit_threshold=0.015, stop_loss=0.01)
    
    # Initialize portfolio tracking and clear previous trades
    portfolio_values.clear()
    trades_list.clear()  # Clear previous trades
    current_cash = initial_cash
    shares_held = 0
    portfolio_values.append(initial_cash)
    
    # Store initial cash for baseline calculations
    global global_initial_cash
    global_initial_cash = initial_cash
    
    iteration = 0
    consecutive_failures = 0
    max_failures = 3
    
    # For historical data, we need to fetch all data first and then process it incrementally
    if selected_date:
        print(f"Running simulator for {symbol} on historical date: {selected_date}")
        # Fetch all historical data for the selected date
        fetcher = DataFetcher(symbol=symbol, interval=interval, period=period, start_date=selected_date)
        all_historical_data = fetcher.get_real_time_data()
        
        if all_historical_data.empty:
            print(f"No historical data available for {selected_date}")
            return
        
        print(f"Fetched {len(all_historical_data)} data points for historical simulation")
        
        # Process historical data incrementally
        data_index = 0
        while is_simulator_running and data_index < len(all_historical_data):
            try:
                # Get current slice of data (incrementally)
                current_slice = all_historical_data.iloc[:data_index + 1]
                if not current_slice.empty:
                    current_data = current_slice
                    
                    # Generate signals for current data slice
                    signals = strategy.generate_signals(current_slice)
                    if not signals.empty:
                        current_signals = signals
                        
                        # Get latest price
                        latest_price = signals["price"].iloc[-1]
                        
                        # Check if we have a signal
                        latest_signal = int(signals["signal"].iloc[-1])
                        
                        if latest_signal != 0:
                            if latest_signal == 1 and current_cash >= latest_price:  # Buy signal
                                # Use improved position sizing based on risk management
                                shares_to_buy = strategy.get_position_size(current_cash, latest_price, risk_per_trade=0.02)
                                if shares_to_buy > 0:
                                    cost = shares_to_buy * latest_price
                                    current_cash -= cost
                                    shares_held += shares_to_buy
                                    
                                    # Use historical timestamp for the trade
                                    trade_time = current_slice.index[-1]
                                    trade = {
                                        "time": trade_time.isoformat(),
                                        "symbol": symbol,
                                        "type": "buy",
                                        "price": latest_price,
                                        "quantity": shares_to_buy
                                    }
                                    trades_list.append(trade)  # Store in memory instead of database
                                    print(f"Bought {shares_to_buy} shares at ${latest_price:.2f} at {trade_time}")
                                    
                            elif latest_signal == -1 and shares_held > 0:  # Sell signal
                                proceeds = shares_held * latest_price
                                current_cash += proceeds
                                
                                # Use historical timestamp for the trade
                                trade_time = current_slice.index[-1]
                                trade = {
                                    "time": trade_time.isoformat(),
                                    "symbol": symbol,
                                    "type": "sell",
                                    "price": latest_price,
                                    "quantity": shares_held
                                }
                                trades_list.append(trade)  # Store in memory instead of database
                                print(f"Sold {shares_held} shares at ${latest_price:.2f} at {trade_time}")
                                shares_held = 0
                        
                        # Calculate current portfolio value with better tracking
                        current_portfolio_value = current_cash + (shares_held * latest_price)
                        portfolio_values.append(current_portfolio_value)
                        
                        # Calculate and log profit/loss
                        if len(portfolio_values) > 1:
                            profit_loss = current_portfolio_value - global_initial_cash
                            profit_percentage = (profit_loss / global_initial_cash) * 100
                            print(f"Portfolio: ${current_portfolio_value:.2f} | P&L: ${profit_loss:.2f} ({profit_percentage:.2f}%)")
                        
                        data_index += 1
                        time.sleep(0.5)  # Simulate real-time processing
                        
            except Exception as e:
                print(f"Error in historical simulation: {e}")
                consecutive_failures += 1
                if consecutive_failures >= max_failures:
                    print("Too many consecutive failures. Stopping simulation.")
                    break
                time.sleep(1)
                continue
        
        print("Historical simulation completed.")
        return
    
    # Real-time simulation
    print(f"Starting real-time simulator for {symbol}")
    fetcher = DataFetcher(symbol=symbol, interval=interval, period=period)
    
    while is_simulator_running:
        try:
            # Fetch real-time data
            data = fetcher.get_real_time_data()
            
            if not data.empty:
                current_data = data
                consecutive_failures = 0  # Reset failure counter
                
                # Generate signals
                signals = strategy.generate_signals(data)
                if not signals.empty:
                    current_signals = signals
                    
                    # Get latest price
                    latest_price = signals["price"].iloc[-1]
                    
                    # Check if we have a signal
                    latest_signal = int(signals["signal"].iloc[-1])
                    
                    if latest_signal != 0:
                        if latest_signal == 1 and current_cash >= latest_price:  # Buy signal
                            # Use improved position sizing based on risk management
                            shares_to_buy = strategy.get_position_size(current_cash, latest_price, risk_per_trade=0.02)
                            if shares_to_buy > 0:
                                cost = shares_to_buy * latest_price
                                current_cash -= cost
                                shares_held += shares_to_buy
                                
                                trade = {
                                    "time": datetime.now().isoformat(),
                                    "symbol": symbol,
                                    "type": "buy",
                                    "price": latest_price,
                                    "quantity": shares_to_buy
                                }
                                trades_list.append(trade)  # Store in memory instead of database
                                print(f"Bought {shares_to_buy} shares at ${latest_price:.2f}")
                                
                        elif latest_signal == -1 and shares_held > 0:  # Sell signal
                            proceeds = shares_held * latest_price
                            current_cash += proceeds
                            
                            trade = {
                                "time": datetime.now().isoformat(),
                                "symbol": symbol,
                                "type": "sell",
                                "price": latest_price,
                                "quantity": shares_held
                            }
                            trades_list.append(trade)  # Store in memory instead of database
                            print(f"Sold {shares_held} shares at ${latest_price:.2f}")
                            shares_held = 0
                    
                    # Calculate current portfolio value with better tracking
                    current_portfolio_value = current_cash + (shares_held * latest_price)
                    portfolio_values.append(current_portfolio_value)
                    
                    # Calculate and log profit/loss
                    profit_loss = current_portfolio_value - global_initial_cash
                    profit_percentage = (profit_loss / global_initial_cash) * 100
                    print(f"Iteration {iteration}: Portfolio: ${current_portfolio_value:.2f} | P&L: ${profit_loss:.2f} ({profit_percentage:.2f}%)")
                    
                    # Keep only last 100 portfolio values to prevent memory issues
                    if len(portfolio_values) > 100:
                        portfolio_values.pop(0)
                    
                    iteration += 1
                    
            else:
                consecutive_failures += 1
                print(f"No data received. Failure {consecutive_failures}/{max_failures}")
                
                if consecutive_failures >= max_failures:
                    print("Too many consecutive failures. Stopping simulation.")
                    break
                    
        except Exception as e:
            consecutive_failures += 1
            print(f"Error in simulation: {e}")
            
            if consecutive_failures >= max_failures:
                print("Too many consecutive failures. Stopping simulation.")
                break
                
        time.sleep(10)  # Wait 10 seconds before next iteration
    
    print("Simulator stopped.")

@api_bp.route('/trades')
def get_trades():
    """Get all trades."""
    return jsonify(trades_list)  # Return just the trades list, not wrapped in a dict

@api_bp.route('/stock-data')
def get_stock_data():
    """Get current stock data and signals for charting."""
    if current_data.empty or current_signals.empty:
        return jsonify({
            "error": "No data available"
        }), 404
    
    # Format data for the frontend charts
    timestamps = []
    prices = []
    short_ma = []
    long_ma = []
    signals = []
    
    for i in range(len(current_signals)):
        if i < len(current_data):
            # Get timestamp
            timestamp = current_data.index[i]
            if hasattr(timestamp, 'isoformat'):
                timestamps.append(timestamp.isoformat())
            else:
                timestamps.append(str(timestamp))
            
            # Get price
            if 'Close' in current_data.columns:
                prices.append(float(current_data.iloc[i]['Close']))
            else:
                prices.append(float(current_data.iloc[i]['price']))
            
            # Get moving averages
            short_ma.append(float(current_signals.iloc[i]['short_ma']) if pd.notna(current_signals.iloc[i]['short_ma']) else None)
            long_ma.append(float(current_signals.iloc[i]['long_ma']) if pd.notna(current_signals.iloc[i]['long_ma']) else None)
            
            # Get signal
            signals.append(int(current_signals.iloc[i]['signal']))
    
    return jsonify({
        "timestamps": timestamps,
        "prices": prices,
        "short_ma": short_ma,
        "long_ma": long_ma,
        "signals": signals
    })

@api_bp.route('/portfolio-values')
def get_portfolio_values():
    """Get portfolio value history for charting."""
    if not portfolio_values:
        return jsonify({
            "timestamps": [],
            "values": [],
            "prices": [],
            "initial_cash": global_initial_cash
        })
    
    # Create timestamps for portfolio values
    timestamps = []
    values = []
    prices = []
    
    for i, value in enumerate(portfolio_values):
        # Create a timestamp based on current time minus the index using timedelta
        from datetime import timedelta
        
        # Calculate total seconds to subtract
        total_seconds_to_subtract = (len(portfolio_values) - i - 1) * 10
        
        # Use timedelta for safe time arithmetic
        timestamp = datetime.now().replace(microsecond=0) - timedelta(seconds=total_seconds_to_subtract)
        
        timestamps.append(timestamp.isoformat())
        values.append(float(value))
        
        # Get corresponding price from current_data if available
        if not current_data.empty and i < len(current_data):
            if 'Close' in current_data.columns:
                price = float(current_data.iloc[i]['Close'])
            else:
                price = float(current_data.iloc[i]['price'])
            prices.append(price)
        else:
            # Estimate price based on portfolio value
            prices.append(float(value) / 100)  # Rough estimate
    
    return jsonify({
        "timestamps": timestamps,
        "values": values,
        "prices": prices,
        "initial_cash": global_initial_cash
    })

@api_bp.route('/start-simulator', methods=['POST'])
def start_simulator():
    """Start the trading simulator."""
    global is_simulator_running, simulator_thread
    
    if is_simulator_running:
        return jsonify({
            "error": "Simulator is already running"
        }), 400
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'AAPL')
        interval = data.get('interval', '1m')
        period = data.get('period', '1d')
        initial_cash = float(data.get('initial_cash', 50000))
        selected_date = data.get('selected_date')
        
        # Validate parameters
        if initial_cash <= 0:
            return jsonify({
                "error": "Initial cash must be positive"
            }), 400
        
        # Start simulator in background thread
        is_simulator_running = True
        simulator_thread = threading.Thread(
            target=run_simulator_background,
            args=(symbol, interval, period, initial_cash, selected_date)
        )
        simulator_thread.daemon = True
        simulator_thread.start()
        
        return jsonify({
            "message": "Simulator started successfully",
            "symbol": symbol,
            "interval": interval,
            "period": period,
            "initial_cash": initial_cash,
            "selected_date": selected_date
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to start simulator: {str(e)}"
        }), 500

@api_bp.route('/stop-simulator', methods=['POST'])
def stop_simulator():
    """Stop the trading simulator."""
    global is_simulator_running
    
    if not is_simulator_running:
        return jsonify({
            "error": "Simulator is not running"
        }), 400
    
    is_simulator_running = False
    return jsonify({
        "message": "Simulator stopped successfully"
    })

@api_bp.route('/simulator-status')
def get_simulator_status():
    """Get the current status of the simulator."""
    return jsonify({
        "is_running": is_simulator_running,
        "total_trades": len(trades_list),
        "current_portfolio_value": float(portfolio_values[-1]) if portfolio_values else 0,
        "total_portfolio_values": len(portfolio_values)
    })

@api_bp.route('/performance-metrics')
def get_performance_metrics():
    """Get detailed performance metrics."""
    if not portfolio_values or len(portfolio_values) < 2:
        return jsonify({
            "error": "Insufficient data for performance calculation"
        }), 404
    
    initial_value = global_initial_cash
    current_value = portfolio_values[-1]
    total_return = current_value - initial_value
    total_return_percentage = (total_return / initial_value) * 100
    
    # Calculate maximum drawdown
    peak = initial_value
    max_drawdown = 0
    for value in portfolio_values:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    # Calculate win rate from trades
    buy_trades = [t for t in trades_list if t['type'] == 'buy']
    sell_trades = [t for t in trades_list if t['type'] == 'sell']
    
    profitable_trades = 0
    total_trades = min(len(buy_trades), len(sell_trades))
    
    for i in range(total_trades):
        if i < len(buy_trades) and i < len(sell_trades):
            buy_price = buy_trades[i]['price']
            sell_price = sell_trades[i]['price']
            if sell_price > buy_price:
                profitable_trades += 1
    
    win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
    
    return jsonify({
        "initial_value": initial_value,
        "current_value": current_value,
        "total_return": total_return,
        "total_return_percentage": total_return_percentage,
        "max_drawdown": max_drawdown,
        "total_trades": len(trades_list),
        "buy_trades": len(buy_trades),
        "sell_trades": len(sell_trades),
        "profitable_trades": profitable_trades,
        "win_rate": win_rate,
        "is_profitable": total_return > 0
    })

@api_bp.route('/clear-trades', methods=['POST'])
def clear_trades():
    """Clear all trades."""
    global trades_list, portfolio_values
    
    trades_list.clear()
    portfolio_values.clear()
    
    return jsonify({
        "message": "Trades cleared successfully"
    }) 