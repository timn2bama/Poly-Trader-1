#!/usr/bin/env python3
import json
import logging
import time
from typing import List, Dict, Any
from poly_trader.config import settings
from poly_trader.models import MarketData, MarketDataResponse
from poly_trader.core.clob import get_clob_client

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Issue 8: Simple TTL cache to avoid hammering external APIs
# ---------------------------------------------------------------------------
_cache: dict = {}

def cached_fetch(key: str, fetch_fn, ttl_seconds: int = 60):
    """Simple TTL cache for API results."""
    now = time.time()
    if key in _cache:
        value, expires_at = _cache[key]
        if now < expires_at:
            return value
    result = fetch_fn()
    _cache[key] = (result, now + ttl_seconds)
    return result


# ---------------------------------------------------------------------------
# Issue 7: Retry with exponential backoff for transient API failures
# ---------------------------------------------------------------------------
def fetch_with_retry(fetch_fn, max_retries=3, backoff_base=2):
    """Retry a fetch function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return fetch_fn()
        except (OSError, ConnectionError, TimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            wait = backoff_base ** attempt
            print(f"Fetch failed (attempt {attempt+1}/{max_retries}): {e}. Retrying in {wait}s...")
            time.sleep(wait)


# ---------------------------------------------------------------------------
# Issue 2: Real OpenAI probability estimate (replaces random.randint)
# ---------------------------------------------------------------------------
def get_ai_probability(question: str, description: str = "") -> float:
    """Ask OpenAI to estimate probability for a prediction market question."""
    import openai

    if not settings.openai_api_key:
        return 0.5  # neutral if no API key

    client = openai.OpenAI(api_key=settings.openai_api_key.get_secret_value())

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # cheap and fast
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a prediction market analyst. Respond ONLY with a number "
                        "between 0 and 1 representing the probability that the following "
                        "event will resolve YES. No explanation."
                    ),
                },
                {"role": "user", "content": f"Question: {question}\nDescription: {description}"},
            ],
            max_tokens=10,
            temperature=0.3,
        )
        prob = float(response.choices[0].message.content.strip())
        return max(0.05, min(0.95, prob))  # clamp to reasonable range
    except (ValueError, IndexError, AttributeError) as e:
        print(f"OpenAI call failed: {e}")
        return 0.5  # neutral fallback
    except Exception as e:
        print(f"OpenAI call failed: {e}")
        return 0.5  # neutral fallback


def fetch_polymarket_data() -> dict:
    """
    Fetch real Polymarket data using the CLOB API.
    """
    try:
        client = get_clob_client()
        logger.info("Fetching markets from Polymarket CLOB...")

        # Issue 8: wrap in TTL cache (60s) to avoid rate-limit abuse
        # Issue 7: wrap the raw network call in retry/backoff
        markets_data = cached_fetch(
            'polymarket_markets',
            lambda: fetch_with_retry(client.get_markets),
            ttl_seconds=60,
        )

        # Handle different response formats if necessary
        if isinstance(markets_data, dict):
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
            description = m.get('description', '')

            # Issue 2: replace random.randint with a real OpenAI estimate
            yes_prob_float = get_ai_probability(question, description)
            yes_prob = int(yes_prob_float * 100)
            no_prob = 100 - yes_prob

            # Strategy: Simple edge detection
            recommendation = "YES" if yes_prob < 45 else ("NO" if yes_prob > 55 else "HOLD")
            confidence = "High" if abs(yes_prob - 50) > 20 else "Medium"

            # Calculate hypothetical bet amounts based on bankroll
            bankroll = settings.initial_bankroll
            bet_amount = bankroll * 0.1  # 10% for example
            expected_profit = (
                bet_amount * (100 / yes_prob - 1)
                if recommendation == "YES"
                else bet_amount * (100 / no_prob - 1)
            )

            market_entry = {
                "name": question,
                "url": f"https://polymarket.com/event/{m.get('condition_id', '')}",
                "description": description,
                "yes_odds": f"{yes_prob}%",
                "no_odds": f"{no_prob}%",
                "recommendation": recommendation,
                "bet_amount": f"${bet_amount:.0f}",
                "expected_profit": f"${expected_profit:.2f}",
                "confidence": confidence,
                "icon": "📈" if yes_prob > 50 else "📉",
            }

            # Issue 9: specific exception instead of bare except
            try:
                validated = MarketData(**market_entry)
                validated_markets.append(validated)
                count += 1
            except (ValueError, TypeError, KeyError) as e:
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
            data_source="clob_api",
        )
        return response.model_dump()

    except (OSError, ConnectionError, TimeoutError, ValueError) as e:
        logger.error(f"Error fetching Polymarket CLOB data: {e}")
        return fetch_fallback_data()
    except Exception as e:
        logger.error(f"Error fetching Polymarket CLOB data: {e}")
        return fetch_fallback_data()


def fetch_fallback_data() -> dict:
    """Fallback data in case the API fails. Includes a timestamp so the UI can show staleness."""
    import datetime

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
            "icon": "₿",
        }
    ]

    markets = []
    for m in raw_markets:
        try:
            markets.append(MarketData(**m))
        except (ValueError, TypeError, KeyError) as e:
            logger.error(f"Fallback data invalid: {e}")

    total_bet = sum(float(m.bet_amount.replace("$", "")) for m in markets)
    total_profit = sum(float(m.expected_profit.replace("$", "")) for m in markets)
    roi = (total_profit / total_bet * 100) if total_bet > 0 else 0

    response = MarketDataResponse(
        markets=markets,
        total_bet_amount=total_bet,
        total_expected_profit=total_profit,
        roi_percentage=round(roi, 1),
        data_source="clob_fallback",
    )
    result = response.model_dump()
    result["fallback_timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = fetch_polymarket_data()
    print(json.dumps(data, indent=2))
