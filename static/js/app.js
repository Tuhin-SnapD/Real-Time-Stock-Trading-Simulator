/**
 * Real-Time Stock Trading Simulator - Main JavaScript
 */

class TradingSimulator {
    constructor() {
        this.isRunning = false;
        this.updateInterval = null;
        this.charts = {};
        this.currentData = {};
        this.initialCash = 5000; // Default initial cash
        this.baselineValues = []; // Store baseline portfolio values
        
        this.initializeEventListeners();
        this.initializeCharts();
        this.prePopulateForm();
        this.checkSimulatorStatus();
    }
    
    prePopulateForm() {
        // Pre-populate symbol with AAPL
        const symbolSelect = document.getElementById('stockSymbol');
        if (symbolSelect) {
            symbolSelect.value = 'AAPL';
        }
        
        // Pre-populate initial cash with 5000
        const initialCashInput = document.getElementById('initialCash');
        if (initialCashInput) {
            initialCashInput.value = this.initialCash;
        }
    }
    
    initializeEventListeners() {
        // Start simulator button
        document.getElementById('startBtn').addEventListener('click', () => {
            this.startSimulator();
        });
        
        // Stop simulator button
        document.getElementById('stopBtn').addEventListener('click', () => {
            this.stopSimulator();
        });
        
        // Clear trades button - check if it exists
        const clearTradesBtn = document.getElementById('clearTrades');
        if (clearTradesBtn) {
            clearTradesBtn.addEventListener('click', () => {
                this.clearTrades();
            });
        }
        
        // Historical mode toggle - check if it exists
        const historicalModeToggle = document.getElementById('historicalMode');
        if (historicalModeToggle) {
            historicalModeToggle.addEventListener('change', (e) => {
                this.toggleHistoricalMode(e.target.checked);
            });
        }
    }
    
    initializeCharts() {
        // Initialize stock price chart
        this.charts.stockChart = this.createStockChart();
        
        // Initialize portfolio chart
        this.charts.portfolioChart = this.createPortfolioChart();
    }
    
    createStockChart() {
        const trace1 = {
            x: [],
            y: [],
            type: 'scatter',
            mode: 'lines',
            name: 'Stock Price',
            line: { color: '#3498db', width: 2 }
        };
        
        const trace2 = {
            x: [],
            y: [],
            type: 'scatter',
            mode: 'lines',
            name: 'Short MA',
            line: { color: '#e74c3c', width: 1, dash: 'dash' }
        };
        
        const trace3 = {
            x: [],
            y: [],
            type: 'scatter',
            mode: 'lines',
            name: 'Long MA',
            line: { color: '#f39c12', width: 1, dash: 'dash' }
        };
        
        const layout = {
            title: 'Stock Price & Moving Averages',
            xaxis: { 
                title: 'Time',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)'
            },
            yaxis: { 
                title: 'Price ($)',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                autorange: true // Enable auto-scaling
            },
            height: 400,
            margin: { l: 50, r: 50, t: 50, b: 50 },
            plot_bgcolor: 'rgba(255,255,255,0.8)',
            paper_bgcolor: 'rgba(255,255,255,0.8)',
            hovermode: 'x unified'
        };
        
        return Plotly.newPlot('stockChart', [trace1, trace2, trace3], layout, {
            responsive: true,
            displayModeBar: false
        });
    }
    
    createPortfolioChart() {
        const trace = {
            x: [],
            y: [],
            type: 'scatter',
            mode: 'lines',
            name: 'Portfolio Value',
            line: { color: '#27ae60', width: 3 },
            fill: 'tonexty',
            fillcolor: 'rgba(39, 174, 96, 0.1)'
        };
        
        // Add baseline trace
        const baselineTrace = {
            x: [],
            y: [],
            type: 'scatter',
            mode: 'lines',
            name: 'Baseline (Buy & Hold)',
            line: { color: '#95a5a6', width: 2, dash: 'dot' },
            opacity: 0.7
        };
        
        const layout = {
            title: 'Portfolio Value Over Time',
            xaxis: { 
                title: 'Time',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)'
            },
            yaxis: { 
                title: 'Value ($)',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                autorange: true // Enable auto-scaling
            },
            height: 300,
            margin: { l: 50, r: 50, t: 50, b: 50 },
            plot_bgcolor: 'rgba(255,255,255,0.8)',
            paper_bgcolor: 'rgba(255,255,255,0.8)',
            hovermode: 'x unified',
            showlegend: true
        };
        
        return Plotly.newPlot('portfolioChart', [trace, baselineTrace], layout, {
            responsive: true,
            displayModeBar: false
        });
    }
    
    async startSimulator() {
        const symbol = document.getElementById('stockSymbol').value;
        const interval = document.getElementById('interval').value;
        const period = document.getElementById('period').value;
        const initialCash = parseFloat(document.getElementById('initialCash').value);
        const historicalMode = document.getElementById('historicalMode').checked;
        const selectedDate = historicalMode ? document.getElementById('selectedDate').value : null;
        
        if (!symbol || initialCash <= 0) {
            this.showAlert('Please enter valid parameters', 'danger');
            return;
        }
        
        if (historicalMode && !selectedDate) {
            this.showAlert('Please select a date for historical mode', 'danger');
            return;
        }
        
        try {
            this.showLoading(true);
            
            const response = await fetch('/api/start-simulator', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    symbol: symbol,
                    interval: interval,
                    period: period,
                    initial_cash: initialCash,
                    selected_date: selectedDate
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showAlert(data.message, 'success');
                this.isRunning = true;
                this.updateUI();
                this.startDataUpdates();
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('Failed to start simulator: ' + error.message, 'danger');
        } finally {
            this.showLoading(false);
        }
    }
    
    async stopSimulator() {
        try {
            const response = await fetch('/api/stop-simulator', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showAlert(data.message, 'success');
                this.isRunning = false;
                this.updateUI();
                this.stopDataUpdates();
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('Failed to stop simulator: ' + error.message, 'danger');
        }
    }
    
    async clearTrades() {
        try {
            const response = await fetch('/api/clear-trades', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showAlert(data.message, 'success');
                this.updateTradesTable([]);
                this.updatePortfolioChart([]);
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('Failed to clear trades: ' + error.message, 'danger');
        }
    }
    
    startDataUpdates() {
        this.updateInterval = setInterval(() => {
            this.updateStockData();
            this.updateTrades();
            this.updatePortfolioValues();
        }, 5000); // Update every 5 seconds
    }
    
    stopDataUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }
    
    async updateStockData() {
        try {
            const response = await fetch('/api/stock-data');
            const data = await response.json();
            
            if (response.ok && data.current_price) {
                this.currentData = data;
                this.updateStockChart(data);
                this.updateCurrentPrice(data);
            }
        } catch (error) {
            console.error('Failed to update stock data:', error);
        }
    }
    
    async updateTrades() {
        try {
            const response = await fetch('/api/trades');
            const data = await response.json();
            
            if (response.ok) {
                this.updateTradesTable(data.trades || []);
            }
        } catch (error) {
            console.error('Failed to update trades:', error);
        }
    }
    
    async updatePortfolioValues() {
        try {
            const response = await fetch('/api/portfolio-values');
            const data = await response.json();
            
            if (response.ok) {
                this.updatePortfolioChart(data.portfolio_values || []);
                this.updatePortfolioStats(data.current_value || 0);
            }
        } catch (error) {
            console.error('Failed to update portfolio values:', error);
        }
    }
    
    updateStockChart(data) {
        if (!data || !data.timestamps || !data.prices) return;
        
        const traces = [
            {
                x: data.timestamps,
                y: data.prices,
                type: 'scatter',
                mode: 'lines',
                name: 'Stock Price',
                line: { color: '#3498db', width: 2 }
            }
        ];
        
        // Add moving averages if available
        if (data.short_ma && data.short_ma.length > 0) {
            traces.push({
                x: data.timestamps,
                y: data.short_ma,
                type: 'scatter',
                mode: 'lines',
                name: 'Short MA',
                line: { color: '#e74c3c', width: 1, dash: 'dash' }
            });
        }
        
        if (data.long_ma && data.long_ma.length > 0) {
            traces.push({
                x: data.timestamps,
                y: data.long_ma,
                type: 'scatter',
                mode: 'lines',
                name: 'Long MA',
                line: { color: '#f39c12', width: 1, dash: 'dash' }
            });
        }
        
        // Update the chart with new data
        Plotly.react('stockChart', traces, {
            title: 'Stock Price & Moving Averages',
            xaxis: { 
                title: 'Time',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)'
            },
            yaxis: { 
                title: 'Price ($)',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                autorange: true // Enable auto-scaling
            },
            height: 400,
            margin: { l: 50, r: 50, t: 50, b: 50 },
            plot_bgcolor: 'rgba(255,255,255,0.8)',
            paper_bgcolor: 'rgba(255,255,255,0.8)',
            hovermode: 'x unified'
        }, {
            responsive: true,
            displayModeBar: false
        });
    }
    
    updatePortfolioChart(portfolioData) {
        if (portfolioData.length === 0) return;
        
        const x = portfolioData.map((item, index) => index);
        const y = portfolioData.map(item => item.value);
        
        // Calculate baseline (buy & hold strategy)
        const baselineY = this.calculateBaselineValues(portfolioData);
        
        // Update both portfolio and baseline traces
        Plotly.update('portfolioChart', {
            x: [x, x],
            y: [y, baselineY]
        });
        
        // Ensure proper scaling by setting autorange
        Plotly.relayout('portfolioChart', {
            'yaxis.autorange': true
        });
    }
    
    calculateBaselineValues(portfolioData) {
        if (portfolioData.length === 0) return [];
        
        const initialCash = this.initialCash;
        const baselineValues = [];
        
        // Calculate what the portfolio would be worth if we bought and held
        // We'll use the first price as our entry point
        const firstPrice = portfolioData[0].price || portfolioData[0].value / initialCash;
        
        portfolioData.forEach((item, index) => {
            const currentPrice = item.price || (item.value / initialCash);
            const sharesOwned = initialCash / firstPrice;
            const baselineValue = sharesOwned * currentPrice;
            baselineValues.push(baselineValue);
        });
        
        return baselineValues;
    }
    
    updateTradesTable(trades) {
        const tableBody = document.getElementById('tradesTableBody');
        tableBody.innerHTML = '';
        
        trades.slice(-10).reverse().forEach(trade => {
            const row = document.createElement('tr');
            row.className = `trade-row trade-${trade.type}`;
            
            row.innerHTML = `
                <td>${new Date(trade.time).toLocaleString()}</td>
                <td>${trade.symbol}</td>
                <td><span class="badge badge-${trade.type === 'buy' ? 'success' : 'danger'}">${trade.type.toUpperCase()}</span></td>
                <td>$${trade.price.toFixed(2)}</td>
                <td>${trade.quantity}</td>
                <td>$${(trade.price * trade.quantity).toFixed(2)}</td>
            `;
            
            tableBody.appendChild(row);
        });
    }
    
    updateCurrentPrice(data) {
        const priceElement = document.getElementById('currentPrice');
        if (priceElement) {
            priceElement.textContent = `$${data.current_price.toFixed(2)}`;
        }
    }
    
    updatePortfolioStats(currentValue) {
        const valueElement = document.getElementById('portfolioValue');
        if (valueElement) {
            valueElement.textContent = `$${currentValue.toFixed(2)}`;
        }
    }
    
    updateUI() {
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const statusIndicator = document.getElementById('statusIndicator');
        
        if (!startBtn || !stopBtn || !statusIndicator) return;
        
        if (this.isRunning) {
            startBtn.disabled = true;
            stopBtn.disabled = false;
            statusIndicator.className = 'status-indicator status-running';
            statusIndicator.title = 'Running';
        } else {
            startBtn.disabled = false;
            stopBtn.disabled = true;
            statusIndicator.className = 'status-indicator status-stopped';
            statusIndicator.title = 'Stopped';
        }
    }
    
    toggleHistoricalMode(enabled) {
        const dateInput = document.getElementById('selectedDate');
        dateInput.disabled = !enabled;
        
        if (enabled) {
            dateInput.required = true;
        } else {
            dateInput.required = false;
            dateInput.value = '';
        }
    }
    
    async checkSimulatorStatus() {
        try {
            const response = await fetch('/api/simulator-status');
            const data = await response.json();
            
            this.isRunning = data.is_running;
            this.updateUI();
            
            if (this.isRunning) {
                this.startDataUpdates();
            }
        } catch (error) {
            console.error('Failed to check simulator status:', error);
        }
    }
    
    showAlert(message, type) {
        const alertContainer = document.getElementById('alertContainer');
        const alertId = 'alert-' + Date.now();
        
        const alertHtml = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `;
        
        alertContainer.innerHTML = alertHtml;
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) {
                alert.remove();
            }
        }, 5000);
    }
    
    showLoading(show) {
        const startBtn = document.getElementById('startBtn');
        if (!startBtn) return;
        
        if (show) {
            startBtn.disabled = true;
            startBtn.innerHTML = '<span class="loading-spinner"></span> Starting...';
        } else {
            startBtn.disabled = false;
            startBtn.innerHTML = '<i class="fas fa-play"></i> Start Simulator';
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.tradingSimulator = new TradingSimulator();
}); 