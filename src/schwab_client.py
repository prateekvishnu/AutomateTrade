"""
Charles Schwab API Client Wrapper

This module provides a clean interface to the Charles Schwab trading API
using the schwabdev package. It includes methods for account management,
market data, order management, and real-time streaming.

IMPORTANT: Add this file to your .gitignore to avoid leaking credentials
if you are pushing to GitHub!

Learn about gitignore: https://git-scm.com/docs/gitignore
"""

import datetime
import json
import logging
import os
import time
from typing import Dict, List, Optional, Any, Union

from dotenv import load_dotenv
import schwabdev


class SchwabClient:
    """
    A wrapper class for the Charles Schwab API client that provides
    a clean interface for trading operations.
    """
    
    def __init__(self, app_key: Optional[str] = None, 
                 app_secret: Optional[str] = None, 
                 callback_url: Optional[str] = None):
        """
        Initialize the Schwab client.
        
        Args:
            app_key: Schwab app key (32 characters)
            app_secret: Schwab app secret (16 characters)
            callback_url: OAuth callback URL
        """
        # Load environment variables if not provided
        load_dotenv()
        
        self.app_key = app_key or os.getenv('app_key')
        self.app_secret = app_secret or os.getenv('app_secret')
        self.callback_url = callback_url or os.getenv('callback_url')
        
        # Validate credentials
        self._validate_credentials()
        
        # Create client
        self.client = schwabdev.Client(self.app_key, self.app_secret, self.callback_url)
        self.streamer = self.client.stream
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Schwab client initialized successfully")
    
    def _validate_credentials(self):
        """Validate that required credentials are present and correct length."""
        if not self.app_key or len(self.app_key) != 32:
            raise ValueError("App key must be exactly 32 characters long")
        
        if not self.app_secret or len(self.app_secret) != 16:
            raise ValueError("App secret must be exactly 16 characters long")
        
        if not self.callback_url:
            raise ValueError("Callback URL is required")
    
    def get_linked_accounts(self) -> List[Dict[str, Any]]:
        """
        Get all linked accounts.
        
        Returns:
            List of linked account information
        """
        try:
            response = self.client.account_linked()
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get linked accounts: {response.status_code}")
                return []
        except Exception as e:
            self.logger.error(f"Error getting linked accounts: {e}")
            return []
    
    def get_account_details(self, account_hash: str, 
                          fields: Optional[str] = None) -> Dict[str, Any]:
        """
        Get details for a specific account.
        
        Args:
            account_hash: Account hash identifier
            fields: Specific fields to retrieve (e.g., "positions")
            
        Returns:
            Account details dictionary
        """
        try:
            response = self.client.account_details(account_hash, fields=fields)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get account details: {response.status_code}")
                return {}
        except Exception as e:
            self.logger.error(f"Error getting account details: {e}")
            return {}
    
    def get_account_positions(self, account_hash: str) -> Dict[str, Any]:
        """
        Get current positions for an account.
        
        Args:
            account_hash: Account hash identifier
            
        Returns:
            Positions information
        """
        return self.get_account_details(account_hash, fields="positions")
    
    def get_orders(self, account_hash: str, 
                   start_date: datetime.datetime,
                   end_date: datetime.datetime) -> List[Dict[str, Any]]:
        """
        Get orders for a specific account within a date range.
        
        Args:
            account_hash: Account hash identifier
            start_date: Start date for order search
            end_date: End date for order search
            
        Returns:
            List of orders
        """
        try:
            response = self.client.account_orders(account_hash, start_date, end_date)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get orders: {response.status_code}")
                return []
        except Exception as e:
            self.logger.error(f"Error getting orders: {e}")
            return []
    
    def place_order(self, account_hash: str, order: Dict[str, Any]) -> Optional[str]:
        """
        Place an order.
        
        Args:
            account_hash: Account hash identifier
            order: Order dictionary with order details
            
        Returns:
            Order ID if successful, None otherwise
        """
        try:
            response = self.client.order_place(account_hash, order)
            if response.status_code in [200, 201]:
                order_id = response.headers.get('location', '/').split('/')[-1]
                self.logger.info(f"Order placed successfully: {order_id}")
                return order_id
            else:
                self.logger.error(f"Failed to place order: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            return None
    
    def cancel_order(self, account_hash: str, order_id: str) -> bool:
        """
        Cancel an existing order.
        
        Args:
            account_hash: Account hash identifier
            order_id: Order ID to cancel
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.order_cancel(account_hash, order_id)
            if response.status_code == 200:
                self.logger.info(f"Order cancelled successfully: {order_id}")
                return True
            else:
                self.logger.error(f"Failed to cancel order: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Error cancelling order: {e}")
            return False
    
    def get_order_details(self, account_hash: str, order_id: str) -> Dict[str, Any]:
        """
        Get details for a specific order.
        
        Args:
            account_hash: Account hash identifier
            order_id: Order ID
            
        Returns:
            Order details dictionary
        """
        try:
            response = self.client.order_details(account_hash, order_id)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get order details: {response.status_code}")
                return {}
        except Exception as e:
            self.logger.error(f"Error getting order details: {e}")
            return {}
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get quote for a single symbol.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL")
            
        Returns:
            Quote information dictionary
        """
        try:
            response = self.client.quote(symbol)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get quote for {symbol}: {response.status_code}")
                return {}
        except Exception as e:
            self.logger.error(f"Error getting quote for {symbol}: {e}")
            return {}
    
    def get_quotes(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """
        Get quotes for multiple symbols.
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            List of quote information dictionaries
        """
        try:
            response = self.client.quotes(symbols)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get quotes: {response.status_code}")
                return []
        except Exception as e:
            self.logger.error(f"Error getting quotes: {e}")
            return []
    
    def get_price_history(self, symbol: str, period: str) -> Dict[str, Any]:
        """
        Get price history for a symbol.
        
        Args:
            symbol: Stock symbol
            period: Time period ("day", "month", "year", "ytd")
            
        Returns:
            Price history data
        """
        try:
            response = self.client.price_history(symbol, period)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get price history: {response.status_code}")
                return {}
        except Exception as e:
            self.logger.error(f"Error getting price history: {e}")
            return {}
    
    def get_option_chain(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """
        Get option chain for a symbol.
        
        Args:
            symbol: Stock symbol
            **kwargs: Additional parameters (contractType, range, etc.)
            
        Returns:
            Option chain data
        """
        try:
            response = self.client.option_chains(symbol, **kwargs)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get option chain: {response.status_code}")
                return {}
        except Exception as e:
            self.logger.error(f"Error getting option chain: {e}")
            return {}
    
    def get_market_hours(self, markets: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Get market hours for specified markets.
        
        Args:
            markets: Market type(s) ("equity", "option", etc.)
            
        Returns:
            Market hours information
        """
        try:
            if isinstance(markets, list):
                markets = ",".join(markets)
            
            response = self.client.market_hours(markets)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get market hours: {response.status_code}")
                return {}
        except Exception as e:
            self.logger.error(f"Error getting market hours: {e}")
            return {}
    
    def start_streaming(self, handler_func=None):
        """
        Start the streaming service.
        
        Args:
            handler_func: Custom message handler function
        """
        try:
            if handler_func:
                self.streamer.start(handler_func)
            else:
                self.streamer.start()
            self.logger.info("Streaming started successfully")
        except Exception as e:
            self.logger.error(f"Error starting streaming: {e}")
    
    def stop_streaming(self, clear_subscriptions: bool = True):
        """
        Stop the streaming service.
        
        Args:
            clear_subscriptions: Whether to clear current subscriptions
        """
        try:
            self.streamer.stop(clear_subscriptions=clear_subscriptions)
            self.logger.info("Streaming stopped successfully")
        except Exception as e:
            self.logger.error(f"Error stopping streaming: {e}")
    
    def subscribe_equities(self, symbols: List[str], fields: List[int]):
        """
        Subscribe to equity quotes.
        
        Args:
            symbols: List of stock symbols
            fields: List of field numbers to subscribe to
        """
        try:
            symbols_str = ",".join(symbols)
            fields_str = ",".join(map(str, fields))
            self.streamer.send(
                self.streamer.level_one_equities(symbols_str, fields_str)
            )
            self.logger.info(f"Subscribed to equity quotes for {symbols}")
        except Exception as e:
            self.logger.error(f"Error subscribing to equities: {e}")
    
    def subscribe_options(self, option_symbols: List[str], fields: List[int]):
        """
        Subscribe to option quotes.
        
        Args:
            option_symbols: List of option symbols
            fields: List of field numbers to subscribe to
        """
        try:
            for symbol in option_symbols:
                fields_str = ",".join(map(str, fields))
                self.streamer.send(
                    self.streamer.level_one_options(symbol, fields_str)
                )
            self.logger.info(f"Subscribed to option quotes for {option_symbols}")
        except Exception as e:
            self.logger.error(f"Error subscribing to options: {e}")
    
    def create_market_order(self, symbol: str, quantity: int, 
                           instruction: str = "BUY") -> Dict[str, Any]:
        """
        Create a market order.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            instruction: "BUY" or "SELL"
            
        Returns:
            Order dictionary
        """
        return {
            "orderType": "MARKET",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": instruction,
                    "quantity": quantity,
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY"
                    }
                }
            ]
        }
    
    def create_limit_order(self, symbol: str, quantity: int, 
                          price: float, instruction: str = "BUY") -> Dict[str, Any]:
        """
        Create a limit order.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            price: Limit price
            instruction: "BUY" or "SELL"
            
        Returns:
            Order dictionary
        """
        return {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "price": str(price),
            "orderLegCollection": [
                {
                    "instruction": instruction,
                    "quantity": quantity,
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY"
                    }
                }
            ]
        }
    
    def get_transactions(self, account_hash: str, 
                        start_date: datetime.datetime,
                        end_date: datetime.datetime,
                        transaction_type: str = "TRADE") -> List[Dict[str, Any]]:
        """
        Get transactions for an account.
        
        Args:
            account_hash: Account hash identifier
            start_date: Start date for transaction search
            end_date: End date for transaction search
            transaction_type: Type of transactions to retrieve
            
        Returns:
            List of transactions
        """
        try:
            response = self.client.transactions(
                account_hash, start_date, end_date, transaction_type
            )
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get transactions: {response.status_code}")
                return []
        except Exception as e:
            self.logger.error(f"Error getting transactions: {e}")
            return []
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """
        Get user preferences for the account.
        
        Returns:
            User preferences dictionary
        """
        try:
            response = self.client.preferences()
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get preferences: {response.status_code}")
                return {}
        except Exception as e:
            self.logger.error(f"Error getting preferences: {e}")
            return {}


def main():
    """
    Example usage of the SchwabClient class.
    This demonstrates the basic functionality of the client.
    """
    print("Welcome to Schwab API Client!")
    print("Documentation: https://tylerebowers.github.io/Schwabdev/")
    
    try:
        # Initialize client
        client = SchwabClient()
        
        # Get linked accounts
        print("\nGetting linked accounts...")
        linked_accounts = client.get_linked_accounts()
        if linked_accounts:
            print(f"Found {len(linked_accounts)} linked account(s)")
            account_hash = linked_accounts[0].get('hashValue')
            print(f"Using account hash: {account_hash}")
            
            # Get account details
            print("\nGetting account details...")
            account_details = client.get_account_details(account_hash)
            if account_details:
                print("Account details retrieved successfully")
            
            # Get a quote
            print("\nGetting quote for AAPL...")
            quote = client.get_quote("AAPL")
            if quote:
                print(f"AAPL Quote: {quote}")
            
            # Get market hours
            print("\nGetting market hours...")
            market_hours = client.get_market_hours(["equity", "option"])
            if market_hours:
                print("Market hours retrieved successfully")
                
        else:
            print("No linked accounts found")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your .env file and credentials")


if __name__ == "__main__":
    main()
