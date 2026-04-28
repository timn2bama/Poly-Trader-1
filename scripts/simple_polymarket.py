#!/usr/bin/env python3
import requests
import datetime

def get_polymarket_markets():
    # Try different endpoints to get current markets
    endpoints = [
        "https://gamma-api.polymarket.com/markets",
        "https://gamma-api.polymarket.com/popular-markets",
        "https://gamma-api.polymarket.com/trending-markets"
    ]
    
    # Current date for filtering
    now = datetime.datetime.now()
    min_date = now.strftime("%Y-%m-%dT00:00:00Z")
    
    for endpoint in endpoints:
        print(f"\nTrying endpoint: {endpoint}")
        params = {
            "limit": 20, 
            "active": True, 
            "start_date_min": min_date  # Only get current markets
        }
        
        resp = requests.get(endpoint, params=params, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            print(f"Failed with status code: {resp.status_code}")
            continue
            
        markets = resp.json()
        if not markets:
            print("No markets returned")
            continue
            
        # Check if we got a list or a response with data field
        if isinstance(markets, dict) and 'data' in markets:
            markets = markets['data']
            
        if not isinstance(markets, list):
            print(f"Unexpected response format: {type(markets)}")
            continue
            
        print(f"Found {len(markets)} markets")
        for m in markets:
            question = m.get('question', 'Unknown')
            volume = float(m.get('volume', 0))
            category = m.get('category', 'Unknown')
            end_date = m.get('endDate', 'Unknown')
            
            # Format date
            if end_date != 'Unknown':
                try:
                    date_obj = datetime.datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                    end_date = date_obj.strftime("%Y-%m-%d")
                except:
                    pass
                    
            print(f"[{category}] {question} - Vol: ${volume:.2f} - End: {end_date}")

if __name__ == "__main__":
    get_polymarket_markets() 