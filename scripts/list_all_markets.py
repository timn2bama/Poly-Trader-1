#!/usr/bin/env python3
import requests
import datetime

def list_all_markets():
    """Fetch and display all active markets from Polymarket with end dates"""
    
    # API endpoint for active markets
    url = "https://gamma-api.polymarket.com/markets"
    
    # Parameters to get all active markets
    params = {"limit": 100, "active": True}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    
    # Make the request
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch markets (Status code: {response.status_code})")
        return
    
    # Parse markets
    markets = response.json()
    
    # Print each market with end date
    print(f"Found {len(markets)} active markets on Polymarket:\n")
    
    for i, market in enumerate(markets, 1):
        question = market.get('question', 'Unknown')
        end_date = market.get('endDate', 'Unknown')
        
        # Format date if available
        if end_date != 'Unknown':
            try:
                date_obj = datetime.datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                end_date = date_obj.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        
        # Print market details
        print(f"{i}. {question}")
        print(f"   End Date: {end_date}")
        print()

if __name__ == "__main__":
    list_all_markets() 