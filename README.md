# AutomateTrade - Automatic Trading Platform

An intelligent, rule-based automated trading platform that integrates with Charles Schwab's trading API to execute systematic trades with strict risk management.

## 🚀 Features

- **Automated Trading**: Execute trades based on predefined strategies and market analysis
- **Risk Management**: Strict stop-loss, position sizing, and portfolio diversification
- **Market Cap Selection**: Intelligent allocation across large, mid, and small-cap stocks
- **Weekly Planning**: Systematic approach with weekly analysis and execution
- **Real-time Monitoring**: Live portfolio tracking and performance metrics
- **Charles Schwab Integration**: Secure API access through schwabdev package

## 📋 Requirements

- Python 3.11+
- Charles Schwab trading account
- API credentials (username, password, 2FA)
- Internet connection for real-time data

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AutomateTrade
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Charles Schwab credentials
   ```

## ⚙️ Configuration

### Environment Variables (.env)
```bash
SCHWAB_USERNAME=your_username
SCHWAB_PASSWORD=your_password
SCHWAB_2FA_SECRET=your_2fa_secret
PAPER_TRADING=true
LOG_LEVEL=INFO
```

### Trading Configuration (config/trading_config.json)
```json
{
  "max_position_size": 0.05,
  "max_sector_exposure": 0.25,
  "stop_loss_percentage": 0.03,
  "max_holding_days": 7,
  "risk_tolerance": "moderate"
}
```

## 🚀 Usage

### Basic Usage
```python
from src.main import TradingPlatform

# Initialize platform
platform = TradingPlatform()

# Start automated trading
platform.start()
```

### Command Line Interface
```bash
# Start the platform
python src/main.py

# Run in paper trading mode
python src/main.py --paper-trading

# Run with custom config
python src/main.py --config custom_config.json
```

## 📊 Trading Strategies

### Market Cap Allocation
- **Conservative**: 70% Large Cap, 20% Mid Cap, 10% Small Cap
- **Moderate**: 50% Large Cap, 30% Mid Cap, 20% Small Cap  
- **Aggressive**: 30% Large Cap, 40% Mid Cap, 30% Small Cap

### Risk Management
- Maximum 5% portfolio per position
- Sector diversification (max 25% per sector)
- Strict stop-loss (2-5% below entry)
- Time-based exits (5-7 days max holding)

## 🔒 Safety Features

- **Paper Trading Mode**: Test strategies without real money
- **Emergency Stop**: Immediate halt to all trading
- **Position Limits**: Strict exposure controls
- **Compliance Checks**: Regulatory adherence
- **Audit Trail**: Complete decision logging

## 📁 Project Structure

```
AutomateTrade/
├── src/                    # Source code
│   ├── main.py            # Main application entry point
│   ├── schwab_client.py   # Charles Schwab API wrapper
│   ├── trading_strategy.py # Trading strategy implementation
│   ├── risk_manager.py    # Risk management and position sizing
│   ├── portfolio_manager.py # Portfolio tracking and management
│   ├── market_analyzer.py # Market data analysis
│   └── utils.py           # Utility functions
├── config/                 # Configuration files
├── data/                   # Data storage
├── tests/                  # Test suite
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=src tests/
```

## 📈 Performance Monitoring

The platform provides comprehensive performance metrics:
- Real-time P&L tracking
- Risk exposure analysis
- Strategy performance reports
- Portfolio rebalancing alerts

## ⚠️ Disclaimer

**This software is for educational and informational purposes only. Trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Always consult with a qualified financial advisor before making investment decisions.**

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the logs for debugging information

## 🔄 Updates

The platform automatically checks for updates and can be configured to:
- Update trading strategies
- Adjust risk parameters
- Modify position allocations
- Update market data sources

---

**Built with ❤️ for systematic trading**
