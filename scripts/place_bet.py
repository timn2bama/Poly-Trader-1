#!/usr/bin/env python3
import requests
import datetime
import os
from dotenv import load_dotenv

# Safely load environment variables - RECOMMENDED APPROACH
load_dotenv()

def get_nba_markets():
    """Fetch NBA markets from Polymarket"""
    url = "https://gamma-api.polymarket.com/markets"
    
    # Current date for filtering
    now = datetime.datetime.now()
    min_date = now.strftime("%Y-%m-%dT00:00:00Z")
    
    params = {
        "limit": 20,
        "active": True,
        "start_date_min": min_date
    }
    
    resp = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        print(f"API request failed with status {resp.status_code}")
        return []
        
    markets = resp.json()
    if not isinstance(markets, list):
        print(f"Unexpected response format: {type(markets)}")
        return []
    
    # Filter for NBA markets
    nba_markets = []
    for market in markets:
        question = market.get('question', '').lower()
        if any(term in question for term in ['mavericks', 'nets', 'lakers', 'celtics', 'spread', 'over ']):
            nba_markets.append(market)
    
    return nba_markets

def parse_token_ids(market):
    """Parse token IDs from market data"""
    token_ids = market.get("clobTokenIds", [])
    
    if isinstance(token_ids, list):
        return [str(t) for t in token_ids]
    
    if isinstance(token_ids, str):
        try:
            import ast
            parsed = ast.literal_eval(token_ids)
            if isinstance(parsed, list):
                return parsed
        except:
            # Try simple parsing
            if token_ids.startswith("[") and token_ids.endswith("]"):
                tokens = token_ids[1:-1].split(",")
                return [t.strip(' "\'') for t in tokens if t.strip()]
            
            return [token_ids]
    
    return []

def place_bet(market, amount=1.0, bet_side="BUY"):
    """Place a bet on a specific market"""
    # IMPORTANT: Use environment variables for private keys
    # Replace this with your actual private key from .env file
    private_key = os.getenv("POLYGON_WALLET_PRIVATE_KEY", "")
    
    # Warn if no private key is found
    if not private_key:
        print("No private key found in environment variables.")
        print("Add your private key to .env file as POLYGON_WALLET_PRIVATE_KEY=your_key_here")
        print("NEVER include your private key directly in the script!")
        return False
    
    # Remove '0x' prefix if present
    if private_key.startswith('0x'):
        private_key = private_key[2:]
    
    # Get market details
    question = market.get('question', 'Unknown')
    token_ids = parse_token_ids(market)
    
    if not token_ids:
        print("No token IDs found for this market")
        return False
    
    try:
        # Import the required client packages
        try:
            from py_clob_client.client import ClobClient
            from py_clob_client.clob_types import OrderArgs, OrderType
            from py_clob_client.order_builder.constants import BUY, SELL
        except ImportError:
            print("Required packages not found. Installing...")
            import subprocess
            subprocess.check_call(["pip", "install", "py_clob_client"])
            from py_clob_client.client import ClobClient
            from py_clob_client.clob_types import OrderArgs, OrderType
            from py_clob_client.order_builder.constants import BUY, SELL
        
        print(f"Initializing CLOB client...")
        # Initialize the CLOB client
        client = ClobClient(
            host="https://clob.polymarket.com",
            key=private_key,
            chain_id=137  # Polygon chain ID
        )
        
        # Generate API credentials
        print("Generating API credentials...")
        api_creds = client.create_or_derive_api_creds()
        client.set_api_creds(api_creds)
        
        # Choose the token ID for the first outcome
        token_id = token_ids[0]
        
        # Set the side
        side = BUY if bet_side.upper() == "BUY" else SELL
        
        # Get current market price
        book_url = "https://clob.polymarket.com/book"
        book_params = {"token_id": token_id}
        book_resp = requests.get(book_url, params=book_params)
        
        price = 0.5  # Default to 50% if we can't get the price
        if book_resp.status_code == 200:
            book_data = book_resp.json()
            asks = book_data.get("asks", [])
            if asks:
                # Use the best ask price if available
                price = float(asks[0]["price"])
        
        print(f"Creating order for {amount} USDC on {question} at price {price}...")
        
        # Create order args
        order_args = OrderArgs(
            token_id=token_id,
            price=price,
            size=amount,
            side=side
        )
        
        # Create and sign the order
        print("Signing order...")
        signed_order = client.create_order(order_args)
        
        # Submit the order
        print("Submitting order...")
        order_result = client.post_order(signed_order, OrderType.GTC)
        
        print(f"Order placed successfully!")
        print(f"Order ID: {order_result.get('orderID', order_result.get('id', 'unknown'))}")
        return True
        
    except Exception as e:
        print(f"Error placing bet: {e}")
        return False

def main():
    print("=" * 60)
    print("POLYMARKET BET PLACER")
    print("=" * 60)
    
    # Get NBA markets
    print("Fetching NBA markets...")
    nba_markets = get_nba_markets()
    
    if not nba_markets:
        print("No NBA markets found")
        return
    
    print(f"Found {len(nba_markets)} NBA markets")
    
    # Display the first few markets
    for i, market in enumerate(nba_markets[:5]):
        question = market.get('question', 'Unknown')
        print(f"{i+1}. {question}")
    
    # Ask which market to bet on
    print("\nWhich market would you like to bet on? (enter number, or 1 for first market)")
    choice = input("> ").strip()
    
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(nba_markets):
            print("Invalid selection, using first market")
            idx = 0
    except:
        print("Invalid input, using first market")
        idx = 0
    
    selected_market = nba_markets[idx]
    question = selected_market.get('question', 'Unknown')
    
    print(f"\nSelected market: {question}")
    
    # Ask for bet amount
    print("\nBet amount in USDC (default: 1.0):")
    amount_str = input("> ").strip()
    
    try:
        amount = float(amount_str) if amount_str else 1.0
        if amount <= 0:
            print("Invalid amount, using 1.0 USDC")
            amount = 1.0
    except:
        print("Invalid amount, using 1.0 USDC")
        amount = 1.0
    
    # Ask for bet side
    print("\nBet side (buy/sell) - default: buy")
    side = input("> ").strip().upper()
    if side not in ["BUY", "SELL"]:
        print("Invalid side, using BUY")
        side = "BUY"
    
    # Final confirmation
    print("\n" + "=" * 60)
    print(f"PLACING BET ON: {question}")
    print(f"AMOUNT: {amount} USDC")
    print(f"SIDE: {side}")
    print("=" * 60)
    
    print("\nConfirm bet placement? (y/n)")
    confirm = input("> ").strip().lower()
    
    if confirm == 'y':
        place_bet(selected_market, amount, side)
    else:
        print("Bet cancelled")

if __name__ == "__main__":
    main() 