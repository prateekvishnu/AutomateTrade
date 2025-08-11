"""
Comprehensive Examples for Charles Schwab API

This file demonstrates all the major functionality of the Schwab API client
including account management, market data, order management, and real-time streaming.

IMPORTANT: 
- Add your credentials to a .env file before running
- This is for educational purposes - use paper trading for testing
- Never commit API credentials to version control
"""

import datetime
import json
import time
from typing import Dict, Any

# Import the SchwabClient class
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from schwab_client import SchwabClient


def example_account_management(client: SchwabClient):
    """Demonstrate account management functionality."""
    print("\n" + "="*50)
    print("ACCOUNT MANAGEMENT EXAMPLES")
    print("="*50)
    
    try:
        # Get linked accounts
        print("\n1. Getting linked accounts...")
        linked_accounts = client.get_linked_accounts()
        if linked_accounts:
            print(f"Found {len(linked_accounts)} linked account(s)")
            for i, account in enumerate(linked_accounts):
                print(f"  Account {i+1}: {account.get('accountNumber', 'N/A')} - {account.get('hashValue', 'N/A')}")
            
            # Use first account for examples
            account_hash = linked_accounts[0].get('hashValue')
            print(f"Using account hash: {account_hash}")
            
            # Get account details
            print("\n2. Getting account details...")
            account_details = client.get_account_details(account_hash)
            if account_details:
                print("Account details retrieved successfully")
                # Print key account information
                if 'securitiesAccount' in account_details:
                    sec_account = account_details['securitiesAccount']
                    print(f"  Account Type: {sec_account.get('type', 'N/A')}")
                    print(f"  Account Number: {sec_account.get('accountNumber', 'N/A')}")
            
            # Get account positions
            print("\n3. Getting account positions...")
            positions = client.get_account_positions(account_hash)
            if positions:
                print("Positions retrieved successfully")
                if 'securitiesAccount' in positions and 'positions' in positions['securitiesAccount']:
                    pos_list = positions['securitiesAccount']['positions']
                    print(f"  Number of positions: {len(pos_list)}")
                    for pos in pos_list[:3]:  # Show first 3 positions
                        symbol = pos.get('instrument', {}).get('symbol', 'N/A')
                        quantity = pos.get('longQuantity', 0)
                        print(f"    {symbol}: {quantity} shares")
            
            # Get recent orders
            print("\n4. Getting recent orders...")
            end_date = datetime.datetime.now(datetime.timezone.utc)
            start_date = end_date - datetime.timedelta(days=30)
            orders = client.get_orders(account_hash, start_date, end_date)
            if orders:
                print(f"Orders retrieved successfully - {len(orders)} orders found")
                for order in orders[:3]:  # Show first 3 orders
                    order_id = order.get('orderId', 'N/A')
                    status = order.get('status', 'N/A')
                    print(f"    Order {order_id}: {status}")
            
            # Get transactions
            print("\n5. Getting recent transactions...")
            transactions = client.get_transactions(account_hash, start_date, end_date, "TRADE")
            if transactions:
                print(f"Transactions retrieved successfully - {len(transactions)} transactions found")
                for tx in transactions[:3]:  # Show first 3 transactions
                    tx_id = tx.get('transactionId', 'N/A')
                    tx_type = tx.get('type', 'N/A')
                    print(f"    Transaction {tx_id}: {tx_type}")
            
            # Get user preferences
            print("\n6. Getting user preferences...")
            preferences = client.get_user_preferences()
            if preferences:
                print("User preferences retrieved successfully")
            
            return account_hash
            
        else:
            print("No linked accounts found")
            return None
            
    except Exception as e:
        print(f"Error in account management examples: {e}")
        return None


def example_market_data(client: SchwabClient):
    """Demonstrate market data functionality."""
    print("\n" + "="*50)
    print("MARKET DATA EXAMPLES")
    print("="*50)
    
    try:
        # Get single quote
        print("\n1. Getting single quote for AAPL...")
        quote = client.get_quote("AAPL")
        if quote:
            print("AAPL Quote retrieved successfully")
            # Print key quote information
            if 'quoteResponse' in quote and 'result' in quote['quoteResponse']:
                result = quote['quoteResponse']['result'][0]
                symbol = result.get('symbol', 'N/A')
                price = result.get('regularMarketPrice', 'N/A')
                change = result.get('regularMarketChange', 'N/A')
                volume = result.get('regularMarketVolume', 'N/A')
                print(f"  {symbol}: ${price} ({change:+}) - Volume: {volume}")
        
        # Get multiple quotes
        print("\n2. Getting quotes for multiple symbols...")
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        quotes = client.get_quotes(symbols)
        if quotes:
            print(f"Multiple quotes retrieved successfully - {len(quotes)} symbols")
            if 'quoteResponse' in quotes and 'result' in quotes['quoteResponse']:
                for result in quotes['quoteResponse']['result'][:3]:  # Show first 3
                    symbol = result.get('symbol', 'N/A')
                    price = result.get('regularMarketPrice', 'N/A')
                    print(f"  {symbol}: ${price}")
        
        # Get price history
        print("\n3. Getting price history for AAPL...")
        history = client.get_price_history("AAPL", "month")
        if history:
            print("Price history retrieved successfully")
            if 'candles' in history:
                candles = history['candles']
                print(f"  {len(candles)} price points retrieved")
                if candles:
                    latest = candles[-1]
                    print(f"  Latest: ${latest.get('close', 'N/A')} at {latest.get('datetime', 'N/A')}")
        
        # Get option chain
        print("\n4. Getting option chain for AAPL...")
        options = client.get_option_chain("AAPL", contractType="CALL", range="ITM")
        if options:
            print("Option chain retrieved successfully")
            if 'optionExpDateMap' in options:
                exp_dates = list(options['optionExpDateMap'].keys())
                print(f"  {len(exp_dates)} expiration dates available")
                if exp_dates:
                    print(f"  First expiration: {exp_dates[0]}")
        
        # Get market hours
        print("\n5. Getting market hours...")
        market_hours = client.get_market_hours(["equity", "option"])
        if market_hours:
            print("Market hours retrieved successfully")
            for market in market_hours:
                market_type = market.get('key', 'N/A')
                is_open = market.get('isOpen', False)
                print(f"  {market_type}: {'OPEN' if is_open else 'CLOSED'}")
        
        # Get movers
        print("\n6. Getting market movers...")
        try:
            movers_response = client.client.movers("$DJI")
            if movers_response.status_code == 200:
                movers = movers_response.json()
                print("Market movers retrieved successfully")
                if 'movers' in movers:
                    print(f"  {len(movers['movers'])} movers found")
            else:
                print("Market movers not available")
        except Exception as e:
            print(f"Market movers error: {e}")
        
        # Get instruments
        print("\n7. Getting instrument details...")
        try:
            instruments_response = client.client.instruments("AAPL", "fundamental")
            if instruments_response.status_code == 200:
                instruments = instruments_response.json()
                print("Instrument details retrieved successfully")
                if 'instruments' in instruments:
                    print(f"  {len(instruments['instruments'])} instruments found")
            else:
                print("Instrument details not available")
        except Exception as e:
            print(f"Instrument details error: {e}")
        
    except Exception as e:
        print(f"Error in market data examples: {e}")


def example_order_management(client: SchwabClient, account_hash: str):
    """Demonstrate order management functionality."""
    print("\n" + "="*50)
    print("ORDER MANAGEMENT EXAMPLES")
    print("="*50)
    
    if not account_hash:
        print("No account hash available - skipping order management examples")
        return
    
    try:
        # Create order examples (not executed)
        print("\n1. Creating order examples...")
        
        # Market order example
        market_order = client.create_market_order("AAPL", 1, "BUY")
        print("  Market order created:")
        print(f"    {json.dumps(market_order, indent=2)}")
        
        # Limit order example
        limit_order = client.create_limit_order("MSFT", 2, 300.00, "BUY")
        print("\n  Limit order created:")
        print(f"    {json.dumps(limit_order, indent=2)}")
        
        # More complex order example
        complex_order = {
            "orderType": "STOP_LIMIT",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "stopPrice": "150.00",
            "price": "151.00",
            "orderLegCollection": [
                {
                    "instruction": "BUY",
                    "quantity": 5,
                    "instrument": {
                        "symbol": "GOOGL",
                        "assetType": "EQUITY"
                    }
                }
            ]
        }
        print("\n  Complex order example:")
        print(f"    {json.dumps(complex_order, indent=2)}")
        
        print("\nNote: These are example orders and were not executed.")
        print("To actually place orders, uncomment the order execution code below.")
        
        # Uncomment the following code to actually place and manage orders
        """
        # Place a limit order
        print("\n2. Placing a limit order...")
        order_id = client.place_order(account_hash, limit_order)
        if order_id:
            print(f"Order placed successfully: {order_id}")
            
            # Wait a moment
            time.sleep(3)
            
            # Get order details
            print("\n3. Getting order details...")
            order_details = client.get_order_details(account_hash, order_id)
            if order_details:
                print("Order details retrieved successfully")
                status = order_details.get('status', 'N/A')
                print(f"  Order status: {status}")
            
            # Cancel the order
            print("\n4. Cancelling the order...")
            if client.cancel_order(account_hash, order_id):
                print("Order cancelled successfully")
            else:
                print("Failed to cancel order")
        else:
            print("Failed to place order")
        """
        
    except Exception as e:
        print(f"Error in order management examples: {e}")


def example_streaming(client: SchwabClient):
    """Demonstrate real-time streaming functionality."""
    print("\n" + "="*50)
    print("STREAMING EXAMPLES")
    print("="*50)
    
    try:
        print("\n1. Setting up streaming...")
        
        # Define a custom message handler
        def custom_handler(message):
            print(f"Stream message: {message[:200]}...")  # Truncate long messages
        
        # Start streaming with custom handler
        client.start_streaming(custom_handler)
        print("Streaming started successfully")
        
        # Subscribe to equity quotes
        print("\n2. Subscribing to equity quotes...")
        symbols = ["AAPL", "MSFT", "GOOGL"]
        fields = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Key fields
        client.subscribe_equities(symbols, fields)
        print(f"Subscribed to {len(symbols)} symbols")
        
        # Subscribe to options (example)
        print("\n3. Subscribing to option quotes...")
        try:
            # Note: These option symbols are examples and may not be valid
            option_symbols = ["AAPL 240712C00150000"]  # Example option symbol
            client.subscribe_options(option_symbols, [0, 1, 2, 3, 4, 5, 6, 7, 8])
            print(f"Subscribed to {len(option_symbols)} option symbols")
        except Exception as e:
            print(f"Option subscription error: {e}")
        
        # Subscribe to futures (example)
        print("\n4. Subscribing to futures...")
        try:
            client.streamer.send(client.streamer.level_one_futures("/ES", "0,1,2,3,4,5,6"))
            print("Subscribed to ES futures")
        except Exception as e:
            print(f"Futures subscription error: {e}")
        
        # Let the stream run for a short time
        print("\n5. Streaming data for 10 seconds...")
        print("(Press Ctrl+C to stop early)")
        time.sleep(10)
        
        # Stop streaming
        print("\n6. Stopping streaming...")
        client.stop_streaming()
        print("Streaming stopped successfully")
        
    except KeyboardInterrupt:
        print("\nStreaming interrupted by user")
        client.stop_streaming()
    except Exception as e:
        print(f"Error in streaming examples: {e}")
        client.stop_streaming()


def example_advanced_features(client: SchwabClient):
    """Demonstrate advanced API features."""
    print("\n" + "="*50)
    print("ADVANCED FEATURES EXAMPLES")
    print("="*50)
    
    try:
        # Get option expiration chain
        print("\n1. Getting option expiration chain...")
        try:
            exp_response = client.client.option_expiration_chain("AAPL")
            if exp_response.status_code == 200:
                exp_chain = exp_response.json()
                print("Option expiration chain retrieved successfully")
                if 'expirationDates' in exp_chain:
                    dates = exp_chain['expirationDates']
                    print(f"  {len(dates)} expiration dates available")
                    if dates:
                        print(f"  First 3 dates: {dates[:3]}")
            else:
                print("Option expiration chain not available")
        except Exception as e:
            print(f"Option expiration chain error: {e}")
        
        # Get instruments by CUSIP
        print("\n2. Getting instrument by CUSIP...")
        try:
            cusip_response = client.client.instrument_cusip("037833100")  # AAPL CUSIP
            if cusip_response.status_code == 200:
                cusip_data = cusip_response.json()
                print("CUSIP instrument data retrieved successfully")
                if 'instruments' in cusip_data:
                    print(f"  {len(cusip_data['instruments'])} instruments found")
            else:
                print("CUSIP instrument data not available")
        except Exception as e:
            print(f"CUSIP instrument error: {e}")
        
        # Get NYSE book data
        print("\n3. Getting NYSE book data...")
        try:
            book_response = client.client.nyse_book(["AAPL"], "0,1,2,3,4,5,6,7,8")
            if book_response.status_code == 200:
                book_data = book_response.json()
                print("NYSE book data retrieved successfully")
            else:
                print("NYSE book data not available")
        except Exception as e:
            print(f"NYSE book error: {e}")
        
        # Get chart data
        print("\n4. Getting chart data...")
        try:
            chart_response = client.client.chart_equity("AAPL", "0,1,2,3,4,5,6,7,8")
            if chart_response.status_code == 200:
                chart_data = chart_response.json()
                print("Chart data retrieved successfully")
            else:
                print("Chart data not available")
        except Exception as e:
            print(f"Chart data error: {e}")
        
        # Get screener data
        print("\n5. Getting screener data...")
        try:
            screener_response = client.client.screener_equity("NASDAQ_VOLUME_30", "0,1,2,3,4,5,6,7,8")
            if screener_response.status_code == 200:
                screener_data = screener_response.json()
                print("Screener data retrieved successfully")
            else:
                print("Screener data not available")
        except Exception as e:
            print(f"Screener data error: {e}")
        
    except Exception as e:
        print(f"Error in advanced features examples: {e}")


def main():
    """Main function to run all examples."""
    print("Charles Schwab API Examples")
    print("="*50)
    print("This script demonstrates the full functionality of the Schwab API client.")
    print("Make sure you have set up your .env file with valid credentials.")
    print("="*50)
    
    try:
        # Initialize client
        print("\nInitializing Schwab client...")
        client = SchwabClient()
        print("Client initialized successfully!")
        
        # Run examples
        account_hash = example_account_management(client)
        example_market_data(client)
        example_order_management(client, account_hash)
        example_streaming(client)
        example_advanced_features(client)
        
        print("\n" + "="*50)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*50)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Please check your credentials and try again.")
    
    finally:
        print("\nExample script completed.")


if __name__ == "__main__":
    main()
