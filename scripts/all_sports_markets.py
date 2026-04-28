#!/usr/bin/env python3
import requests
import datetime
from typing import List, Dict, Any

def get_sports_markets() -> List[Dict[str, Any]]:
    """
    Fetch all sports-related markets from Polymarket
    """
    print("Fetching sports markets from Polymarket...")
    
    # API endpoint
    url = "https://gamma-api.polymarket.com/markets"
    
    # Request parameters
    params = {
        "limit": 100,
        "active": True  # Get active markets
    }
    
    # Request headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # Make API request
        response = requests.get(url, params=params, headers=headers)
        
        # Check response status
        if response.status_code != 200:
            print(f"Error fetching markets: {response.status_code}")
            return []
        
        # Parse response
        markets = response.json()
        
        # Validate response format
        if not isinstance(markets, list):
            print("Unexpected API response format")
            return []
        
        print(f"Retrieved {len(markets)} active markets")
        
        # Filter for sports-related markets
        sports_markets = []
        sports_terms = [
            # Basketball terms
            "nba", "basketball", "lakers", "celtics", "warriors", "knicks", "bulls",
            
            # Baseball terms
            "mlb", "baseball", "yankees", "dodgers", "red sox", 
            
            # Football terms 
            "nfl", "football", "chiefs", "eagles", "cowboys", "super bowl",
            
            # Soccer terms
            "soccer", "premier league", "uefa", "champions league", "fifa", "world cup",
            
            # Other sports
            "tennis", "golf", "boxing", "ufc", "mma", "hockey", "nhl", "olympics"
        ]
        
        for market in markets:
            question = market.get("question", "").lower()
            description = market.get("description", "").lower()
            category = market.get("category", "").lower()
            
            # Combine text fields for searching
            market_text = f"{question} {description} {category}"
            
            # Check if any sports term is in the market text
            if any(term in market_text for term in sports_terms):
                sports_markets.append(market)
        
        print(f"Found {len(sports_markets)} sports-related markets")
        return sports_markets
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_sport_category(market_text: str) -> str:
    """Classify market into sport category"""
    market_text = market_text.lower()
    
    if any(x in market_text for x in ["nba", "basketball"]):
        return "Basketball"
    elif any(x in market_text for x in ["mlb", "baseball"]):
        return "Baseball"
    elif any(x in market_text for x in ["nfl", "football", "super bowl"]) and "soccer" not in market_text:
        return "Football"
    elif any(x in market_text for x in ["soccer", "premier league", "fifa", "uefa", "manchester", "liverpool"]):
        return "Soccer"
    elif any(x in market_text for x in ["tennis", "atp", "wta"]):
        return "Tennis"
    elif any(x in market_text for x in ["ufc", "mma", "boxing", "fight"]):
        return "Combat Sports"
    elif any(x in market_text for x in ["nhl", "hockey"]):
        return "Hockey"
    elif any(x in market_text for x in ["golf", "pga"]):
        return "Golf"
    
    return "Other Sports"

def format_date(date_str: str) -> str:
    """Format ISO date string to readable format"""
    if not date_str:
        return "Unknown"
    
    try:
        date_obj = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_obj.strftime("%Y-%m-%d %H:%M")
    except:
        return date_str

def display_markets(markets: List[Dict[str, Any]]) -> None:
    """Display all markets in a readable format"""
    # Group markets by category
    categories = {}
    
    for market in markets:
        question = market.get("question", "")
        category = get_sport_category(question)
        
        if category not in categories:
            categories[category] = []
        
        categories[category].append(market)
    
    # Print summary
    print("\nSports Markets by Category:")
    for category, cat_markets in categories.items():
        print(f"- {category}: {len(cat_markets)} markets")
    
    # Display markets by category
    for category, cat_markets in categories.items():
        print(f"\n{'=' * 70}")
        print(f"{category.upper()} MARKETS")
        print(f"{'=' * 70}")
        
        for i, market in enumerate(cat_markets):
            question = market.get("question", "Unknown Market")
            end_date = format_date(market.get("endDate", ""))
            
            # Get outcomes if available
            outcomes = market.get("outcomes", [])
            if isinstance(outcomes, str):
                try:
                    import ast
                    outcomes = ast.literal_eval(outcomes)
                except:
                    outcomes = [outcomes]
            
            # Get volume if available
            volume = market.get("volume", "N/A")
            if volume:
                try:
                    volume = f"${float(volume):.2f}"
                except:
                    volume = "N/A"
            
            # Display market with index for reference
            print(f"\n{i+1}. {question}")
            print(f"   End Date: {end_date}")
            print(f"   Volume: {volume}")
            
            # Display outcomes if available
            if outcomes and isinstance(outcomes, list):
                print("   Outcomes:")
                for outcome in outcomes:
                    print(f"   - {outcome}")
            
            # Separator between markets
            print(f"   {'-' * 50}")

def main() -> None:
    """Main function"""
    print("SPORTS BETTING MARKETS ON POLYMARKET")
    print("=" * 70)
    
    # Get sports markets
    markets = get_sports_markets()
    
    if not markets:
        print("\nNo sports markets found.")
        print("Try again later or check for other market types.")
        return
    
    # Display markets
    display_markets(markets)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"Total sports markets: {len(markets)}")
    print("=" * 70)
    print("\nNote: These markets may or may not have active order books.")
    print("To place bets, visit the Polymarket website (https://polymarket.com).")

if __name__ == "__main__":
    main() 