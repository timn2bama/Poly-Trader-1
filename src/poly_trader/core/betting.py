#!/usr/bin/env python3
import json
import logging
from typing import Dict, Any, Optional, List, Tuple
from web3 import Web3
from eth_account import Account
from poly_trader.config import settings
from poly_trader.core.clob import get_clob_client
from poly_trader.data.db import SessionLocal, Trade
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY, SELL
from uuid import uuid4

# Audit Logger Setup
audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)
if not audit_logger.handlers:
    audit_handler = logging.FileHandler('audit_trail.log')
    audit_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    audit_logger.addHandler(audit_handler)

# General Logger Setup
logger = logging.getLogger(__name__)

# Constants
USDC_CONTRACT = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
POLYMARKET_EXCHANGE = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"
RPC_URL = "https://polygon-rpc.com"

# Custom Exceptions
class SecurityError(Exception): pass
class InsufficientBalanceError(Exception): pass
class OrderRejectedError(Exception): pass
class NetworkError(Exception): pass
class OrderVerificationError(Exception): pass

def place_bet_on_market(token_id: str, price: float, side: str = "BUY", size: float = 1.0, question: str = "Unknown", outcome: str = "Unknown") -> str:
    """
    Place a bet and record it in the SQLite database.
    """
    bet_id = str(uuid4())
    db = SessionLocal()
    
    try:
        client = get_clob_client()
        
        # Determine side
        order_side = BUY if side.upper() == "BUY" else SELL
        
        # Create the order
        order_args = OrderArgs(
            price=price,
            size=size,
            side=order_side,
            token_id=token_id
        )
        
        signed_order = client.create_order(order_args)
        
        # Record attempt in database
        new_trade = Trade(
            bet_id=bet_id,
            token_id=token_id,
            question=question,
            side=side.upper(),
            outcome=outcome.upper(),
            price=price,
            size=size,
            total_amount=price * size,
            status="PENDING"
        )
        db.add(new_trade)
        db.commit()
        
        # Post the order to the CLOB
        resp = client.post_order(signed_order, OrderType.GTC)
        
        if resp and resp.get('success'):
            order_id = resp.get('orderID')
            
            # Update database record
            new_trade.order_id = order_id
            new_trade.status = "FILLED"
            db.commit()
            
            audit_logger.info(f"BET_PLACED|{bet_id}|{token_id}|{side}|{size}|{order_id}|SUCCESS")
            logger.info(f"✅ Bet placed successfully! Order ID: {order_id}")
            return order_id
        else:
            error_msg = resp.get('errorMsg', 'Unknown error')
            new_trade.status = "FAILED"
            db.commit()
            raise OrderRejectedError(error_msg)
            
    except Exception as e:
        audit_logger.error(f"BET_FAILED|{bet_id}|{token_id}|{side}|{size}|{str(e)}")
        logger.error(f"❌ Failed to place bet: {e}")
        db.rollback()
        raise
    finally:
        db.close()
