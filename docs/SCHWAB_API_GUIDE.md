# Charles Schwab API Integration Guide

## Overview
This guide covers the integration with Charles Schwab's trading API using the `schwabdev` Python wrapper. The API provides access to account information, market data, order management, and real-time streaming data.

## Table of Contents
1. [Setup and Authentication](#setup-and-authentication)
2. [Account Management](#account-management)
3. [Market Data](#market-data)
4. [Order Management](#order-management)
5. [Real-time Streaming](#real-time-streaming)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Examples](#examples)

## Setup and Authentication

### Prerequisites
- Charles Schwab developer account
- App key (32 characters)
- App secret (16 characters)
- Callback URL (for OAuth flow)

### Environment Configuration
Create a `.env` file in your project root:

```bash
# .env file
app_key=your_32_character_app_key_here
app_secret=your_16_character_secret_here
callback_url=https://127.0.0.1
```

### Installation
```bash
pip install schwabdev python-dotenv
```

### Basic Client Setup
```python
import os
from dotenv import load_dotenv
import schwabdev

# Load environment variables
load_dotenv()

# Create client
client = schwabdev.Client(
    os.getenv('app_key'),
    os.getenv('app_secret'),
    os.getenv('callback_url')
)
```

## Account Management

### Get Linked Accounts
```python
# Get all linked accounts
linked_accounts = client.account_linked().json()
account_hash = linked_accounts[0].get('hashValue')

# Get account details
account_details = client.account_details(account_hash, fields="positions").json()
```

### Account Information
- **Balance**: Available cash and buying power
- **Positions**: Current holdings and quantities
- **Orders**: Pending and completed orders
- **Transactions**: Trade history and activity

## Market Data

### Stock Quotes
```python
# Single quote
quote = client.quote("AAPL").json()

# Multiple quotes
quotes = client.quotes(["AAPL", "MSFT", "GOOGL"]).json()
```

### Price History
```python
# Available periods: day, month, year, ytd
history = client.price_history("AAPL", "year").json()
```

### Option Chains
```python
# Get option chain for a symbol
options = client.option_chains("AAPL").json()

# Filtered options (CALL/PUT, ITM/OTM)
call_options = client.option_chains("AAPL", contractType="CALL", range="ITM").json()
```

### Market Hours
```python
# Get market hours for different asset types
equity_hours = client.market_hour("equity").json()
option_hours = client.market_hour("option").json()
```

## Order Management

### Order Types
- **Market Orders**: Immediate execution at current market price
- **Limit Orders**: Execution at specified price or better
- **Stop Orders**: Execution when price reaches specified level
- **Stop Limit Orders**: Combination of stop and limit orders

### Placing Orders
```python
order = {
    "orderType": "LIMIT",
    "session": "NORMAL",
    "duration": "DAY",
    "orderStrategyType": "SINGLE",
    "price": "150.00",
    "orderLegCollection": [
        {
            "instruction": "BUY",
            "quantity": 10,
            "instrument": {
                "symbol": "AAPL",
                "assetType": "EQUITY"
            }
        }
    ]
}

# Place order
response = client.order_place(account_hash, order)
order_id = response.headers.get('location', '/').split('/')[-1]
```

### Order Management
```python
# Get order details
order_details = client.order_details(account_hash, order_id).json()

# Cancel order
cancel_response = client.order_cancel(account_hash, order_id)

# Get all orders for account
orders = client.account_orders(
    account_hash,
    start_date,
    end_date
).json()
```

## Real-time Streaming

### Setup Streaming
```python
# Get streamer instance
streamer = client.stream

# Define response handler
def handle_message(message):
    print(f"Received: {message}")

# Start streaming
streamer.start(handle_message)
```

### Subscription Types
```python
# Equity quotes
streamer.send(streamer.level_one_equities("AAPL,MSFT", "0,1,2,3,4,5,6,7,8"))

# Options quotes
streamer.send(streamer.level_one_options("AAPL 240712C00150000", "0,1,2,3,4,5,6,7,8"))

# Futures quotes
streamer.send(streamer.level_one_futures("/ES", "0,1,2,3,4,5,6"))

# Order book data
streamer.send(streamer.nyse_book(["AAPL", "MSFT"], "0,1,2,3,4,5,6,7,8"))
```

### Field Definitions
Common field numbers for equity quotes:
- `0`: Symbol
- `1`: Bid Price
- `2`: Ask Price
- `3`: Last Price
- `4`: Bid Size
- `5`: Ask Size
- `6`: Volume
- `7`: High
- `8`: Low

### Stop Streaming
```python
# Stop after 60 seconds
import time
time.sleep(60)
streamer.stop()

# Keep subscriptions for next session
streamer.stop(clear_subscriptions=False)
```

## Error Handling

### Common Errors
1. **Authentication Errors**: Invalid app key/secret
2. **Rate Limiting**: Too many API calls
3. **Invalid Symbols**: Unsupported ticker symbols
4. **Order Errors**: Insufficient funds, invalid order parameters

### Error Handling Example
```python
try:
    response = client.quote("INVALID_SYMBOL")
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Exception occurred: {e}")
```

## Best Practices

### Rate Limiting
- Implement delays between API calls (3+ seconds)
- Use streaming for real-time data instead of polling
- Batch requests when possible

### Error Handling
- Always check response status codes
- Implement retry logic for transient failures
- Log all API interactions for debugging

### Security
- Never commit API credentials to version control
- Use environment variables for sensitive data
- Implement proper session management

### Performance
- Cache frequently accessed data
- Use appropriate field selections in API calls
- Monitor API usage and optimize calls

## Examples

### Complete Trading Example
```python
import os
import time
from dotenv import load_dotenv
import schwabdev

def main():
    # Setup
    load_dotenv()
    client = schwabdev.Client(
        os.getenv('app_key'),
        os.getenv('app_secret'),
        os.getenv('callback_url')
    )
    
    # Get account
    accounts = client.account_linked().json()
    account_hash = accounts[0].get('hashValue')
    
    # Get quote
    quote = client.quote("AAPL").json()
    current_price = quote.get('lastPrice', 0)
    
    # Place limit order
    if current_price > 150:
        order = {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "price": str(current_price - 5),
            "orderLegCollection": [
                {
                    "instruction": "BUY",
                    "quantity": 5,
                    "instrument": {
                        "symbol": "AAPL",
                        "assetType": "EQUITY"
                    }
                }
            ]
        }
        
        response = client.order_place(account_hash, order)
        print(f"Order placed: {response.status_code}")
    
    # Get positions
    positions = client.account_details(account_hash, fields="positions").json()
    print(f"Current positions: {positions}")

if __name__ == "__main__":
    main()
```

### Streaming Data Processing
```python
import json
import time
from datetime import datetime

def process_streaming_data():
    shared_list = []
    
    def response_handler(message):
        shared_list.append(message)
    
    # Start stream
    streamer.start(response_handler)
    streamer.send(streamer.level_one_equities("AAPL,MSFT", "0,1,2,3,4,5,6,7,8"))
    
    # Process messages
    while True:
        while len(shared_list) > 0:
            message = json.loads(shared_list.pop(0))
            
            if message.get("data"):
                for service in message["data"]:
                    service_type = service.get("service")
                    timestamp = service.get("timestamp", 0)
                    contents = service.get("content", [])
                    
                    for content in contents:
                        symbol = content.pop("key", "NO_KEY")
                        fields = content
                        print(f"[{service_type} - {symbol}]({datetime.fromtimestamp(timestamp//1000)}): {fields}")
        
        time.sleep(0.5)

# Run streaming
process_streaming_data()
```

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure `schwabdev` is properly installed
2. **Authentication Failures**: Verify app key/secret in `.env` file
3. **Streaming Issues**: Check network connectivity and firewall settings
4. **Order Failures**: Verify account has sufficient funds and valid symbols

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Support Resources
- [Schwabdev Documentation](https://tylerebowers.github.io/Schwabdev/)
- [Charles Schwab Developer Portal](https://developer.schwab.com/)
- [API Status Page](https://status.schwab.com/)

## Security Notes

⚠️ **IMPORTANT**: 
- Never share your API credentials
- Use environment variables for sensitive data
- Implement proper access controls
- Monitor API usage for suspicious activity
- Regularly rotate API keys
- Use HTTPS for all communications
- Implement proper session timeout

## Rate Limits

The Schwab API has rate limits to prevent abuse:
- **REST API**: ~120 requests per minute
- **Streaming**: Up to 500 symbols per connection
- **Order Management**: Varies by account type

Always implement appropriate delays between API calls and use streaming for real-time data when possible.
