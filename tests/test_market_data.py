"""
Test module for market data functionality.

This module tests the ability to pull market data from Charles Schwab API
including quotes, price history, market hours, and option chains.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os
import sys
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from schwab_client import SchwabClient


class TestMarketData(unittest.TestCase):
    """Test cases for market data functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'app_key': '12345678901234567890123456789012',
            'app_secret': '1234567890123456',
            'callback_url': 'https://example.com/callback'
        })
        self.env_patcher.start()
        
        # Mock schwabdev client
        self.mock_client = Mock()
        self.mock_response = Mock()
        self.mock_response.status_code = 200
        
        # Create SchwabClient instance with mocked dependencies
        with patch('schwabdev.Client') as mock_client_class:
            mock_client_class.return_value = self.mock_client
            self.client = SchwabClient()
    
    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()
    
    def test_get_quote_success(self):
        """Test successful quote retrieval."""
        # Mock response data
        mock_quote_data = {
            "symbol": "AAPL",
            "bid": 150.50,
            "ask": 150.75,
            "last": 150.60,
            "volume": 1000000,
            "change": 0.50,
            "changePercent": 0.33
        }
        self.mock_response.json.return_value = mock_quote_data
        self.mock_client.quote.return_value = self.mock_response
        
        # Test quote retrieval
        result = self.client.get_quote("AAPL")
        
        # Verify results
        self.assertEqual(result, mock_quote_data)
        self.mock_client.quote.assert_called_once_with("AAPL")
    
    def test_get_quote_failure(self):
        """Test quote retrieval failure."""
        # Mock failed response
        self.mock_response.status_code = 404
        self.mock_response.json.return_value = {"error": "Symbol not found"}
        self.mock_client.quote.return_value = self.mock_response
        
        # Test quote retrieval
        result = self.client.get_quote("INVALID")
        
        # Verify results
        self.assertEqual(result, {})
    
    def test_get_quotes_multiple_symbols(self):
        """Test retrieving quotes for multiple symbols."""
        # Mock response data
        mock_quotes_data = [
            {
                "symbol": "AAPL",
                "bid": 150.50,
                "ask": 150.75,
                "last": 150.60
            },
            {
                "symbol": "GOOGL",
                "bid": 2800.00,
                "ask": 2801.00,
                "last": 2800.50
            }
        ]
        self.mock_response.json.return_value = mock_quotes_data
        self.mock_client.quotes.return_value = self.mock_response
        
        # Test multiple quotes retrieval
        symbols = ["AAPL", "GOOGL"]
        result = self.client.get_quotes(symbols)
        
        # Verify results
        self.assertEqual(result, mock_quotes_data)
        self.mock_client.quotes.assert_called_once_with(symbols)
    
    def test_get_price_history(self):
        """Test price history retrieval."""
        # Mock response data
        mock_history_data = {
            "symbol": "AAPL",
            "candles": [
                {
                    "datetime": "2024-01-01T09:30:00",
                    "open": 150.00,
                    "high": 151.00,
                    "low": 149.50,
                    "close": 150.50,
                    "volume": 1000000
                }
            ]
        }
        self.mock_response.json.return_value = mock_history_data
        self.mock_client.price_history.return_value = self.mock_response
        
        # Test price history retrieval
        result = self.client.get_price_history("AAPL", "day")
        
        # Verify results
        self.assertEqual(result, mock_history_data)
        self.mock_client.price_history.assert_called_once_with("AAPL", "day")
    
    def test_get_market_hours(self):
        """Test market hours retrieval."""
        # Mock response data
        mock_hours_data = {
            "equity": {
                "isOpen": True,
                "open": "09:30",
                "close": "16:00"
            },
            "option": {
                "isOpen": True,
                "open": "09:30",
                "close": "16:00"
            }
        }
        self.mock_response.json.return_value = mock_hours_data
        self.mock_client.market_hours.return_value = self.mock_response
        
        # Test market hours retrieval
        markets = ["equity", "option"]
        result = self.client.get_market_hours(markets)
        
        # Verify results
        self.assertEqual(result, mock_hours_data)
        self.mock_client.market_hours.assert_called_once_with("equity,option")
    
    def test_get_option_chain(self):
        """Test option chain retrieval."""
        # Mock response data
        mock_option_data = {
            "symbol": "AAPL",
            "putExpDateMap": {},
            "callExpDateMap": {}
        }
        self.mock_response.json.return_value = mock_option_data
        self.mock_client.option_chains.return_value = self.mock_response
        
        # Test option chain retrieval
        result = self.client.get_option_chain("AAPL", contractType="ALL")
        
        # Verify results
        self.assertEqual(result, mock_option_data)
        self.mock_client.option_chains.assert_called_once_with("AAPL", contractType="ALL")
    
    def test_get_quote_exception_handling(self):
        """Test exception handling in quote retrieval."""
        # Mock exception
        self.mock_client.quote.side_effect = Exception("API Error")
        
        # Test quote retrieval with exception
        result = self.client.get_quote("AAPL")
        
        # Verify results
        self.assertEqual(result, {})
    
    def test_get_quotes_exception_handling(self):
        """Test exception handling in multiple quotes retrieval."""
        # Mock exception
        self.mock_client.quotes.side_effect = Exception("API Error")
        
        # Test quotes retrieval with exception
        symbols = ["AAPL", "GOOGL"]
        result = self.client.get_quotes(symbols)
        
        # Verify results
        self.assertEqual(result, [])
    
    def test_get_price_history_exception_handling(self):
        """Test exception handling in price history retrieval."""
        # Mock exception
        self.mock_client.price_history.side_effect = Exception("API Error")
        
        # Test price history retrieval with exception
        result = self.client.get_price_history("AAPL", "day")
        
        # Verify results
        self.assertEqual(result, {})
    
    def test_market_hours_string_conversion(self):
        """Test market hours with string input."""
        # Mock response data
        mock_hours_data = {"equity": {"isOpen": True}}
        self.mock_response.json.return_value = mock_hours_data
        self.mock_client.market_hours.return_value = self.mock_response
        
        # Test with string input
        result = self.client.get_market_hours("equity")
        
        # Verify results
        self.assertEqual(result, mock_hours_data)
        self.mock_client.market_hours.assert_called_once_with("equity")


class TestMarketDataIntegration(unittest.TestCase):
    """Integration tests for market data functionality."""
    
    @unittest.skip("Requires real API credentials")
    def test_real_quote_retrieval(self):
        """Test real quote retrieval (requires valid credentials)."""
        # This test requires real API credentials
        # It's skipped by default but can be run manually
        client = SchwabClient()
        result = client.get_quote("AAPL")
        
        # Basic validation
        self.assertIsInstance(result, dict)
        if result:  # If API call succeeds
            self.assertIn("symbol", result)
    
    @unittest.skip("Requires real API credentials")
    def test_real_market_hours(self):
        """Test real market hours retrieval (requires valid credentials)."""
        # This test requires real API credentials
        client = SchwabClient()
        result = client.get_market_hours(["equity"])
        
        # Basic validation
        self.assertIsInstance(result, dict)
        if result:  # If API call succeeds
            self.assertIn("equity", result)


if __name__ == '__main__':
    unittest.main()
