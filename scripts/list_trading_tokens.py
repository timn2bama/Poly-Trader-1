#!/usr/bin/env python3
import requests

def list_trading_tokens():
    """
    Fetch and list most recently traded tokens on Polymarket
    """
    # Recent trades endpoint
    url = "https://clob.polymarket.com/trades"
    
    # Parameters - get the 10 most recent trades
    params = {
        "limit": 10
    }
    
    # Headers
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Make the request
        print("Fetching recent trades from Polymarket...")
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Failed to fetch trades (Status code: {response.status_code})")
            print(f"Response: {response.text}")
            return
        
        # Parse trades
        trades = response.json()
        
        if not trades:
            print("No recent trades found.")
            return
            
        # Get unique token IDs
        token_ids = set()
        for trade in trades:
            token_id = trade.get("asset_id")
            if token_id:
                token_ids.add(token_id)
        
        print(f"\nFound {len(token_ids)} unique trading tokens:\n")
        
        # For each token ID, get the order book to see market details
        for i, token_id in enumerate(token_ids, 1):
            print(f"Token {i}: {token_id[:10]}...{token_id[-10:]}")
            
            # Try to get order book
            book_url = "https://clob.polymarket.com/book"
            book_params = {"token_id": token_id}
            
            try:
                book_response = requests.get(book_url, params=book_params, headers=headers)
                
                if book_response.status_code == 200:
                    book = book_response.json()
                    
                    # Get bids and asks
                    bids = book.get("bids", [])
                    asks = book.get("asks", [])
                    
                    if bids or asks:
                        best_bid = float(bids[0].get("price", 0)) if bids else 0
                        best_ask = float(asks[0].get("price", 0)) if asks else 0
                        mid_price = (best_bid + best_ask) / 2 if (bids and asks) else 0
                        
                        print(f"  Market ID: {book.get('market', 'Unknown')}")
                        if bids:
                            print(f"  Best Bid: {best_bid:.4f}")
                        if asks:
                            print(f"  Best Ask: {best_ask:.4f}")
                        if bids and asks:
                            print(f"  Implied Probability: {mid_price*100:.1f}%")
                    else:
                        print("  No bids or asks available")
                else:
                    print(f"  Could not fetch order book: {book_response.status_code}")
            except Exception as e:
                print(f"  Error fetching order book: {str(e)}")
                
            print()
            
    except Exception as e:
        print(f"Error fetching trades: {e}")

if __name__ == "__main__":
    list_trading_tokens() 