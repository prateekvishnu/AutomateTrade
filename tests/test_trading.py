"""
Test module for trading functionality.

This module tests the ability to send trades, manage orders, and handle
trading operations through the Charles Schwab API.
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


class TestTrading(unittest.TestCase):
    """Test cases for trading functionality."""
    
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
        
        # Sample account hash for testing
        self.test_account_hash = "test_account_hash_123"
    
    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()
    
    def test_place_market_order_success(self):
        """Test successful market order placement."""
        # Mock successful response
        self.mock_response.status_code = 201
        self.mock_response.headers = {'location': '/orders/12345'}
        self.mock_client.order_place.return_value = self.mock_response
        
        # Test order placement
        order = self.client.create_market_order("AAPL", 100, "BUY")
        result = self.client.place_order(self.test_account_hash, order)
        
        # Verify results
        self.assertEqual(result, "12345")
        self.mock_client.order_place.assert_called_once_with(self.test_account_hash, order)
    
    def test_place_limit_order_success(self):
        """Test successful limit order placement."""
        # Mock successful response
        self.mock_response.status_code = 200
        self.mock_response.headers = {'location': '/orders/67890'}
        self.mock_client.order_place.return_value = self.mock_response
        
        # Test order placement
        order = self.client.create_limit_order("GOOGL", 50, 2800.00, "BUY")
        result = self.client.place_order(self.test_account_hash, order)
        
        # Verify results
        self.assertEqual(result, "67890")
        self.mock_client.order_place.assert_called_once_with(self.test_account_hash, order)
    
    def test_place_order_failure(self):
        """Test order placement failure."""
        # Mock failed response
        self.mock_response.status_code = 400
        self.mock_client.order_place.return_value = self.mock_response
        
        # Test order placement
        order = self.client.create_market_order("INVALID", 100, "BUY")
        result = self.client.place_order(self.test_account_hash, order)
        
        # Verify results
        self.assertIsNone(result)
    
    def test_cancel_order_success(self):
        """Test successful order cancellation."""
        # Mock successful response
        self.mock_response.status_code = 200
        self.mock_client.order_cancel.return_value = self.mock_response
        
        # Test order cancellation
        result = self.client.cancel_order(self.test_account_hash, "12345")
        
        # Verify results
        self.assertTrue(result)
        self.mock_client.order_cancel.assert_called_once_with(self.test_account_hash, "12345")
    
    def test_cancel_order_failure(self):
        """Test order cancellation failure."""
        # Mock failed response
        self.mock_response.status_code = 404
        self.mock_client.order_cancel.return_value = self.mock_response
        
        # Test order cancellation
        result = self.client.cancel_order(self.test_account_hash, "invalid_id")
        
        # Verify results
        self.assertFalse(result)
    
    def test_get_order_details(self):
        """Test order details retrieval."""
        # Mock response data
        mock_order_data = {
            "orderId": "12345",
            "status": "FILLED",
            "filledQuantity": 100,
            "orderType": "MARKET",
            "orderLegCollection": [
                {
                    "instruction": "BUY",
                    "quantity": 100,
                    "instrument": {"symbol": "AAPL", "assetType": "EQUITY"}
                }
            ]
        }
        self.mock_response.json.return_value = mock_order_data
        self.mock_client.order_details.return_value = self.mock_response
        
        # Test order details retrieval
        result = self.client.get_order_details(self.test_account_hash, "12345")
        
        # Verify results
        self.assertEqual(result, mock_order_data)
        self.mock_client.order_details.assert_called_once_with(self.test_account_hash, "12345")
    
    def test_get_orders_by_date_range(self):
        """Test retrieving orders within a date range."""
        # Mock response data
        mock_orders_data = [
            {
                "orderId": "12345",
                "status": "FILLED",
                "orderType": "MARKET"
            },
            {
                "orderId": "67890",
                "status": "PENDING",
                "orderType": "LIMIT"
            }
        ]
        self.mock_response.json.return_value = mock_orders_data
        self.mock_client.account_orders.return_value = self.mock_response
        
        # Test orders retrieval
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        result = self.client.get_orders(self.test_account_hash, start_date, end_date)
        
        # Verify results
        self.assertEqual(result, mock_orders_data)
        self.mock_client.account_orders.assert_called_once_with(self.test_account_hash, start_date, end_date)
    
    def test_get_account_positions(self):
        """Test account positions retrieval."""
        # Mock response data
        mock_positions_data = {
            "positions": [
                {
                    "instrument": {"symbol": "AAPL", "assetType": "EQUITY"},
                    "longQuantity": 100,
                    "marketValue": 15000.00
                }
            ]
        }
        self.mock_response.json.return_value = mock_positions_data
        self.mock_client.account_details.return_value = self.mock_response
        
        # Test positions retrieval
        result = self.client.get_account_positions(self.test_account_hash)
        
        # Verify results
        self.assertEqual(result, mock_positions_data)
        self.mock_client.account_details.assert_called_once_with(self.test_account_hash, fields="positions")
    
    def test_get_linked_accounts(self):
        """Test linked accounts retrieval."""
        # Mock response data
        mock_accounts_data = [
            {
                "hashValue": "account_hash_1",
                "accountNumber": "123456789",
                "accountType": "INDIVIDUAL"
            },
            {
                "hashValue": "account_hash_2",
                "accountNumber": "987654321",
                "accountType": "IRA"
            }
        ]
        self.mock_response.json.return_value = mock_accounts_data
        self.mock_client.account_linked.return_value = self.mock_response
        
        # Test linked accounts retrieval
        result = self.client.get_linked_accounts()
        
        # Verify results
        self.assertEqual(result, mock_accounts_data)
        self.mock_client.account_linked.assert_called_once()
    
    def test_create_market_order(self):
        """Test market order creation."""
        # Test market order creation
        order = self.client.create_market_order("AAPL", 100, "BUY")
        
        # Verify order structure
        self.assertEqual(order["orderType"], "MARKET")
        self.assertEqual(order["orderLegCollection"][0]["instruction"], "BUY")
        self.assertEqual(order["orderLegCollection"][0]["quantity"], 100)
        self.assertEqual(order["orderLegCollection"][0]["instrument"]["symbol"], "AAPL")
        self.assertEqual(order["orderLegCollection"][0]["instrument"]["assetType"], "EQUITY")
    
    def test_create_limit_order(self):
        """Test limit order creation."""
        # Test limit order creation
        order = self.client.create_limit_order("GOOGL", 50, 2800.00, "SELL")
        
        # Verify order structure
        self.assertEqual(order["orderType"], "LIMIT")
        self.assertEqual(order["price"], "2800.0")
        self.assertEqual(order["orderLegCollection"][0]["instruction"], "SELL")
        self.assertEqual(order["orderLegCollection"][0]["quantity"], 50)
        self.assertEqual(order["orderLegCollection"][0]["instrument"]["symbol"], "GOOGL")
    
    def test_get_transactions(self):
        """Test transactions retrieval."""
        # Mock response data
        mock_transactions_data = [
            {
                "transactionId": "txn_1",
                "type": "TRADE",
                "amount": 15000.00,
                "date": "2024-01-01"
            }
        ]
        self.mock_response.json.return_value = mock_transactions_data
        self.mock_client.transactions.return_value = self.mock_response
        
        # Test transactions retrieval
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        result = self.client.get_transactions(self.test_account_hash, start_date, end_date, "TRADE")
        
        # Verify results
        self.assertEqual(result, mock_transactions_data)
        self.mock_client.transactions.assert_called_once_with(
            self.test_account_hash, start_date, end_date, "TRADE"
        )
    
    def test_place_order_exception_handling(self):
        """Test exception handling in order placement."""
        # Mock exception
        self.mock_client.order_place.side_effect = Exception("API Error")
        
        # Test order placement with exception
        order = self.client.create_market_order("AAPL", 100, "BUY")
        result = self.client.place_order(self.test_account_hash, order)
        
        # Verify results
        self.assertIsNone(result)
    
    def test_cancel_order_exception_handling(self):
        """Test exception handling in order cancellation."""
        # Mock exception
        self.mock_client.order_cancel.side_effect = Exception("API Error")
        
        # Test order cancellation with exception
        result = self.client.cancel_order(self.test_account_hash, "12345")
        
        # Verify results
        self.assertFalse(result)
    
    def test_get_order_details_exception_handling(self):
        """Test exception handling in order details retrieval."""
        # Mock exception
        self.mock_client.order_details.side_effect = Exception("API Error")
        
        # Test order details retrieval with exception
        result = self.client.get_order_details(self.test_account_hash, "12345")
        
        # Verify results
        self.assertEqual(result, {})


class TestTradingIntegration(unittest.TestCase):
    """Integration tests for trading functionality."""
    
    @unittest.skip("Requires real API credentials")
    def test_real_order_placement(self):
        """Test real order placement (requires valid credentials)."""
        # This test requires real API credentials
        # It's skipped by default but can be run manually
        client = SchwabClient()
        
        # Get linked accounts first
        accounts = client.get_linked_accounts()
        if accounts:
            account_hash = accounts[0].get('hashValue')
            
            # Create a small test order (paper trading recommended)
            order = client.create_market_order("AAPL", 1, "BUY")
            result = client.place_order(account_hash, order)
            
            # Basic validation
            self.assertIsInstance(result, (str, type(None)))
    
    @unittest.skip("Requires real API credentials")
    def test_real_account_positions(self):
        """Test real account positions retrieval (requires valid credentials)."""
        # This test requires real API credentials
        client = SchwabClient()
        
        # Get linked accounts first
        accounts = client.get_linked_accounts()
        if accounts:
            account_hash = accounts[0].get('hashValue')
            
            # Get positions
            result = client.get_account_positions(account_hash)
            
            # Basic validation
            self.assertIsInstance(result, dict)


class TestOrderValidation(unittest.TestCase):
    """Test cases for order validation and structure."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'app_key': '12345678901234567890123456789012',
            'app_secret': '1234567890123456',
            'callback_url': 'https://example.com/callback'
        })
        self.env_patcher.start()
        
        # Create SchwabClient instance
        with patch('schwabdev.Client'):
            self.client = SchwabClient()
    
    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()
    
    def test_market_order_structure(self):
        """Test market order structure validation."""
        order = self.client.create_market_order("TSLA", 200, "BUY")
        
        # Verify required fields
        required_fields = ["orderType", "session", "duration", "orderStrategyType", "orderLegCollection"]
        for field in required_fields:
            self.assertIn(field, order)
        
        # Verify order type
        self.assertEqual(order["orderType"], "MARKET")
        
        # Verify order leg collection
        self.assertIsInstance(order["orderLegCollection"], list)
        self.assertEqual(len(order["orderLegCollection"]), 1)
        
        leg = order["orderLegCollection"][0]
        self.assertEqual(leg["instruction"], "BUY")
        self.assertEqual(leg["quantity"], 200)
        self.assertEqual(leg["instrument"]["symbol"], "TSLA")
    
    def test_limit_order_structure(self):
        """Test limit order structure validation."""
        order = self.client.create_limit_order("MSFT", 75, 300.50, "SELL")
        
        # Verify required fields
        required_fields = ["orderType", "session", "duration", "orderStrategyType", "price", "orderLegCollection"]
        for field in required_fields:
            self.assertIn(field, order)
        
        # Verify order type and price
        self.assertEqual(order["orderType"], "LIMIT")
        self.assertEqual(order["price"], "300.5")
        
        # Verify order leg collection
        leg = order["orderLegCollection"][0]
        self.assertEqual(leg["instruction"], "SELL")
        self.assertEqual(leg["quantity"], 75)
        self.assertEqual(leg["instrument"]["symbol"], "MSFT")
    
    def test_order_leg_instrument_structure(self):
        """Test order leg instrument structure validation."""
        order = self.client.create_market_order("NVDA", 100, "BUY")
        leg = order["orderLegCollection"][0]
        instrument = leg["instrument"]
        
        # Verify instrument structure
        self.assertIn("symbol", instrument)
        self.assertIn("assetType", instrument)
        self.assertEqual(instrument["symbol"], "NVDA")
        self.assertEqual(instrument["assetType"], "EQUITY")


if __name__ == '__main__':
    unittest.main()
