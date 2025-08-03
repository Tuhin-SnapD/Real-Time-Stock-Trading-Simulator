# API Documentation

## Overview

The Real-Time Stock Trading Simulator provides a RESTful API for managing trading simulations, fetching stock data, and retrieving trading results.

## Base URL

```
http://localhost:5000/api
```

## Authentication

Currently, the API does not require authentication. In production, consider implementing API key authentication or JWT tokens.

## Response Format

All API responses are returned in JSON format with the following structure:

```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully",
  "error": null
}
```

## Endpoints

### 1. Simulator Status

**GET** `/api/simulator-status`

Get the current status of the trading simulator.

**Response:**
```json
{
  "is_running": true,
  "total_trades": 15,
  "current_portfolio_value": 52345.67,
  "total_portfolio_values": 100
}
```

### 2. Start Simulator

**POST** `/api/start-simulator`

Start a new trading simulation.

**Request Body:**
```json
{
  "symbol": "AAPL",
  "interval": "1m",
  "period": "1d",
  "initial_cash": 50000,
  "selected_date": "2024-01-15"
}
```

**Parameters:**
- `symbol` (string, required): Stock symbol (e.g., "AAPL", "MSFT")
- `interval` (string, optional): Data interval ("1m", "5m", "15m", "30m", "1h", "1d")
- `period` (string, optional): Data period ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
- `initial_cash` (number, optional): Initial cash amount (default: 50000)
- `selected_date` (string, optional): Historical date for backtesting (format: "YYYY-MM-DD")

**Response:**
```json
{
  "message": "Simulator started successfully",
  "symbol": "AAPL",
  "interval": "1m",
  "period": "1d",
  "initial_cash": 50000,
  "selected_date": "2024-01-15"
}
```

**Error Response:**
```json
{
  "error": "Simulator is already running"
}
```

### 3. Stop Simulator

**POST** `/api/stop-simulator`

Stop the currently running trading simulation.

**Response:**
```json
{
  "message": "Simulator stopped successfully"
}
```

**Error Response:**
```json
{
  "error": "Simulator is not running"
}
```

### 4. Get Stock Data

**GET** `/api/stock-data`

Get current stock data and trading signals.

**Response:**
```json
{
  "symbol": "AAPL",
  "current_price": 150.25,
  "open": 149.50,
  "high": 151.00,
  "low": 149.25,
  "volume": 1250000,
  "short_ma": 150.10,
  "long_ma": 149.85,
  "signal": 1,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Error Response:**
```json
{
  "error": "No data available"
}
```

### 5. Get Trades

**GET** `/api/trades`

Get the list of all trades executed during the simulation.

**Response:**
```json
{
  "trades": [
    {
      "time": "2024-01-15T10:30:00Z",
      "symbol": "AAPL",
      "type": "buy",
      "price": 150.25,
      "quantity": 332,
      "total_value": 49883.00
    },
    {
      "time": "2024-01-15T11:15:00Z",
      "symbol": "AAPL",
      "type": "sell",
      "price": 151.50,
      "quantity": 332,
      "total_value": 50298.00
    }
  ],
  "total_trades": 2
}
```

### 6. Get Portfolio Values

**GET** `/api/portfolio-values`

Get the portfolio value history over time.

**Response:**
```json
{
  "portfolio_values": [
    {
      "index": 0,
      "value": 50000.00,
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "index": 1,
      "value": 49883.00,
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "index": 2,
      "value": 50298.00,
      "timestamp": "2024-01-15T11:15:00Z"
    }
  ],
  "current_value": 50298.00
}
```

### 7. Clear Trades

**POST** `/api/clear-trades`

Clear all trades and reset the simulation data.

**Response:**
```json
{
  "message": "Trades cleared successfully"
}
```

## Error Handling

### HTTP Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "error": "Error message description",
  "details": "Additional error details (optional)"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. In production, consider implementing rate limiting to prevent abuse.

## Data Formats

### Date Format
All dates are returned in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

### Number Format
- Prices are returned as floating-point numbers with 2 decimal places
- Quantities are returned as integers
- Portfolio values are returned as floating-point numbers

## Examples

### Starting a Real-time Simulation

```bash
curl -X POST http://localhost:5000/api/start-simulator \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "interval": "1m",
    "period": "1d",
    "initial_cash": 50000
  }'
```

### Starting a Historical Simulation

```bash
curl -X POST http://localhost:5000/api/start-simulator \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "interval": "1m",
    "period": "1d",
    "initial_cash": 50000,
    "selected_date": "2024-01-15"
  }'
```

### Getting Current Status

```bash
curl http://localhost:5000/api/simulator-status
```

### Getting Trade History

```bash
curl http://localhost:5000/api/trades
```

## WebSocket Support

Future versions may include WebSocket support for real-time updates without polling.

## Versioning

The API version is included in the URL path. Current version: v1

```
http://localhost:5000/api/v1/...
```

## Support

For API support and questions, please refer to the main project documentation or create an issue on GitHub. 