#!/usr/bin/env python3
import requests

def list_all_markets():
    """Print all Polymarket markets using the main API endpoint"""
    url = "https://gamma-api.polymarket.com/markets"
    params = {"limit": 100, "active": True}
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    
    response = requests.get(url, params=params, headers=headers)
    markets = response.json() if response.status_code == 200 else []
    
    print(f"Found {len(markets)} Polymarket markets:")
    for i, market in enumerate(markets, 1):
        print(f"{i}. {market.get('question', 'Unknown')}")

if __name__ == "__main__":
    list_all_markets() 