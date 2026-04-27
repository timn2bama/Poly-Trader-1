import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from place_polymarket_bet import place_market_order, NetworkError, InsufficientBalanceError, OrderRejectedError, verify_order_placed

def test_verify_order_placed_success():
    assert verify_order_placed({"orderID": "123", "status": "filled"}) == True
    assert verify_order_placed({"tx_data": {"to": "0x123"}}) == True

def test_verify_order_placed_failure():
    assert verify_order_placed({"status": "failed"}) == False
    assert verify_order_placed({"error": "something went wrong"}) == False

@patch('requests.post')
def test_place_market_order_network_error(mock_post):
    mock_post.side_effect = Exception("Connection timeout")
    
    with pytest.raises(NetworkError) as exc:
        place_market_order("token123", "buy", 10, "0xwallet", "0xprivate", MagicMock())
    
    assert "API request failed" in str(exc.value)

@patch('requests.post')
def test_place_market_order_insufficient_balance(mock_post):
    # Mock signature response
    mock_sig_resp = MagicMock()
    mock_sig_resp.status_code = 200
    mock_sig_resp.json.return_value = {"nonce": 1, "expiration": 123, "signature": "0xsig"}
    
    # Mock order response
    mock_order_resp = MagicMock()
    mock_order_resp.status_code = 400
    mock_order_resp.text = "Insufficient balance"
    
    mock_post.side_effect = [mock_sig_resp, mock_order_resp]
    
    with pytest.raises(InsufficientBalanceError):
        place_market_order("token123", "buy", 10, "0xwallet", "0xprivate", MagicMock())
