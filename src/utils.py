"""
Utility functions for the AutomateTrade platform.
Common helper functions used across the application.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np


def setup_logging(log_level: str = "INFO", log_file: str = "data/logs/trading.log") -> logging.Logger:
    """Set up logging configuration for the application."""
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized with level: {log_level}")
    return logger


def load_config(config_file: str) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {config_file}")


def save_config(config: Dict[str, Any], config_file: str) -> None:
    """Save configuration to JSON file."""
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        raise Exception(f"Failed to save configuration: {e}")


def calculate_market_cap(price: float, shares_outstanding: int) -> float:
    """Calculate market capitalization."""
    return price * shares_outstanding


def categorize_market_cap(market_cap: float) -> str:
    """Categorize stock by market capitalization."""
    if market_cap >= 10_000_000_000:  # $10B+
        return "large_cap"
    elif market_cap >= 2_000_000_000:  # $2B-$10B
        return "mid_cap"
    elif market_cap >= 300_000_000:    # $300M-$2B
        return "small_cap"
    else:                               # <$300M
        return "micro_cap"


def calculate_position_size(portfolio_value: float, stock_price: float, 
                           max_position_percentage: float = 0.05) -> int:
    """Calculate the number of shares to buy based on position size limits."""
    max_position_value = portfolio_value * max_position_percentage
    shares = int(max_position_value / stock_price)
    return max(shares, 1)  # Minimum 1 share


def calculate_stop_loss_price(entry_price: float, stop_loss_percentage: float) -> float:
    """Calculate stop loss price."""
    return entry_price * (1 - stop_loss_percentage)


def calculate_trailing_stop_price(current_price: float, highest_price: float, 
                                trailing_percentage: float) -> float:
    """Calculate trailing stop loss price."""
    return highest_price * (1 - trailing_percentage)


def is_market_open() -> bool:
    """Check if the market is currently open."""
    now = datetime.now()
    
    # Check if it's a weekday
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False
    
    # Check if it's within market hours (9:30 AM - 4:00 PM ET)
    # Note: This is a simplified check. In production, consider timezone handling
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    
    return market_open <= now <= market_close


def format_currency(amount: float) -> str:
    """Format amount as currency string."""
    return f"${amount:,.2f}"


def format_percentage(value: float) -> str:
    """Format value as percentage string."""
    return f"{value * 100:.2f}%"


def calculate_volatility(prices: List[float], lookback_days: int = 30) -> float:
    """Calculate volatility (standard deviation of returns)."""
    if len(prices) < 2:
        return 0.0
    
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] != 0:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    
    if not returns:
        return 0.0
    
    return np.std(returns) * np.sqrt(252)  # Annualized volatility


def calculate_correlation(prices1: List[float], prices2: List[float]) -> float:
    """Calculate correlation between two price series."""
    if len(prices1) != len(prices2) or len(prices1) < 2:
        return 0.0
    
    returns1 = []
    returns2 = []
    
    for i in range(1, len(prices1)):
        if prices1[i-1] != 0 and prices2[i-1] != 0:
            returns1.append((prices1[i] - prices1[i-1]) / prices1[i-1])
            returns2.append((prices2[i] - prices2[i-1]) / prices2[i-1])
    
    if len(returns1) < 2:
        return 0.0
    
    return np.corrcoef(returns1, returns2)[0, 1]


def validate_ticker(ticker: str) -> bool:
    """Validate stock ticker format."""
    if not ticker or len(ticker) > 10:
        return False
    
    # Basic validation - ticker should be alphanumeric
    return ticker.replace('.', '').replace('-', '').isalnum()


def get_next_trading_day(current_date: datetime = None) -> datetime:
    """Get the next trading day."""
    if current_date is None:
        current_date = datetime.now()
    
    next_day = current_date + timedelta(days=1)
    
    # Skip weekends
    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)
    
    return next_day


def calculate_portfolio_metrics(positions: List[Dict[str, Any]], 
                              initial_value: float) -> Dict[str, Any]:
    """Calculate portfolio performance metrics."""
    if not positions:
        return {
            "total_value": 0,
            "total_pnl": 0,
            "total_return": 0,
            "num_positions": 0
        }
    
    total_value = sum(pos.get('current_value', 0) for pos in positions)
    total_cost = sum(pos.get('cost_basis', 0) for pos in positions)
    total_pnl = total_value - total_cost
    total_return = (total_pnl / initial_value) if initial_value > 0 else 0
    
    return {
        "total_value": total_value,
        "total_pnl": total_pnl,
        "total_return": total_return,
        "num_positions": len(positions),
        "winning_positions": len([p for p in positions if p.get('pnl', 0) > 0]),
        "losing_positions": len([p for p in positions if p.get('pnl', 0) < 0])
    }


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def round_to_precision(value: float, precision: int = 2) -> float:
    """Round value to specified decimal precision."""
    return round(value, precision)


def log_trade_action(logger: logging.Logger, action: str, details: Dict[str, Any]) -> None:
    """Log trading actions with structured details."""
    logger.info(f"TRADE_ACTION: {action} - {json.dumps(details, default=str)}")


def create_backup_filename(original_filename: str) -> str:
    """Create a backup filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(original_filename)
    return f"{name}_backup_{timestamp}{ext}"
