/**
 * Real-Time Stock Trading Simulator - Enhanced JavaScript
 * Features: Modern charts, real-time animations, professional styling
 */

class TradingSimulator {
    constructor() {
        this.isRunning = false;
        this.updateInterval = null;
        this.charts = {};
        this.currentData = {};
        this.initialCash = 5000;
        this.baselineValues = [];
        this.chartColors = {
            primary: '#667eea',
            secondary: '#764ba2',
            success: '#27ae60',
            danger: '#e74c3c',
            warning: '#f39c12',
            info: '#17a2b8',
            light: '#ecf0f1',
            dark: '#2c3e50'
        };
        
        this.initializeEventListeners();
        this.initializeCharts();
        this.prePopulateForm();
        this.checkSimulatorStatus();
    }
    
    prePopulateForm() {
        const symbolSelect = document.getElementById('stockSymbol');
        if (symbolSelect) {
            symbolSelect.value = 'AAPL';
        }
        
        const initialCashInput = document.getElementById('initialCash');
        if (initialCashInput) {
            initialCashInput.value = this.initialCash;
        }
    }
    
    initializeEventListeners() {
        document.getElementById('startBtn').addEventListener('click', () => {
            this.startSimulator();
        });
        
        document.getElementById('stopBtn').addEventListener('click', () => {
            this.stopSimulator();
        });
        
        const clearTradesBtn = document.getElementById('clearTrades');
        if (clearTradesBtn) {
            clearTradesBtn.addEventListener('click', () => {
                this.clearTrades();
            });
        }
        
        const historicalModeToggle = document.getElementById('historicalMode');
        if (historicalModeToggle) {
            historicalModeToggle.addEventListener('change', (e) => {
                this.toggleHistoricalMode(e.target.checked);
            });
        }
    }
    
    initializeCharts() {
        // Initialize with empty states and helpful messages
        this.charts.stockChart = this.createStockChart();
        this.charts.portfolioChart = this.createPortfolioChart();
        
        // Add chart responsiveness
        window.addEventListener('resize', () => {
            this.resizeCharts();
        });
    }
    
    createStockChart() {
        const trace1 = {
            x: [],
            y: [],
            type: 'scatter',
            mode: 'lines',
            name: 'Stock Price',
            line: { 
                color: this.chartColors.primary, 
                width: 3,
                shape: 'spline'
            },
            fill: 'tonexty',
            fillcolor: 'rgba(102, 126, 234, 0.1)'
        };
        
        const layout = {
            title: {
                text: 'Stock Price & Trading Signals',
                font: { size: 18, color: this.chartColors.dark },
                x: 0.5
            },
            xaxis: { 
                title: 'Time',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                zeroline: false,
                rangeslider: { visible: false }
            },
            yaxis: { 
                title: 'Price ($)',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                zeroline: false,
                autorange: true
            },
            height: 450,
            margin: { l: 60, r: 60, t: 80, b: 60 },
            plot_bgcolor: 'rgba(255,255,255,0.9)',
            paper_bgcolor: 'rgba(255,255,255,0.9)',
            hovermode: 'x unified',
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.8)',
                bordercolor: 'rgba(0,0,0,0.1)',
                borderwidth: 1
            },
            font: {
                family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
            },
            annotations: [{
                text: 'Click "Start Simulator" to begin trading and see live data',
                xref: 'paper',
                yref: 'paper',
                x: 0.5,
                y: 0.5,
                xanchor: 'center',
                yanchor: 'middle',
                showarrow: false,
                font: {
                    size: 16,
                    color: '#7f8c8d'
                },
                bgcolor: 'rgba(255,255,255,0.8)',
                bordercolor: 'rgba(0,0,0,0.1)',
                borderwidth: 1,
                pad: 10
            }]
        };
        
        const config = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false
        };
        
        return Plotly.newPlot('stockChart', [trace1], layout, config);
    }
    
    createPortfolioChart() {
        const trace = {
            x: [],
            y: [],
            type: 'scatter',
            mode: 'lines',
            name: 'Portfolio Value',
            line: { 
                color: this.chartColors.success, 
                width: 4,
                shape: 'spline'
            },
            fill: 'tonexty',
            fillcolor: 'rgba(39, 174, 96, 0.1)'
        };
        
        const layout = {
            title: {
                text: 'Portfolio Performance vs Buy & Hold',
                font: { size: 16, color: this.chartColors.dark },
                x: 0.5
            },
            xaxis: { 
                title: 'Time',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                zeroline: false,
                rangeslider: { visible: false }
            },
            yaxis: { 
                title: 'Value ($)',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                zeroline: false,
                autorange: true
            },
            height: 350,
            margin: { l: 60, r: 60, t: 80, b: 60 },
            plot_bgcolor: 'rgba(255,255,255,0.9)',
            paper_bgcolor: 'rgba(255,255,255,0.9)',
            hovermode: 'x unified',
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.8)',
                bordercolor: 'rgba(0,0,0,0.1)',
                borderwidth: 1
            },
            font: {
                family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
            },
            annotations: [{
                text: 'Portfolio performance will appear here once trading begins',
                xref: 'paper',
                yref: 'paper',
                x: 0.5,
                y: 0.5,
                xanchor: 'center',
                yanchor: 'middle',
                showarrow: false,
                font: {
                    size: 14,
                    color: '#7f8c8d'
                },
                bgcolor: 'rgba(255,255,255,0.8)',
                bordercolor: 'rgba(0,0,0,0.1)',
                borderwidth: 1,
                pad: 10
            }]
        };
        
        const config = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false
        };
        
        return Plotly.newPlot('portfolioChart', [trace], layout, config);
    }
    
    async startSimulator() {
        const symbol = document.getElementById('stockSymbol').value;
        const interval = document.getElementById('interval').value;
        const period = document.getElementById('period').value;
        const initialCash = parseFloat(document.getElementById('initialCash').value);
        const historicalMode = document.getElementById('historicalMode')?.checked || false;
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
                this.showAlert(`Simulator started successfully! Trading ${symbol} with $${initialCash.toLocaleString()} initial cash.`, 'success');
                this.isRunning = true;
                this.initialCash = initialCash;
                this.updateUI();
                this.startDataUpdates();
                
                // Update status indicators to show simulator is starting
                this.updateRealTimeIndicator('stockUpdateStatus', 'Simulator starting...');
                this.updateRealTimeIndicator('portfolioUpdateStatus', 'Simulator starting...');
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
                this.resetCharts();
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('Failed to clear trades: ' + error.message, 'danger');
        }
    }
    
    startDataUpdates() {
        // More frequent updates for smoother animations and better responsiveness
        this.updateInterval = setInterval(() => {
            this.updateStockData();
            this.updateTrades();
            this.updatePortfolioValues();
        }, 2000); // Update every 2 seconds for better responsiveness
        
        // Immediate first update
        setTimeout(() => {
            this.updateStockData();
            this.updateTrades();
            this.updatePortfolioValues();
        }, 100);
        
        // Additional update after 1 second to ensure data is loaded
        setTimeout(() => {
            this.updateStockData();
            this.updateTrades();
            this.updatePortfolioValues();
        }, 1000);
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
            
            if (response.ok && data.timestamps && data.prices && data.timestamps.length > 0) {
                this.currentData = data;
                this.updateStockChart(data);
                this.updateCurrentPrice(data);
                this.updateRealTimeIndicator('stockUpdateStatus');
            } else if (response.status === 404) {
                // If no data available, show a message but don't error
                console.log('No stock data available yet. Waiting for simulator to start...');
                this.updateRealTimeIndicator('stockUpdateStatus', 'Waiting for data...');
                // Update chart with empty state
                this.updateStockChart({ timestamps: [], prices: [] });
            } else {
                console.error('Failed to update stock data:', data.error || 'Unknown error');
                this.updateRealTimeIndicator('stockUpdateStatus', 'Error loading data');
                // Update chart with empty state
                this.updateStockChart({ timestamps: [], prices: [] });
            }
        } catch (error) {
            console.error('Failed to update stock data:', error);
            this.updateRealTimeIndicator('stockUpdateStatus', 'Connection error');
            // Update chart with empty state
            this.updateStockChart({ timestamps: [], prices: [] });
        }
    }
    
    async updateTrades() {
        try {
            const response = await fetch('/api/trades');
            const data = await response.json();
            
            if (response.ok) {
                this.updateTradesTable(data);
                this.updateStats(data);
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
                this.updatePortfolioChart(data);
                this.updatePortfolioStats(data.current_value || 0);
                this.updateRealTimeIndicator('portfolioUpdateStatus');
            } else {
                console.error('Failed to update portfolio values:', data.error || 'Unknown error');
                this.updateRealTimeIndicator('portfolioUpdateStatus', 'Error loading data');
                // Update chart with empty state
                this.updatePortfolioChart({ timestamps: [], values: [] });
            }
        } catch (error) {
            console.error('Failed to update portfolio values:', error);
            this.updateRealTimeIndicator('portfolioUpdateStatus', 'Connection error');
            // Update chart with empty state
            this.updatePortfolioChart({ timestamps: [], values: [] });
        }
    }
    
    updateStockChart(data) {
        if (!data || !data.timestamps || !data.prices || data.timestamps.length === 0) {
            // Show empty state with helpful message
            const emptyTrace = {
                x: [],
                y: [],
                type: 'scatter',
                mode: 'lines',
                name: 'Stock Price',
                line: { 
                    color: this.chartColors.primary, 
                    width: 3,
                    shape: 'spline'
                }
            };
            
            const layout = {
                title: {
                    text: 'Stock Price & Trading Signals',
                    font: { size: 18, color: this.chartColors.dark },
                    x: 0.5
                },
                xaxis: { 
                    title: 'Time',
                    showgrid: true,
                    gridcolor: 'rgba(0,0,0,0.1)',
                    zeroline: false,
                    rangeslider: { visible: false }
                },
                yaxis: { 
                    title: 'Price ($)',
                    showgrid: true,
                    gridcolor: 'rgba(0,0,0,0.1)',
                    zeroline: false,
                    autorange: true
                },
                height: 450,
                margin: { l: 60, r: 60, t: 80, b: 60 },
                plot_bgcolor: 'rgba(255,255,255,0.9)',
                paper_bgcolor: 'rgba(255,255,255,0.9)',
                hovermode: 'x unified',
                showlegend: true,
                legend: {
                    x: 0.02,
                    y: 0.98,
                    bgcolor: 'rgba(255,255,255,0.8)',
                    bordercolor: 'rgba(0,0,0,0.1)',
                    borderwidth: 1
                },
                font: {
                    family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
                },
                annotations: [{
                    text: 'Click "Start Simulator" to begin trading and see live data',
                    xref: 'paper',
                    yref: 'paper',
                    x: 0.5,
                    y: 0.5,
                    xanchor: 'center',
                    yanchor: 'middle',
                    showarrow: false,
                    font: {
                        size: 16,
                        color: '#7f8c8d'
                    },
                    bgcolor: 'rgba(255,255,255,0.8)',
                    bordercolor: 'rgba(0,0,0,0.1)',
                    borderwidth: 1,
                    pad: 10
                }]
            };
            
            Plotly.react('stockChart', [emptyTrace], layout, {
                responsive: true,
                displayModeBar: true,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
                displaylogo: false
            });
            return;
        }
        
        const traces = [
            {
                x: data.timestamps,
                y: data.prices,
                type: 'scatter',
                mode: 'lines',
                name: 'Stock Price',
                line: { 
                    color: this.chartColors.primary, 
                    width: 3,
                    shape: 'spline'
                },
                fill: 'tonexty',
                fillcolor: 'rgba(102, 126, 234, 0.1)'
            }
        ];
        
        // Add moving averages with enhanced styling
        if (data.short_ma && data.short_ma.length > 0) {
            traces.push({
                x: data.timestamps,
                y: data.short_ma,
                type: 'scatter',
                mode: 'lines',
                name: 'Short MA (5)',
                line: { 
                    color: this.chartColors.danger, 
                    width: 2, 
                    dash: 'dot' 
                }
            });
        }
        
        if (data.long_ma && data.long_ma.length > 0) {
            traces.push({
                x: data.timestamps,
                y: data.long_ma,
                type: 'scatter',
                mode: 'lines',
                name: 'Long MA (20)',
                line: { 
                    color: this.chartColors.warning, 
                    width: 2, 
                    dash: 'dash' 
                }
            });
        }
        
        // Add buy/sell signals with enhanced markers
        if (data.signals) {
            const buySignals = [];
            const sellSignals = [];
            const buyPrices = [];
            const sellPrices = [];
            
            data.signals.forEach((signal, index) => {
                if (signal === 1) {
                    buySignals.push(data.timestamps[index]);
                    buyPrices.push(data.prices[index]);
                } else if (signal === -1) {
                    sellSignals.push(data.timestamps[index]);
                    sellPrices.push(data.prices[index]);
                }
            });
            
            if (buySignals.length > 0) {
                traces.push({
                    x: buySignals,
                    y: buyPrices,
                    type: 'scatter',
                    mode: 'markers',
                    name: 'Buy Signal',
                    marker: { 
                        symbol: 'triangle-up', 
                        size: 15, 
                        color: this.chartColors.success,
                        line: { width: 2, color: '#ffffff' }
                    }
                });
            }
            
            if (sellSignals.length > 0) {
                traces.push({
                    x: sellSignals,
                    y: sellPrices,
                    type: 'scatter',
                    mode: 'markers',
                    name: 'Sell Signal',
                    marker: { 
                        symbol: 'triangle-down', 
                        size: 15, 
                        color: this.chartColors.danger,
                        line: { width: 2, color: '#ffffff' }
                    }
                });
            }
        }
        
        const symbol = document.getElementById('stockSymbol').value;
        const layout = {
            title: {
                text: `${symbol} Real-Time Price & Trading Signals`,
                font: { size: 18, color: this.chartColors.dark },
                x: 0.5
            },
            xaxis: { 
                title: 'Time',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                zeroline: false,
                rangeslider: { visible: false }
            },
            yaxis: { 
                title: 'Price ($)',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                zeroline: false,
                autorange: true
            },
            height: 450,
            margin: { l: 60, r: 60, t: 80, b: 60 },
            plot_bgcolor: 'rgba(255,255,255,0.9)',
            paper_bgcolor: 'rgba(255,255,255,0.9)',
            hovermode: 'x unified',
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.8)',
                bordercolor: 'rgba(0,0,0,0.1)',
                borderwidth: 1
            },
            font: {
                family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
            },
            transition: {
                duration: 300,
                easing: 'cubic-in-out'
            }
        };
        
        Plotly.react('stockChart', traces, layout, {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false
        });
    }
    
    updatePortfolioChart(portfolioData) {
        if (!portfolioData || !portfolioData.timestamps || !portfolioData.values || portfolioData.timestamps.length === 0) {
            // Show empty state with helpful message
            const emptyTrace = {
                x: [],
                y: [],
                type: 'scatter',
                mode: 'lines',
                name: 'Portfolio Value',
                line: { 
                    color: this.chartColors.success, 
                    width: 4,
                    shape: 'spline'
                }
            };
            
            const layout = {
                title: {
                    text: 'Portfolio Performance vs Buy & Hold',
                    font: { size: 16, color: this.chartColors.dark },
                    x: 0.5
                },
                xaxis: { 
                    title: 'Time',
                    showgrid: true,
                    gridcolor: 'rgba(0,0,0,0.1)',
                    zeroline: false,
                    rangeslider: { visible: false }
                },
                yaxis: { 
                    title: 'Value ($)',
                    showgrid: true,
                    gridcolor: 'rgba(0,0,0,0.1)',
                    zeroline: false,
                    autorange: true
                },
                height: 350,
                margin: { l: 60, r: 60, t: 80, b: 60 },
                plot_bgcolor: 'rgba(255,255,255,0.9)',
                paper_bgcolor: 'rgba(255,255,255,0.9)',
                hovermode: 'x unified',
                showlegend: true,
                legend: {
                    x: 0.02,
                    y: 0.98,
                    bgcolor: 'rgba(255,255,255,0.8)',
                    bordercolor: 'rgba(0,0,0,0.1)',
                    borderwidth: 1
                },
                font: {
                    family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
                },
                annotations: [{
                    text: 'Portfolio performance will appear here once trading begins',
                    xref: 'paper',
                    yref: 'paper',
                    x: 0.5,
                    y: 0.5,
                    xanchor: 'center',
                    yanchor: 'middle',
                    showarrow: false,
                    font: {
                        size: 14,
                        color: '#7f8c8d'
                    },
                    bgcolor: 'rgba(255,255,255,0.8)',
                    bordercolor: 'rgba(0,0,0,0.1)',
                    borderwidth: 1,
                    pad: 10
                }]
            };
            
            Plotly.react('portfolioChart', [emptyTrace], layout, {
                responsive: true,
                displayModeBar: true,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
                displaylogo: false
            });
            return;
        }
        
        const trace = {
            x: portfolioData.timestamps,
            y: portfolioData.values,
            type: 'scatter',
            mode: 'lines',
            name: 'Portfolio Value',
            line: { 
                color: this.chartColors.success, 
                width: 4,
                shape: 'spline'
            },
            fill: 'tonexty',
            fillcolor: 'rgba(39, 174, 96, 0.1)'
        };
        
        // Calculate baseline values
        const baselineValues = this.calculateBaselineValues(portfolioData);
        const baselineTrace = {
            x: portfolioData.timestamps,
            y: baselineValues,
            type: 'scatter',
            mode: 'lines',
            name: 'Baseline (Buy & Hold)',
            line: { 
                color: this.chartColors.dark, 
                width: 2, 
                dash: 'dot',
                opacity: 0.7
            }
        };
        
        const symbol = document.getElementById('stockSymbol').value;
        const layout = {
            title: {
                text: `${symbol} Portfolio Performance`,
                font: { size: 16, color: this.chartColors.dark },
                x: 0.5
            },
            xaxis: { 
                title: 'Time',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                zeroline: false,
                rangeslider: { visible: false }
            },
            yaxis: { 
                title: 'Value ($)',
                showgrid: true,
                gridcolor: 'rgba(0,0,0,0.1)',
                zeroline: false,
                autorange: true
            },
            height: 350,
            margin: { l: 60, r: 60, t: 80, b: 60 },
            plot_bgcolor: 'rgba(255,255,255,0.9)',
            paper_bgcolor: 'rgba(255,255,255,0.9)',
            hovermode: 'x unified',
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.8)',
                bordercolor: 'rgba(0,0,0,0.1)',
                borderwidth: 1
            },
            font: {
                family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
            },
            transition: {
                duration: 300,
                easing: 'cubic-in-out'
            }
        };
        
        Plotly.react('portfolioChart', [trace, baselineTrace], layout, {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false
        });
    }
    
    calculateBaselineValues(portfolioData) {
        if (!portfolioData || !portfolioData.values || portfolioData.values.length === 0) return [];
        
        const initialCash = portfolioData.initial_cash || this.initialCash;
        const baselineValues = [];
        
        if (portfolioData.prices && portfolioData.prices.length > 0) {
            const firstPrice = portfolioData.prices[0];
            const sharesOwned = initialCash / firstPrice;
            
            portfolioData.prices.forEach(price => {
                const baselineValue = sharesOwned * price;
                baselineValues.push(baselineValue);
            });
        } else {
            // Fallback calculation
            const firstValue = portfolioData.values[0];
            const firstPrice = firstValue / initialCash;
            
            portfolioData.values.forEach(value => {
                const currentPrice = value / initialCash;
                const sharesOwned = initialCash / firstPrice;
                const baselineValue = sharesOwned * currentPrice;
                baselineValues.push(baselineValue);
            });
        }
        
        return baselineValues;
    }
    
    updateTradesTable(trades) {
        const tableBody = document.getElementById('tradesTableBody');
        tableBody.innerHTML = '';
        
        if (!trades || trades.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No trades yet</td></tr>';
            return;
        }
        
        trades.slice(-10).reverse().forEach(trade => {
            const row = document.createElement('tr');
            row.className = `trade-row trade-${trade.type}`;
            
            const time = new Date(trade.time).toLocaleString();
            const typeClass = trade.type === 'buy' ? 'badge-success' : 'badge-danger';
            
            row.innerHTML = `
                <td><i class="fas fa-clock"></i> ${time}</td>
                <td><strong>${trade.symbol}</strong></td>
                <td><span class="badge ${typeClass}">${trade.type.toUpperCase()}</span></td>
                <td><strong>$${trade.price.toFixed(2)}</strong></td>
                <td>${trade.quantity}</td>
                <td><strong>$${(trade.price * trade.quantity).toFixed(2)}</strong></td>
            `;
            
            tableBody.appendChild(row);
        });
    }
    
    updateCurrentPrice(data) {
        const priceElement = document.getElementById('currentPrice');
        if (priceElement && data.prices && data.prices.length > 0) {
            const currentPrice = data.prices[data.prices.length - 1];
            priceElement.textContent = `$${currentPrice.toFixed(2)}`;
            
            // Add price change indicator
            if (data.prices.length > 1) {
                const previousPrice = data.prices[data.prices.length - 2];
                const change = currentPrice - previousPrice;
                const changePercent = (change / previousPrice) * 100;
                
                const changeElement = document.getElementById('priceChange');
                if (changeElement) {
                    const changeClass = change >= 0 ? 'text-success' : 'text-danger';
                    const changeIcon = change >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';
                    changeElement.innerHTML = `
                        <span class="${changeClass}">
                            <i class="fas ${changeIcon}"></i>
                            ${change >= 0 ? '+' : ''}$${change.toFixed(2)} (${changePercent.toFixed(2)}%)
                        </span>
                    `;
                }
            }
        }
    }
    
    updatePortfolioStats(currentValue) {
        const valueElement = document.getElementById('portfolioValue');
        if (valueElement) {
            valueElement.textContent = `$${currentValue.toFixed(2)}`;
            
            // Calculate and display return
            const returnAmount = currentValue - this.initialCash;
            const returnPercent = (returnAmount / this.initialCash) * 100;
            
            const returnElement = document.getElementById('portfolioReturn');
            if (returnElement) {
                const returnClass = returnAmount >= 0 ? 'text-success' : 'text-danger';
                const returnIcon = returnAmount >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';
                returnElement.innerHTML = `
                    <span class="${returnClass}">
                        <i class="fas ${returnIcon}"></i>
                        ${returnAmount >= 0 ? '+' : ''}$${returnAmount.toFixed(2)} (${returnPercent.toFixed(2)}%)
                    </span>
                `;
            }
        }
    }
    
    async updateStats(trades) {
        if (!trades) return;
        
        try {
            const response = await fetch('/api/performance-metrics');
            if (response.ok) {
                const metrics = await response.json();
                
                document.getElementById('totalTrades').textContent = metrics.total_trades;
                document.getElementById('winRate').textContent = `${metrics.win_rate.toFixed(1)}%`;
                document.getElementById('totalReturn').textContent = `$${metrics.total_return.toFixed(2)}`;
                document.getElementById('returnPercentage').textContent = `${metrics.total_return_percentage.toFixed(2)}%`;
                document.getElementById('maxDrawdown').textContent = `${metrics.max_drawdown.toFixed(2)}%`;
                document.getElementById('currentValue').textContent = `$${metrics.current_value.toFixed(2)}`;
                
                // Color code the return percentage
                const returnElement = document.getElementById('returnPercentage');
                if (metrics.is_profitable) {
                    returnElement.style.color = this.chartColors.success;
                } else {
                    returnElement.style.color = this.chartColors.danger;
                }
                
                document.getElementById('statsRow').style.display = 'flex';
            }
        } catch (error) {
            console.error('Error fetching performance metrics:', error);
        }
    }
    
    updateRealTimeIndicator(elementId, message = 'Live Updates') {
        const element = document.getElementById(elementId);
        if (element) {
            const timestamp = new Date().toLocaleTimeString();
            element.innerHTML = `
                <span class="real-time-indicator"></span>
                <span>${message} - Last: ${timestamp}</span>
            `;
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
        if (dateInput) {
            dateInput.disabled = !enabled;
            dateInput.required = enabled;
            if (!enabled) {
                dateInput.value = '';
            }
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
    
    resetCharts() {
        // Reset charts to empty state with helpful messages
        this.updateStockChart({ timestamps: [], prices: [], short_ma: [], long_ma: [], signals: [] });
        this.updatePortfolioChart({ timestamps: [], values: [], prices: [], initial_cash: this.initialCash });
        
        // Update status indicators
        this.updateRealTimeIndicator('stockUpdateStatus', 'Charts cleared');
        this.updateRealTimeIndicator('portfolioUpdateStatus', 'Charts cleared');
    }
    
    resizeCharts() {
        // Resize charts on window resize
        if (this.charts.stockChart) {
            Plotly.Plots.resize('stockChart');
        }
        if (this.charts.portfolioChart) {
            Plotly.Plots.resize('portfolioChart');
        }
    }
    
    showAlert(message, type) {
        const alertContainer = document.getElementById('alertContainer');
        const alertId = 'alert-' + Date.now();
        
        const alertHtml = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
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