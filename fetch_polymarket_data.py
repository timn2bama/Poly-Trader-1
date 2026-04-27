#!/usr/bin/env python3
import json
from serpapi import GoogleSearch
import os
import logging
from config import settings
from models import MarketData, MarketDataResponse

logger = logging.getLogger(__name__)

def fetch_polymarket_data() -> dict:
    """
    Fetch real Polymarket data using SerpAPI
    """
    serp_api_key = settings.serpapi_api_key.get_secret_value() if settings.serpapi_api_key else None
    
    if not serp_api_key:
        logger.warning("SERPAPI_API_KEY not found in environment variables. Using fallback data.")
        return fetch_fallback_data()
    
    params = {
        "api_key": serp_api_key,
        "engine": "google",
        "q": "polymarket active markets site:polymarket.com",
        "num": 5,
        "tbm": "nws"
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        organic_results = results.get("organic_results", results.get("news_results", []))
        markets = []
        
        for result in organic_results:
            if "link" not in result or "/event/" not in result["link"]:
                continue
                
            title = result.get("title", "").replace(" | Polymarket", "").strip()
            snippet = result.get("snippet", "")
            
            # Since we cannot fetch real odds without the CLOB API, we use placeholders
            # and explicitly mark this as incomplete data.
            market_data = {
                "name": title,
                "url": result["link"],
                "description": snippet,
                "yes_odds": "50%",
                "no_odds": "50%",
                "recommendation": "NONE",
                "bet_amount": "$0",
                "expected_profit": "$0",
                "confidence": "Low",
                "icon": "🔮"
            }
            
            try:
                validated = MarketData(**market_data)
                markets.append(validated)
            except Exception as e:
                logger.error(f"Market validation error: {e}")
                
        # If no valid markets were fetched, use fallback
        if not markets:
            return fetch_fallback_data()
            
        total_bet = sum(float(m.bet_amount.replace("$", "")) for m in markets)
        total_profit = sum(float(m.expected_profit.replace("$", "")) for m in markets)
        roi = (total_profit / total_bet * 100) if total_bet > 0 else 0
        
        response = MarketDataResponse(
            markets=markets,
            total_bet_amount=total_bet,
            total_expected_profit=total_profit,
            roi_percentage=round(roi, 1),
            data_source="serpapi"
        )
        return response.model_dump()
        
    except Exception as e:
        logger.error(f"Error fetching Polymarket data: {e}")
        return fetch_fallback_data()

def fetch_fallback_data() -> dict:
    """Fallback data in case the API fails"""
    raw_markets = [
        {
            "name": "Will Donald Trump win the 2024 US Presidential Election?",
            "url": "https://polymarket.com/event/will-donald-trump-win-the-2024-us-presidential-election",
            "description": "This market resolves to 'YES' if Donald Trump is elected...",
            "yes_odds": "59%",
            "no_odds": "41%",
            "recommendation": "YES",
            "bet_amount": "$300",
            "expected_profit": "$208.47",
            "confidence": "94%",
            "icon": "🗳️"
        }
    ]
    
    markets = []
    for m in raw_markets:
        try:
            markets.append(MarketData(**m))
        except Exception as e:
            logger.error(f"Fallback data invalid: {e}")
            
    total_bet = sum(float(m.bet_amount.replace("$", "")) for m in markets)
    total_profit = sum(float(m.expected_profit.replace("$", "")) for m in markets)
    roi = (total_profit / total_bet * 100) if total_bet > 0 else 0
    
    response = MarketDataResponse(
        markets=markets,
        total_bet_amount=total_bet,
        total_expected_profit=total_profit,
        roi_percentage=round(roi, 1),
        data_source="mock_fallback"
    )
    return response.model_dump()

if __name__ == "__main__":
    data = fetch_polymarket_data()
    print(json.dumps(data, indent=2))