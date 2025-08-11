# Comprehensive Prompt for Automatic Trading Platform

### Project Overview
Create an **Automatic Trading Platform** that integrates with Charles Schwab's trading API to execute automated trades based on market analysis, risk management, and predefined strategies. The platform should be designed for retail investors who want systematic, rule-based trading with strict risk controls.

### Core Requirements

#### 1. **Trading Strategy & Risk Management**
- **Market Cap Selection**: Implement algorithms to identify and categorize stocks by market capitalization:
  - **Large Cap**: $10B+ (stable, dividend-paying companies)
  - **Mid Cap**: $2B-$10B (growth potential with moderate risk)
  - **Small Cap**: $300M-$2B (high growth, higher risk)
  - **Micro Cap**: <$300M (speculative, highest risk)
- **Budget Allocation**: Dynamic portfolio allocation based on:
  - Total available capital
  - Risk tolerance (Conservative: 70% Large Cap, 20% Mid Cap, 10% Small Cap)
  - Market conditions and volatility
- **Risk Assessment**: 
  - Maximum position size: 5% of total portfolio per stock
  - Sector diversification: Max 25% in any single sector
  - Volatility-based position sizing
- **Stop Loss Implementation**:
  - **Strict Stop Loss**: 2-5% below entry price (configurable)
  - **Trailing Stop Loss**: Dynamic adjustment as position moves in profit
  - **Time-based Stop Loss**: Exit positions after 5-7 days if no profit target reached

#### 2. **Charles Schwab API Integration**
- **Authentication**: Use `schwabdev` package for secure API access
- **Account Management**: 
  - Real-time account balance and positions
  - Available buying power calculation
  - Margin requirements monitoring
- **Trading Operations**:
  - Market orders, limit orders, stop orders
  - Order modification and cancellation
  - Real-time order status tracking
- **Market Data**: 
  - Real-time stock quotes and charts
  - Historical price data for analysis
  - Volume and volatility metrics

#### 3. **Weekly Planning System**
- **Sunday Analysis**: Weekly market analysis and strategy planning
- **Monday Execution**: Position entry based on weekly plan
- **Mid-week Monitoring**: Performance tracking and adjustment
- **Friday Review**: Position evaluation and weekend preparation
- **Weekend Research**: Market research and next week's strategy

#### 4. **Technical Implementation**
- **Python 3.11+**: Use most basic Python code structure
- **Core Libraries**:
  - `schwabdev`: Charles Schwab API wrapper
  - `pandas`: Data manipulation and analysis
  - `numpy`: Mathematical calculations
  - `requests`: HTTP requests for additional data
  - `datetime`: Time-based operations
  - `json`: Configuration and data handling
- **Architecture**: Simple, modular design with clear separation of concerns
- **Configuration**: JSON-based settings for easy modification
- **Logging**: Comprehensive logging for audit trails and debugging

#### 5. **Key Features**
- **Portfolio Dashboard**: Real-time view of positions, P&L, and risk metrics
- **Strategy Backtesting**: Historical performance analysis
- **Alert System**: Email/SMS notifications for critical events
- **Performance Reporting**: Weekly/monthly performance summaries
- **Risk Monitoring**: Real-time risk exposure calculations

#### 6. **Safety & Compliance**
- **Paper Trading Mode**: Test strategies without real money
- **Emergency Stop**: Immediate halt to all trading activities
- **Position Limits**: Maximum exposure controls
- **Compliance Checks**: Ensure adherence to trading rules
- **Audit Trail**: Complete record of all decisions and actions

#### 7. **User Experience**
- **Simple Interface**: Command-line or basic web interface
- **Configuration Files**: Easy-to-edit settings
- **Documentation**: Clear setup and usage instructions
- **Error Handling**: Graceful failure with clear error messages

### Technical Specifications

#### File Structure
```
AutomateTrade/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── schwab_client.py
│   ├── trading_strategy.py
│   ├── risk_manager.py
│   ├── portfolio_manager.py
│   ├── market_analyzer.py
│   └── utils.py
├── config/
│   ├── trading_config.json
│   ├── risk_config.json
│   └── schwab_config.json
├── data/
│   ├── historical/
│   ├── logs/
│   └── reports/
├── tests/
├── requirements.txt
├── README.md
└── .env
```

#### Core Classes
1. **SchwabClient**: API wrapper and authentication
2. **TradingStrategy**: Strategy implementation and execution
3. **RiskManager**: Risk assessment and position sizing
4. **PortfolioManager**: Portfolio tracking and rebalancing
5. **MarketAnalyzer**: Market data analysis and signals
6. **OrderManager**: Order execution and management

#### Configuration Examples
```json
{
  "trading": {
    "max_position_size": 0.05,
    "max_sector_exposure": 0.25,
    "stop_loss_percentage": 0.03,
    "max_holding_days": 7
  },
  "risk": {
    "conservative": {"large_cap": 0.70, "mid_cap": 0.20, "small_cap": 0.10},
    "moderate": {"large_cap": 0.50, "mid_cap": 0.30, "small_cap": 0.20},
    "aggressive": {"large_cap": 0.30, "mid_cap": 0.40, "small_cap": 0.30}
  }
}
```

### Development Phases

#### Phase 1: Foundation
- Set up project structure and dependencies
- Implement Charles Schwab API integration
- Create basic portfolio management

#### Phase 2: Core Trading Logic
- Implement market cap selection algorithms
- Add risk management and position sizing
- Create stop loss mechanisms

#### Phase 3: Strategy & Planning
- Develop weekly planning system
- Implement trading strategies
- Add backtesting capabilities

#### Phase 4: Monitoring & Safety
- Real-time monitoring and alerts
- Performance reporting
- Safety mechanisms and compliance

#### Phase 5: Optimization
- Performance tuning
- Additional strategies
- User interface improvements

### Success Criteria
- Successfully execute trades through Charles Schwab API
- Maintain strict risk controls and stop losses
- Generate consistent weekly trading plans
- Provide clear performance metrics and reporting
- Handle errors gracefully with comprehensive logging

### Risk Considerations
- **Market Risk**: Implement strict position limits and diversification
- **Technical Risk**: Robust error handling and fallback mechanisms
- **Regulatory Risk**: Ensure compliance with trading regulations
- **Operational Risk**: Comprehensive testing and monitoring

This platform should provide a systematic, disciplined approach to trading while maintaining strict risk controls and leveraging the reliability of Charles Schwab's infrastructure through the `schwabdev` package.
