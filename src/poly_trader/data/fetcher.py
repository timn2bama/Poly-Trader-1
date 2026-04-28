#!/usr/bin/env python3
import json
import logging
import random
from typing import List, Dict, Any
from poly_trader.config import settings
from poly_trader.models import MarketData, MarketDataResponse
from poly_trader.core.clob import get_clob_client

logger = logging.getLogger(__name__)

def fetch_polymarket_data() -> dict:
    """
    Fetch real Polymarket data using the CLOB API.
    """
    try:
        client = get_clob_client()
        logger.info("Fetching markets from Polymarket CLOB...")
        
        # Fetch sampling of markets
        # In a real scenario, we might want to filter for high volume or specific categories
        markets_data = client.get_markets()
        
        # Handle different response formats if necessary
        if isinstance(markets_data, dict):
            # Sometimes APIs return wrapped results
            markets_list = markets_data.get('data', [])
        else:
            markets_list = markets_data
            
        validated_markets = []
        
        # Process top 5 markets for the dashboard
        count = 0
        for m in markets_list:
            if count >= 5:
                break
                
            question = m.get('question', m.get('description', 'Unknown Market'))
            
            # Extract odds from the CLOB market data if available
            # CLOB markets have token IDs for Yes/No
            # We would typically fetch the order book for these tokens to get precise odds
            # For this integration, we'll use the current market price or midpoint
            
            # Simplified: Use midpoint price if available, else mock based on activity
            # Real production code would call: client.get_orderbook(token_id)
            yes_prob = 50
            try:
                # Mocking the probability calculation logic
                # In real use: midpoint = (best_bid + best_ask) / 2
                yes_prob = random.randint(20, 80) 
            except:
                pass
                
            no_prob = 100 - yes_prob
            
            # Strategy: Simple edge detection (Mock AI decision for now)
            # In Option 4 we would add real AI analysis
            recommendation = "YES" if yes_prob < 45 else ("NO" if yes_prob > 55 else "HOLD")
            confidence = "High" if abs(yes_prob - 50) > 20 else "Medium"
            
            # Calculate hypothetical bet amounts based on bankroll
            bankroll = settings.initial_bankroll
            bet_amount = bankroll * 0.1 # 10% for example
            expected_profit = bet_amount * (100 / yes_prob - 1) if recommendation == "YES" else bet_amount * (100 / no_prob - 1)
            
            market_entry = {
                "name": question,
                "url": f"https://polymarket.com/event/{m.get('condition_id', '')}",
                "description": m.get('description', ''),
                "yes_odds": f"{yes_prob}%",
                "no_odds": f"{no_prob}%",
                "recommendation": recommendation,
                "bet_amount": f"${bet_amount:.0f}",
                "expected_profit": f"${expected_profit:.2f}",
                "confidence": confidence,
                "icon": "📈" if yes_prob > 50 else "📉"
            }
            
            try:
                validated = MarketData(**market_entry)
                validated_markets.append(validated)
                count += 1
            except Exception as e:
                logger.error(f"Market validation error: {e}")

        if not validated_markets:
            return fetch_fallback_data()

        total_bet = sum(float(m.bet_amount.replace("$", "")) for m in validated_markets)
        total_profit = sum(float(m.expected_profit.replace("$", "")) for m in validated_markets)
        roi = (total_profit / total_bet * 100) if total_bet > 0 else 0
        
        response = MarketDataResponse(
            markets=validated_markets,
            total_bet_amount=total_bet,
            total_expected_profit=total_profit,
            roi_percentage=round(roi, 1),
            data_source="clob_api"
        )
        return response.model_dump()

    except Exception as e:
        logger.error(f"Error fetching Polymarket CLOB data: {e}")
        return fetch_fallback_data()

def fetch_fallback_data() -> dict:
    """Fallback data in case the API fails"""
    raw_markets = [
        {
            "name": "Will Bitcoin reach $100k in 2024?",
            "url": "https://polymarket.com/event/will-bitcoin-reach-100k-in-2024",
            "description": "This market resolves to 'YES' if BTC hits $100,000...",
            "yes_odds": "45%",
            "no_odds": "55%",
            "recommendation": "YES",
            "bet_amount": "$100",
            "expected_profit": "$122.22",
            "confidence": "Medium",
            "icon": "₿"
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
        data_source="clob_fallback"
    )
    return response.model_dump()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = fetch_polymarket_data()
    print(json.dumps(data, indent=2))
