#!/usr/bin/env python3
import requests
import json
import logging
from typing import Dict, Any, Optional, List, Tuple
from web3 import Web3
from eth_account import Account
from config import settings
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
POLYMARKET_EXCHANGE = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"
USDC_CONTRACT = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
RPC_URL = "https://polygon-rpc.com"
CLOB_API_URL = "https://clob.polymarket.com"

# Custom Exceptions
class SecurityError(Exception): pass
class InsufficientBalanceError(Exception): pass
class OrderRejectedError(Exception): pass
class NetworkError(Exception): pass
class OrderVerificationError(Exception): pass

def get_wallet_info() -> Tuple[str, str, Web3]:
    private_key_secret = settings.polygon_wallet_private_key
    if not private_key_secret:
        raise SecurityError("No private key found in configuration.")
    
    private_key = private_key_secret.get_secret_value()
    if not private_key.startswith("0x"):
        private_key = "0x" + private_key
    
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        if not w3.is_connected():
            raise NetworkError("Failed to connect to Polygon network")
    except Exception as e:
        raise NetworkError(f"Connection failed: {e}")
    
    account = Account.from_key(private_key)
    return account.address, private_key, w3

def check_usdc_approval(wallet_address: str, w3: Web3) -> bool:
    usdc_abi = json.loads('''[
        {"constant": true, "inputs": [{"name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"},
        {"constant": true, "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}
    ]''')
    
    try:
        usdc_contract = w3.eth.contract(address=USDC_CONTRACT, abi=usdc_abi)
        balance = usdc_contract.functions.balanceOf(wallet_address).call()
        if balance == 0:
            raise InsufficientBalanceError("Zero USDC balance in wallet.")
            
        current_allowance = usdc_contract.functions.allowance(wallet_address, POLYMARKET_EXCHANGE).call()
        return current_allowance > 0 and current_allowance >= 1_000_000
    except Exception as e:
        logger.error(f"Failed checking USDC: {e}")
        raise NetworkError("Error verifying USDC balance/allowance")

def verify_order_placed(order_result: dict) -> bool:
    """Verify order was actually placed successfully"""
    if "tx_data" in order_result:
        return True # On-chain settlement required
        
    required_fields = ['orderID']
    if not all(field in order_result for field in required_fields):
        return False
        
    # Depending on API response, check status if present
    if 'status' in order_result and order_result.get('status') not in ['pending', 'filled', 'partially-filled', 'success', 'live']:
        return False
        
    return True

def place_market_order(
    token_id: str, 
    side: str, 
    size: float, 
    wallet_address: str, 
    private_key: str,
    w3: Web3
) -> str:
    
    try:
        order = {
            "order": {
                "token_id": token_id,
                "side": side.upper(),
                "type": "MARKET",
                "size": str(size),
                "time_in_force": "FOK"
            }
        }
        
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = requests.post(f"{CLOB_API_URL}/orders/signature", headers=headers, json=order, timeout=10)
        response.raise_for_status()
        
        signature_data = response.json()
        if not all([signature_data.get("nonce"), signature_data.get("expiration"), signature_data.get("signature")]):
            raise OrderRejectedError("Incomplete signature data from CLOB")
            
        signed_order = {
            "token_id": token_id,
            "side": side.upper(),
            "type": "MARKET",
            "size": str(size),
            "time_in_force": "FOK",
            "nonce": signature_data["nonce"],
            "expiration": signature_data["expiration"],
            "signature": signature_data["signature"],
            "wallet": wallet_address
        }
        
        order_response = requests.post(f"{CLOB_API_URL}/orders", headers=headers, json=signed_order, timeout=10)
        if order_response.status_code == 400 and "insufficient" in order_response.text.lower():
            raise InsufficientBalanceError("Insufficient balance to place order.")
            
        order_response.raise_for_status()
        order_result = order_response.json()
        
        if not verify_order_placed(order_result):
            raise OrderVerificationError(f"Order placement unconfirmed: {order_result}")
            
        if "tx_data" in order_result:
            tx_data = order_result["tx_data"]
            tx = {
                'from': wallet_address,
                'to': tx_data.get("to"),
                'data': tx_data.get("data"),
                'value': w3.to_wei(0, 'ether'),
                'gas': 500000,
                'gasPrice': w3.to_wei('50', 'gwei'),
                'nonce': w3.eth.get_transaction_count(wallet_address),
            }
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            if tx_receipt['status'] != 1:
                raise OrderRejectedError("On-chain settlement failed.")
            return tx_hash.hex()
            
        return order_result.get("orderID", "success")
        
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"API request failed: {e}")

def place_bet_on_market(token_id: str, market_question: str, outcome: str, wallet_address: str, private_key: str, w3: Web3) -> None:
    amount = 1.0
    bet_id = str(uuid4())
    
    try:
        tx_hash = place_market_order(token_id, "buy", amount, wallet_address, private_key, w3)
        audit_logger.info(f"BET_PLACED|{bet_id}|{market_question}|{outcome}|{amount}|{tx_hash}|SUCCESS")
        logger.info(f"✅ Bet placed successfully! tx_hash={tx_hash}")
    except Exception as e:
        audit_logger.error(f"BET_FAILED|{bet_id}|{market_question}|{outcome}|{amount}|{str(e)}")
        logger.error(f"❌ Failed to place bet: {e}")