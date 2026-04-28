#!/usr/bin/env python3
import requests
import time
import datetime

def fetch_current_markets():
    """Fetch current markets from Polymarket using timestamp to avoid cached data"""
    
    # Use current timestamp to try to avoid cached data
    current_timestamp = int(time.time() * 1000)
    
    # API endpoint
    url = "https://gamma-api.polymarket.com/markets"
    
    # Parameters
    params = {
        "limit": 100,
        "active": True,
        "t": current_timestamp  # Add timestamp to avoid caching
    }
    
    # Headers with up-to-date user agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Cache-Control": "no-cache"
    }
    
    try:
        # Make the request
        print(f"Fetching markets with timestamp: {current_timestamp}")
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Failed to fetch markets (Status code: {response.status_code})")
            print(f"Response: {response.text}")
            return
        
        # Parse markets
        markets = response.json()
        
        # Check if we got an object or array
        if isinstance(markets, dict):
            print(f"Received object instead of array: {markets}")
            return
            
        # Sort markets by end date (newest first)
        try:
            markets.sort(key=lambda x: x.get("endDate", ""), reverse=True)
        except:
            print("Could not sort markets by end date")
            
        # Print each market with end date
        print(f"Found {len(markets)} markets on Polymarket:\n")
        
        newest_end_date = None
        
        for i, market in enumerate(markets, 1):
            question = market.get('question', 'Unknown')
            end_date = market.get('endDate', 'Unknown')
            
            # Format date if available
            formatted_date = "Unknown"
            if end_date != 'Unknown':
                try:
                    date_obj = datetime.datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
                    
                    # Track the newest date
                    if newest_end_date is None or date_obj > newest_end_date:
                        newest_end_date = date_obj
                except:
                    pass
            
            # Print market details
            print(f"{i}. {question}")
            print(f"   End Date: {formatted_date}")
            print()
            
        # Print the newest end date
        if newest_end_date:
            print(f"Newest market end date: {newest_end_date.strftime('%Y-%m-%d %H:%M')}")
            today = datetime.datetime.now()
            days_diff = (newest_end_date - today).days
            print(f"Days from now: {days_diff}")
            
    except Exception as e:
        print(f"Error fetching markets: {e}")
        
if __name__ == "__main__":
    fetch_current_markets() 