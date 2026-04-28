#!/usr/bin/env python3
import requests
import datetime

def fetch_current_polymarket_markets():
    """
    Fetch current markets from Polymarket using the updated API endpoint
    """
    # Try alternative endpoint
    url = "https://gamma-api.polymarket.com/markets"
    
    # Parameters for active markets
    params = {
        "active": True,
        "limit": 100
    }
    
    # Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        # Make the request
        print("Fetching current markets from Polymarket...")
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Failed to fetch markets (Status code: {response.status_code})")
            print(f"Response: {response.text}")
            return
        
        # Parse markets
        markets = response.json()
        
        # Check if we got valid data
        if not isinstance(markets, list):
            print(f"Unexpected response format: {type(markets)}")
            print(markets)
            return
            
        # Print each market
        print(f"Found {len(markets)} markets on Polymarket:\n")
        
        # Get current year for filtering
        current_year = datetime.datetime.now().year
        
        # Filter markets with a reasonable end date (after 2023)
        current_markets = []
        for market in markets:
            end_date = market.get('endDate', '')
            if end_date:
                try:
                    date_obj = datetime.datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                    if date_obj.year >= 2023:
                        current_markets.append(market)
                except:
                    pass
        
        if not current_markets:
            print("No current markets found. The API seems to be returning historical data.")
            
            # Let's try to check the most recent data
            try:
                # Sort markets by most recent end date
                markets.sort(key=lambda x: x.get('endDate', ''), reverse=True)
                most_recent = markets[0]
                end_date = most_recent.get('endDate', '')
                if end_date:
                    date_obj = datetime.datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                    print(f"Most recent market end date: {date_obj.strftime('%Y-%m-%d')}")
            except:
                pass
            
            return
            
        # Print each market
        for i, market in enumerate(current_markets, 1):
            question = market.get('question', 'Unknown')
            end_date = market.get('endDate', 'Unknown')
            
            # Format date if available
            formatted_date = "Unknown"
            if end_date != 'Unknown':
                try:
                    date_obj = datetime.datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted_date = end_date
            
            # Print market details
            print(f"{i}. {question}")
            print(f"   End Date: {formatted_date}")
            print()
    
    except Exception as e:
        print(f"Error fetching markets: {e}")

if __name__ == "__main__":
    fetch_current_polymarket_markets() 