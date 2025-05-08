import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_results(signals, portfolio_values, symbol="AAPL"):
    """Plot price, moving averages, signals, and portfolio value."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        subplot_titles=("Price and Signals", "Portfolio Value"),
                        vertical_spacing=0.1)

    # Plot price and moving averages
    fig.add_trace(go.Scatter(x=signals.index, y=signals["price"], name="Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=signals.index, y=signals["short_ma"], name="Short MA"), row=1, col=1)
    fig.add_trace(go.Scatter(x=signals.index, y=signals["long_ma"], name="Long MA"), row=1, col=1)

    # Plot buy/sell signals
    buy_signals = signals[signals["signal"] == 1]
    sell_signals = signals[signals["signal"] == -1]
    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals["price"], mode="markers", 
                             name="Buy", marker=dict(symbol="triangle-up", size=10, color="green")), row=1, col=1)
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals["price"], mode="markers", 
                             name="Sell", marker=dict(symbol="triangle-down", size=10, color="red")), row=1, col=1)

    # Plot portfolio value
    fig.add_trace(go.Scatter(x=signals.index, y=portfolio_values, name="Portfolio Value"), row=2, col=1)

    fig.update_layout(title=f"Trading Simulator Results for {symbol}", showlegend=True)
    fig.show()