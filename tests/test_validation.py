import pytest
from pydantic import ValidationError
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from poly_trader.models import MarketData

def test_market_data_valid():
    data = {
        "name": "Will BTC hit 100k?",
        "description": "Bitcoin test market",
        "yes_odds": "65%",
        "no_odds": "35%",
        "recommendation": "YES",
        "bet_amount": "$100",
        "expected_profit": "$50",
        "confidence": "High",
        "icon": "📈"
    }
    market = MarketData(**data)
    assert market.name == "Will BTC hit 100k?"
    assert market.yes_odds == "65%"

def test_market_data_invalid_odds_format():
    data = {
        "name": "Test Market",
        "yes_odds": "65", # Missing %
        "no_odds": "35%",
        "recommendation": "YES",
        "bet_amount": "$100",
        "expected_profit": "$50",
        "confidence": "High",
        "icon": "📈"
    }
    with pytest.raises(ValidationError) as exc:
        MarketData(**data)
    assert "Odds must end with '%'" in str(exc.value)

def test_market_data_invalid_odds_range():
    data = {
        "name": "Test Market",
        "yes_odds": "150%", # Out of range
        "no_odds": "35%",
        "recommendation": "YES",
        "bet_amount": "$100",
        "expected_profit": "$50",
        "confidence": "High",
        "icon": "📈"
    }
    with pytest.raises(ValidationError) as exc:
        MarketData(**data)
    assert "between 0 and 100" in str(exc.value)

def test_market_data_invalid_confidence():
    data = {
        "name": "Test Market",
        "yes_odds": "50%",
        "no_odds": "50%",
        "recommendation": "YES",
        "bet_amount": "$100",
        "expected_profit": "$50",
        "confidence": "Maybe", # Invalid confidence
        "icon": "📈"
    }
    with pytest.raises(ValidationError) as exc:
        MarketData(**data)
    assert "High/Medium/Low or a percentage" in str(exc.value)
