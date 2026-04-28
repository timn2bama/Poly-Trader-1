#!/usr/bin/env python3
import requests
import datetime
from typing import List, Dict, Any, Optional, Union

def get_sports_markets():
    url = "https://gamma-api.polymarket.com/markets"
    
    # Current date for filtering
    now = datetime.datetime.now()
    min_date = now.strftime("%Y-%m-%dT00:00:00Z")
    
    # Parameters to get sports markets
    params = {
        "limit": 50,  # Get more markets
        "active": True,
        "start_date_min": min_date
    }
    
    # Make request
    resp = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        print(f"API request failed with status code: {resp.status_code}")
        return []
        
    markets = resp.json()
    if not isinstance(markets, list):
        print(f"Unexpected response format: {type(markets)}")
        return []
    
    # Group markets by type
    nba_markets = []
    nfl_markets = []
    other_sports = []
    
    for market in markets:
        question = market.get('question', '').lower()
        
        # Parse outcomes
        outcomes = market.get('outcomes', [])
        if isinstance(outcomes, str):
            try:
                import ast
                outcomes = ast.literal_eval(outcomes)
            except:
                outcomes = [outcomes]
        
        # Identify market type
        if any(team in question for team in ['mavericks', 'nets', 'lakers', 'celtics', 'knicks', 'over ']):
            nba_markets.append(market)
        elif any(team in question for team in ['cowboys', 'chiefs', 'eagles', 'packers', 'nfl']):
            nfl_markets.append(market)
        elif any(sport in question for sport in ['soccer', 'baseball', 'tennis', 'hockey', 'golf']):
            other_sports.append(market)
    
    return {
        'nba': nba_markets,
        'nfl': nfl_markets,
        'other': other_sports
    }

def display_markets(markets_by_type):
    """Display markets in a nice format"""
    print("=" * 60)
    print(" POLYMARKET SPORTS BETTING MARKETS")
    print("=" * 60)
    
    # Display NBA markets
    if markets_by_type['nba']:
        print("\n🏀 NBA MARKETS")
        print("-" * 60)
        
        for market in markets_by_type['nba']:
            question = market.get('question', 'Unknown')
            end_date = market.get('endDate', '')
            
            # Format date
            if end_date:
                try:
                    date_obj = datetime.datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                    end_date = date_obj.strftime("%Y-%m-%d")
                except:
                    end_date = "Unknown date"
            
            # Display market info
            print(f"Market: {question}")
            print(f"End Date: {end_date}")
            
            # Show outcomes and probabilities
            outcomes = market.get('outcomes', [])
            prices = market.get('outcomePrices', [])
            
            if outcomes and prices and len(outcomes) == len(prices):
                for i, (outcome, price) in enumerate(zip(outcomes, prices)):
                    try:
                        probability = float(price) * 100
                        print(f"  {outcome}: {probability:.1f}%")
                    except:
                        print(f"  {outcome}: Unknown price")
            
            print("-" * 60)
    else:
        print("\nNo NBA markets found")
    
    # Display NFL markets
    if markets_by_type['nfl']:
        print("\n🏈 NFL MARKETS")
        print("-" * 60)
        
        for market in markets_by_type['nfl']:
            question = market.get('question', 'Unknown')
            print(f"Market: {question}")
            print("-" * 60)
    else:
        print("\nNo NFL markets found")
    
    # Display other sports markets
    if markets_by_type['other']:
        print("\n⚽ OTHER SPORTS MARKETS")
        print("-" * 60)
        
        for market in markets_by_type['other']:
            question = market.get('question', 'Unknown')
            print(f"Market: {question}")
            print("-" * 60)
    else:
        print("\nNo other sports markets found")

def main():
    markets_by_type = get_sports_markets()
    
    total_markets = len(markets_by_type['nba']) + len(markets_by_type['nfl']) + len(markets_by_type['other'])
    if total_markets == 0:
        print("No sports markets found")
        return
    
    display_markets(markets_by_type)
    print(f"\nTotal sports markets found: {total_markets}")

if __name__ == "__main__":
    main() 