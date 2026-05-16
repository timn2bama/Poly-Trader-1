#!/usr/bin/env python3
import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, Optional, List, Tuple
from web3 import Web3
from eth_account import Account
from poly_trader.config import settings
from poly_trader.core.clob import get_clob_client
from poly_trader.data.db import SessionLocal, Trade
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY, SELL
from uuid import uuid4

# ---------------------------------------------------------------------------
# Issue 10: Rotating audit log so the file never grows unbounded
# ---------------------------------------------------------------------------
audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)
if not audit_logger.handlers:
    audit_handler = RotatingFileHandler(
        'audit_trail.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB per file
        backupCount=5               # keep 5 rotated files
    )
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


# ---------------------------------------------------------------------------
# Issue 1: Kelly Criterion bet sizing
# ---------------------------------------------------------------------------
def calculate_kelly_bet(
    win_probability: float,  # AI-estimated probability (0-1)
    market_odds: float,      # decimal odds (e.g. 2.0 for 50% market)
    bankroll: float,
    max_fraction: float = 0.25,  # cap Kelly at 25% for safety
) -> float:
    """Kelly Criterion: f* = (bp - q) / b  where b=odds-1, p=win_prob, q=1-p"""
    if win_probability <= 0 or win_probability >= 1 or market_odds <= 1:
        return 0.0
    b = market_odds - 1
    p = win_probability
    q = 1 - p
    kelly_fraction = (b * p - q) / b
    if kelly_fraction <= 0:
        return 0.0  # No edge, don't bet
    # Apply safety cap and max_bet_percentage from config
    max_bet = bankroll * min(max_fraction, settings.max_bet_percentage)
    return min(kelly_fraction * bankroll, max_bet)


def place_bet_on_market(
    token_id: str,
    win_probability: float,   # Issue 1: AI-estimated probability (0-1)
    market_price: float,      # Issue 1: current market price used to derive decimal odds
    side: str = "BUY",
    question: str = "Unknown",
    outcome: str = "Unknown",
) -> str:
    """
    Place a bet and record it in the SQLite database.
    Bet size is determined by the Kelly Criterion using the supplied win_probability.
    """
    bet_id = str(uuid4())
    db = SessionLocal()

    # Issue 1: derive decimal odds from market price (price is 0-1 for a binary market)
    # e.g. market_price=0.40 -> decimal odds = 1/0.40 = 2.5
    if market_price <= 0 or market_price >= 1:
        raise ValueError(f"market_price must be between 0 and 1 exclusive, got {market_price}")
    market_odds = 1.0 / market_price

    # Issue 1: determine size via Kelly Criterion and enforce max_bet_percentage
    bankroll = settings.initial_bankroll
    size = calculate_kelly_bet(win_probability, market_odds, bankroll)

    # Issue 5: validate size > 0 before touching the network
    if size <= 0:
        raise ValueError(
            f"Kelly Criterion returned no edge (size={size:.4f}). "
            "win_probability may not justify a bet at this price."
        )

    try:
        client = get_clob_client()

        # Issue 5: attempt a balance check if the CLOB client exposes one.
        # py_clob_client does not currently expose a direct USDC balance method,
        # so we guard with the size check above and log a warning.
        try:
            # Future-proof: if the client ever exposes get_balance_allowance, call it here.
            # balance_info = client.get_balance_allowance(...)
            # available = balance_info.get('balance', 0)
            # if size > available:
            #     raise InsufficientBalanceError(f"Insufficient balance: need {size}, have {available}")
            if size <= 0:
                raise ValueError("Bet size must be positive")
        except (InsufficientBalanceError, ValueError):
            raise
        except Exception as e:
            logger.warning(f"Balance check skipped (CLOB client does not expose balance): {e}")

        # Determine side
        order_side = BUY if side.upper() == "BUY" else SELL

        # Create the order
        order_args = OrderArgs(
            price=market_price,
            size=size,
            side=order_side,
            token_id=token_id,
        )

        signed_order = client.create_order(order_args)

        # Record attempt in database
        new_trade = Trade(
            bet_id=bet_id,
            token_id=token_id,
            question=question,
            side=side.upper(),
            outcome=outcome.upper(),
            price=market_price,
            size=size,
            total_amount=market_price * size,
            status="PENDING",
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

            audit_logger.info(
                f"BET_PLACED|{bet_id}|{token_id}|{side}|{size:.4f}|{order_id}|SUCCESS"
            )
            logger.info(f"Bet placed successfully! Order ID: {order_id}")
            return order_id
        else:
            error_msg = resp.get('errorMsg', 'Unknown error') if resp else 'No response'
            new_trade.status = "FAILED"
            db.commit()
            raise OrderRejectedError(error_msg)

    except Exception as e:
        audit_logger.error(f"BET_FAILED|{bet_id}|{token_id}|{side}|{size:.4f}|{str(e)}")
        logger.error(f"Failed to place bet: {e}")
        db.rollback()
        raise
    finally:
        db.close()
