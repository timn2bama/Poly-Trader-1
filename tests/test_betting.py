import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from poly_trader.core.betting import place_bet_on_market, OrderRejectedError

@patch('poly_trader.core.betting.SessionLocal')
@patch('poly_trader.core.betting.get_clob_client')
def test_place_bet_on_market_db_record(mock_get_client, mock_session_local):
    # Mock database session
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    
    # Mock client and response
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.create_order.return_value = {"signed": "order"}
    mock_client.post_order.return_value = {"success": True, "orderID": "0x123"}
    
    order_id = place_bet_on_market("token_yes", 0.5, "BUY", 10.0, "Test?", "YES")
    
    assert order_id == "0x123"
    # Verify DB calls
    assert mock_db.add.called
    assert mock_db.commit.called
    mock_db.close.assert_called_once()

@patch('poly_trader.core.betting.SessionLocal')
@patch('poly_trader.core.betting.get_clob_client')
def test_place_bet_on_market_db_failed(mock_get_client, mock_session_local):
    # Mock database session
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    
    # Mock client and failure response
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.create_order.return_value = {"signed": "order"}
    mock_client.post_order.return_value = {"success": False, "errorMsg": "Failed"}
    
    with pytest.raises(OrderRejectedError):
        place_bet_on_market("token_yes", 0.5, "BUY", 10.0)
    
    # Verify DB reflected failure
    assert mock_db.commit.called
    mock_db.close.assert_called_once()
