from flask import Blueprint, jsonify, request
import pandas as pd
from datetime import datetime, timedelta
import threading
import time
import numpy as np

# Import from core modules
from ..core.data_fetcher import DataFetcher
from ..core.strategy import TradingStrategy
from ..models.state import get_simulator_state

# Create Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Get the global state instance
simulator_state = get_simulator_state()
data_fetcher = None  # Global data fetcher instance

def run_simulator_background(symbol="AAPL", interval="1m", period="1d", initial_cash=5000, selected_date=None):
    """Run the simulator in a background thread with enhanced data handling."""
    global data_fetcher
    
    # Use more conservative strategy parameters for better profitability
    strategy = TradingStrategy(short_window=5, long_window=20, profit_threshold=0.015, stop_loss=0.01)
    
    # Initialize portfolio tracking and clear previous trades
    simulator_state.clear_portfolio_values()
    simulator_state.clear_trades()
    current_cash = initial_cash
    shares_held = 0
    simulator_state.add_portfolio_value(initial_cash)
    
    # Store initial cash for baseline calculations
    simulator_state.global_initial_cash = initial_cash
    
    iteration = 0
    consecutive_failures = 0
    max_failures = 3
    
    # Initialize data fetcher
    data_fetcher = DataFetcher(symbol=symbol, interval=interval, period=period, start_date=selected_date)
    
    # Always run historical simulation first to populate data
    print(f"Running historical simulation for {symbol}")
    
    # Fetch all historical data
    all_historical_data = data_fetcher.get_real_time_data()
    
    if all_historical_data.empty:
        print(f"No historical data available")
        return
    
    print(f"Fetched {len(all_historical_data)} data points for historical simulation")
    
    # Generate signals for all historical data
    signals_result = strategy.generate_signals(all_historical_data)
    if signals_result.success and not signals_result.signals.empty:
        simulator_state.current_data = all_historical_data
        simulator_state.current_signals = signals_result.signals
        
        # Process historical data incrementally to simulate trading
        print("Processing historical data for trading simulation...")
        
        for i, (timestamp, row) in enumerate(signals_result.signals.iterrows()):
            if not simulator_state.is_simulator_running:
                break
                
            signal = row['signal']
            price = row['price']
            
            if signal == 1 and current_cash >= price:  # Buy signal
                shares_to_buy = strategy.get_position_size(current_cash, price, risk_per_trade=0.02)
                if shares_to_buy > 0:
                    cost = shares_to_buy * price
                    current_cash -= cost
                    shares_held += shares_to_buy
                    
                    trade = {
                        "time": timestamp.isoformat(),
                        "symbol": symbol,
                        "type": "buy",
                        "price": price,
                        "quantity": shares_to_buy
                    }
                    simulator_state.add_trade(trade)
                    print(f"Historical BUY: {shares_to_buy} shares at ${price:.2f}")
                    
            elif signal == -1 and shares_held > 0:  # Sell signal
                proceeds = shares_held * price
                current_cash += proceeds
                
                trade = {
                    "time": timestamp.isoformat(),
                    "symbol": symbol,
                    "type": "sell",
                    "price": price,
                    "quantity": shares_held
                }
                simulator_state.add_trade(trade)
                print(f"Historical SELL: {shares_held} shares at ${price:.2f}")
                shares_held = 0
            
            # Calculate current portfolio value
            current_portfolio_value = current_cash + (shares_held * price)
            simulator_state.add_portfolio_value(current_portfolio_value)
            
            # Show progress every 200 iterations
            if i % 200 == 0:
                profit_loss = current_portfolio_value - simulator_state.global_initial_cash
                profit_percentage = (profit_loss / simulator_state.global_initial_cash) * 100
                print(f"Historical progress {i}/{len(signals_result.signals)}: Portfolio ${current_portfolio_value:.2f} (P&L: ${profit_loss:.2f}, {profit_percentage:.2f}%)")
        
        print(f"Historical simulation completed. Generated {len(simulator_state.trades_list)} trades.")
        
        # Calculate final results
        final_value = simulator_state.portfolio_values[-1] if simulator_state.portfolio_values else initial_cash
        total_return = final_value - initial_cash
        total_return_percentage = (total_return / initial_cash) * 100
        print(f"Final portfolio value: ${final_value:.2f} (Return: ${total_return:.2f}, {total_return_percentage:.2f}%)")
    
    # Now continue with real-time simulation if still running
    if not simulator_state.is_simulator_running:
        print("Simulator stopped after historical simulation.")
        return
    
    print(f"Starting real-time simulator for {symbol}")
    
    while simulator_state.is_simulator_running:
        try:
            # Fetch real-time data
            data = data_fetcher.get_real_time_data()
            
            if not data.empty:
                simulator_state.current_data = data
                consecutive_failures = 0  # Reset failure counter
                
                # Generate signals
                signals_result = strategy.generate_signals(data)
                if signals_result.success and not signals_result.signals.empty:
                    simulator_state.current_signals = signals_result.signals
                    
                    # Get latest price
                    latest_price = signals_result.signals["price"].iloc[-1]
                    
                    # Check if we have a signal
                    latest_signal = int(signals_result.signals["signal"].iloc[-1])
                    
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
                                simulator_state.add_trade(trade)  # Store in memory instead of database
                                print(f"Real-time BUY: {shares_to_buy} shares at ${latest_price:.2f}")
                                
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
                            simulator_state.add_trade(trade)  # Store in memory instead of database
                            print(f"Real-time SELL: {shares_held} shares at ${latest_price:.2f}")
                            shares_held = 0
                    
                    # Calculate current portfolio value with better tracking
                    current_portfolio_value = current_cash + (shares_held * latest_price)
                    simulator_state.add_portfolio_value(current_portfolio_value)
                    
                    # Calculate and log profit/loss
                    profit_loss = current_portfolio_value - simulator_state.global_initial_cash
                    profit_percentage = (profit_loss / simulator_state.global_initial_cash) * 100
                    print(f"Iteration {iteration}: Portfolio: ${current_portfolio_value:.2f} | P&L: ${profit_loss:.2f} ({profit_percentage:.2f}%)")
                    
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
                
        time.sleep(5)  # Reduced wait time for more frequent updates
    
    print("Simulator stopped.")

@api_bp.route('/trades')
def get_trades():
    """Get all trades with enhanced formatting."""
    return jsonify(simulator_state.trades_list)  # Return just the trades list, not wrapped in a dict

@api_bp.route('/stock-data')
def get_stock_data():
    """Get current stock data and signals for charting with enhanced formatting."""
    
    # If no data is available yet, try to fetch some initial data
    if simulator_state.current_data.empty or simulator_state.current_signals.empty:
        try:
            # Create a temporary data fetcher to get some initial data
            temp_fetcher = DataFetcher(symbol="AAPL", interval="1m", period="1d")
            temp_data = temp_fetcher.get_real_time_data()
            
            if not temp_data.empty:
                # Generate some basic signals for the temp data
                temp_strategy = TradingStrategy(short_window=5, long_window=20)
                temp_signals_result = temp_strategy.generate_signals(temp_data)
                
                if temp_signals_result.success and not temp_signals_result.signals.empty:
                    simulator_state.current_data = temp_data
                    simulator_state.current_signals = temp_signals_result.signals
                else:
                    return jsonify({
                        "error": "No data available"
                    }), 404
            else:
                return jsonify({
                    "error": "No data available"
                }), 404
        except Exception as e:
            return jsonify({
                "error": f"Failed to fetch initial data: {str(e)}"
            }), 500
    
    # Format data for the frontend charts with enhanced structure
    timestamps = []
    prices = []
    short_ma = []
    long_ma = []
    signals = []
    volumes = []
    
    try:
        for i in range(len(simulator_state.current_signals)):
            if i < len(simulator_state.current_data):
                # Get timestamp
                timestamp = simulator_state.current_data.index[i]
                if hasattr(timestamp, 'isoformat'):
                    timestamps.append(timestamp.isoformat())
                else:
                    timestamps.append(str(timestamp))
                
                # Get price - handle both column names
                if 'Close' in simulator_state.current_data.columns:
                    price_val = simulator_state.current_data.iloc[i]['Close']
                elif 'price' in simulator_state.current_data.columns:
                    price_val = simulator_state.current_data.iloc[i]['price']
                else:
                    price_val = 0
                
                prices.append(float(price_val) if pd.notna(price_val) else 0)
                
                # Get moving averages - handle missing values
                short_ma_val = simulator_state.current_signals.iloc[i]['short_ma'] if 'short_ma' in simulator_state.current_signals.columns else None
                long_ma_val = simulator_state.current_signals.iloc[i]['long_ma'] if 'long_ma' in simulator_state.current_signals.columns else None
                
                short_ma.append(float(short_ma_val) if pd.notna(short_ma_val) else None)
                long_ma.append(float(long_ma_val) if pd.notna(long_ma_val) else None)
                
                # Get signal
                signal_val = simulator_state.current_signals.iloc[i]['signal'] if 'signal' in simulator_state.current_signals.columns else 0
                signals.append(int(signal_val) if pd.notna(signal_val) else 0)
                
                # Get volume
                if 'Volume' in simulator_state.current_data.columns:
                    volume_val = simulator_state.current_data.iloc[i]['Volume']
                    volumes.append(float(volume_val) if pd.notna(volume_val) else 0)
                else:
                    volumes.append(0)
        
        # Add current price for immediate display
        current_price = prices[-1] if prices else 0
        
        return jsonify({
            "timestamps": timestamps,
            "prices": prices,
            "short_ma": short_ma,
            "long_ma": long_ma,
            "signals": signals,
            "volumes": volumes,
            "current_price": current_price,
            "data_points": len(timestamps)
        })
        
    except Exception as e:
        # Return a more detailed error response
        return jsonify({
            "error": f"Error formatting stock data: {str(e)}",
            "current_data_shape": simulator_state.current_data.shape if not simulator_state.current_data.empty else "empty",
            "current_signals_shape": simulator_state.current_signals.shape if not simulator_state.current_signals.empty else "empty"
        }), 500

@api_bp.route('/portfolio-values')
def get_portfolio_values():
    """Get portfolio value history for charting with enhanced formatting."""
    if not simulator_state.portfolio_values:
        return jsonify({
            "timestamps": [],
            "values": [],
            "prices": [],
            "initial_cash": simulator_state.global_initial_cash,
            "current_value": simulator_state.global_initial_cash
        })
    
    # Create timestamps for portfolio values
    timestamps = []
    values = []
    prices = []
    
    # Get current stock price for baseline calculation
    current_price = 0
    if not simulator_state.current_data.empty:
        if 'Close' in simulator_state.current_data.columns:
            current_price = float(simulator_state.current_data.iloc[-1]['Close'])
        else:
            current_price = float(simulator_state.current_data.iloc[-1]['price'])
    
    for i, value in enumerate(simulator_state.portfolio_values):
        # Create a timestamp based on current time minus the index using timedelta
        from datetime import timedelta
        
        # Calculate total seconds to subtract (more frequent updates)
        total_seconds_to_subtract = (len(simulator_state.portfolio_values) - i - 1) * 5  # 5-second intervals
        
        # Use timedelta for safe time arithmetic
        timestamp = datetime.now().replace(microsecond=0) - timedelta(seconds=total_seconds_to_subtract)
        
        timestamps.append(timestamp.isoformat())
        values.append(float(value))
        
        # Get corresponding price from current_data if available
        if not simulator_state.current_data.empty and i < len(simulator_state.current_data):
            if 'Close' in simulator_state.current_data.columns:
                price = float(simulator_state.current_data.iloc[i]['Close'])
            else:
                price = float(simulator_state.current_data.iloc[i]['price'])
            prices.append(price)
        else:
            # Estimate price based on portfolio value
            prices.append(current_price if current_price > 0 else float(value) / 100)
    
    return jsonify({
        "timestamps": timestamps,
        "values": values,
        "prices": prices,
        "initial_cash": simulator_state.global_initial_cash,
        "current_value": float(simulator_state.portfolio_values[-1]) if simulator_state.portfolio_values else simulator_state.global_initial_cash
    })

@api_bp.route('/start-simulator', methods=['POST'])
def start_simulator():
    """Start the trading simulator."""
    
    if simulator_state.is_simulator_running:
        return jsonify({
            "error": "Simulator is already running"
        }), 400
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'AAPL')
        interval = data.get('interval', '1m')
        period = data.get('period', '1d')
        initial_cash = float(data.get('initial_cash', 5000))
        selected_date = data.get('selected_date')
        
        # Validate parameters
        if initial_cash <= 0:
            return jsonify({
                "error": "Initial cash must be positive"
            }), 400
        
        # Start simulator in background thread
        simulator_state.is_simulator_running = True
        simulator_thread = threading.Thread(
            target=run_simulator_background,
            args=(symbol, interval, period, initial_cash, selected_date)
        )
        simulator_thread.daemon = True
        simulator_state.simulator_thread = simulator_thread
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
    
    if not simulator_state.is_simulator_running:
        return jsonify({
            "error": "Simulator is not running"
        }), 400
    
    simulator_state.is_simulator_running = False
    return jsonify({
        "message": "Simulator stopped successfully"
    })

@api_bp.route('/simulator-status')
def get_simulator_status():
    """Get the current status of the simulator."""
    return jsonify({
        "is_running": simulator_state.is_simulator_running,
        "total_trades": len(simulator_state.trades_list),
        "current_portfolio_value": float(simulator_state.portfolio_values[-1]) if simulator_state.portfolio_values else simulator_state.global_initial_cash,
        "total_portfolio_values": len(simulator_state.portfolio_values),
        "initial_cash": simulator_state.global_initial_cash
    })

@api_bp.route('/performance-metrics')
def get_performance_metrics():
    """Get detailed performance metrics with enhanced calculations."""
    try:
        if not simulator_state.portfolio_values or len(simulator_state.portfolio_values) < 2:
            # Return default metrics when insufficient data
            return jsonify({
                "initial_value": simulator_state.global_initial_cash,
                "current_value": simulator_state.global_initial_cash,
                "total_return": 0.0,
                "total_return_percentage": 0.0,
                "max_drawdown": 0.0,
                "total_trades": len(simulator_state.trades_list),
                "buy_trades": len([t for t in simulator_state.trades_list if t['type'] == 'buy']),
                "sell_trades": len([t for t in simulator_state.trades_list if t['type'] == 'sell']),
                "profitable_trades": 0,
                "win_rate": 0.0,
                "avg_trade_return": 0.0,
                "is_profitable": True
            })
        
        initial_value = simulator_state.global_initial_cash
        current_value = simulator_state.portfolio_values[-1] if simulator_state.portfolio_values else simulator_state.global_initial_cash
        total_return = current_value - initial_value
        total_return_percentage = (total_return / initial_value) * 100
        
        # Calculate maximum drawdown
        peak = initial_value
        max_drawdown = 0
        for value in simulator_state.portfolio_values:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # Calculate win rate from trades
        buy_trades = [t for t in simulator_state.trades_list if t['type'] == 'buy']
        sell_trades = [t for t in simulator_state.trades_list if t['type'] == 'sell']
        
        profitable_trades = 0
        total_trades = min(len(buy_trades), len(sell_trades))
        
        for i in range(total_trades):
            if i < len(buy_trades) and i < len(sell_trades):
                try:
                    buy_price = float(buy_trades[i]['price'])
                    sell_price = float(sell_trades[i]['price'])
                    if sell_price > buy_price:
                        profitable_trades += 1
                except (ValueError, TypeError, KeyError):
                    # Skip invalid trade data
                    continue
        
        win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate additional metrics
        avg_trade_return = 0
        if total_trades > 0:
            total_trade_returns = []
            for i in range(total_trades):
                if i < len(buy_trades) and i < len(sell_trades):
                    try:
                        buy_price = float(buy_trades[i]['price'])
                        sell_price = float(sell_trades[i]['price'])
                        if buy_price > 0:  # Avoid division by zero
                            trade_return = (sell_price - buy_price) / buy_price * 100
                            total_trade_returns.append(trade_return)
                    except (ValueError, TypeError, KeyError, ZeroDivisionError):
                        # Skip invalid trade data
                        continue
            
            if total_trade_returns:
                avg_trade_return = sum(total_trade_returns) / len(total_trade_returns)
        
        return jsonify({
            "initial_value": initial_value,
            "current_value": current_value,
            "total_return": total_return,
            "total_return_percentage": total_return_percentage,
            "max_drawdown": max_drawdown,
            "total_trades": len(simulator_state.trades_list),
            "buy_trades": len(buy_trades),
            "sell_trades": len(sell_trades),
            "profitable_trades": profitable_trades,
            "win_rate": win_rate,
            "avg_trade_return": avg_trade_return,
            "is_profitable": bool(total_return > 0)
        })
        
    except Exception as e:
        print(f"Error in performance metrics: {e}")
        # Return a simplified response on error
        return jsonify({
            "initial_value": simulator_state.global_initial_cash,
            "current_value": simulator_state.portfolio_values[-1] if simulator_state.portfolio_values else simulator_state.global_initial_cash,
            "total_return": 0.0,
            "total_return_percentage": 0.0,
            "max_drawdown": 0.0,
            "total_trades": len(simulator_state.trades_list),
            "buy_trades": len([t for t in simulator_state.trades_list if t['type'] == 'buy']),
            "sell_trades": len([t for t in simulator_state.trades_list if t['type'] == 'sell']),
            "profitable_trades": 0,
            "win_rate": 0.0,
            "avg_trade_return": 0.0,
            "is_profitable": True,
            "error": str(e)
        })

@api_bp.route('/clear-trades', methods=['POST'])
def clear_trades():
    """Clear all trades."""
    
    simulator_state.clear_trades()
    simulator_state.clear_portfolio_values()
    
    return jsonify({
        "message": "Trades cleared successfully"
    })

@api_bp.route('/current-price')
def get_current_price():
    """Get the current stock price."""
    if simulator_state.current_data.empty:
        return jsonify({
            "error": "No data available"
        }), 404
    
    try:
        if 'Close' in simulator_state.current_data.columns:
            current_price = float(simulator_state.current_data.iloc[-1]['Close'])
        else:
            current_price = float(simulator_state.current_data.iloc[-1]['price'])
        
        return jsonify({
            "current_price": current_price,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to get current price: {str(e)}"
        }), 500 