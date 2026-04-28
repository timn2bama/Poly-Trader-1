import logging
from py_clob_client.client import ClobClient
from poly_trader.config import settings

logger = logging.getLogger(__name__)

def get_clob_client() -> ClobClient:
    """
    Initialize and return a Polymarket CLOB Client.
    Requires POLYGON_WALLET_PRIVATE_KEY in settings.
    """
    private_key_secret = settings.polygon_wallet_private_key
    if not private_key_secret:
        logger.error("POLYGON_WALLET_PRIVATE_KEY not found in settings.")
        raise ValueError("Missing private key for CLOB client initialization.")
    
    private_key = private_key_secret.get_secret_value()
    # Ensure '0x' prefix is NOT present for the client (based on script observations)
    if private_key.startswith('0x'):
        private_key = private_key[2:]
        
    try:
        # Initialize the CLOB client
        # Host for Polygon: https://clob.polymarket.com
        # Chain ID for Polygon: 137
        client = ClobClient(
            host="https://clob.polymarket.com",
            key=private_key,
            chain_id=137
        )
        
        # Generate or derive API credentials
        api_creds = client.create_or_derive_api_creds()
        client.set_api_creds(api_creds)
        
        return client
    except Exception as e:
        logger.error(f"Failed to initialize CLOB client: {str(e)}")
        raise
