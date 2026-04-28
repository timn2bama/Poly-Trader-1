#!/usr/bin/env python3
import requests

def fetch_order_book():
    """
    Fetch the order book for a known current market (Trump 2024 Presidential Election)
    """
    # Trump 2024 Election token ID from documentation example
    token_id = "21742633143463906290569050155826241533067272736897614950488156847949938836455"
    
    # Order book endpoint
    url = f"https://clob.polymarket.com/book"
    
    # Parameters
    params = {
        "token_id": token_id
    }
    
    # Headers
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Make the request
        print(f"Fetching order book for token ID: {token_id[:10]}...{token_id[-10:]}")
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Failed to fetch order book (Status code: {response.status_code})")
            print(f"Response: {response.text}")
            return
        
        # Parse order book
        book = response.json()
        
        print("\nOrder Book for 'Will Donald Trump win the 2024 US Presidential Election?' - YES token\n")
        
        # Display bid orders (buy orders)
        bids = book.get("bids", [])
        if bids:
            print("BID ORDERS (Buying YES tokens):")
            print("-" * 40)
            print("Price    |  Size  ")
            print("-" * 40)
            for bid in bids[:10]:  # Show top 10 bids
                price = float(bid.get("price", 0))
                size = float(bid.get("size", 0))
                print(f"{price:.4f}   |  {size:.1f}")
        else:
            print("No bid orders found.")
            
        print()
        
        # Display ask orders (sell orders)
        asks = book.get("asks", [])
        if asks:
            print("ASK ORDERS (Selling YES tokens):")
            print("-" * 40)
            print("Price    |  Size  ")
            print("-" * 40)
            for ask in asks[:10]:  # Show top 10 asks
                price = float(ask.get("price", 0))
                size = float(ask.get("size", 0))
                print(f"{price:.4f}   |  {size:.1f}")
        else:
            print("No ask orders found.")
            
        # Calculate and display market implied probability
        if bids and asks:
            best_bid = float(bids[0].get("price", 0))
            best_ask = float(asks[0].get("price", 0))
            mid_price = (best_bid + best_ask) / 2
            
            print("\nMARKET SUMMARY:")
            print(f"Best Bid: {best_bid:.4f} (Buying YES at {best_bid*100:.1f}%)")
            print(f"Best Ask: {best_ask:.4f} (Selling YES at {best_ask*100:.1f}%)")
            print(f"Mid Price: {mid_price:.4f} (Implied probability: {mid_price*100:.1f}%)")
            
    except Exception as e:
        print(f"Error fetching order book: {e}")

if __name__ == "__main__":
    fetch_order_book() 