#!/usr/.env/bin/env python3
from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from markupsafe import escape
import openai
from datetime import datetime, timedelta
import logging

from config import settings
from models import MarketData, MarketDataResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = settings.flask_secret_key.get_secret_value()

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Initialize OpenAI client
try:
    if settings.openai_api_key:
        client = openai.OpenAI(api_key=settings.openai_api_key.get_secret_value())
        logger.info("OpenAI client initialized successfully")
    else:
        logger.warning("OPENAI_API_KEY is not set.")
        client = None
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {str(e)}")
    client = None

def get_market_data() -> dict:
    # Get tomorrow's date
    tomorrow_date = datetime.now() + timedelta(days=1)
    tomorrow_display = tomorrow_date.strftime('%B %d, %Y')
    
    # Define mock market data with sanitized strings
    raw_markets = [
        {
            "name": escape(f"Bitcoin Up or Down on {tomorrow_display}?"),
            "description": escape(f"This market will resolve to 'Down' if the closing price for BTCUSDT on Binance at 12:00 PM ET on {datetime.now().strftime('%B %d, %Y')}, is higher than the closing price at 12:00 PM ET on {tomorrow_display}."),
            "yes_odds": "43%",
            "no_odds": "57%",
            "recommendation": "NO",
            "bet_amount": "$280",
            "expected_profit": "$211.58",
            "confidence": "High",
            "icon": "📉"
        },
        {
            "name": escape(f"Ethereum Up or Down on {tomorrow_display}?"),
            "description": escape(f"Similar to the Bitcoin market, this will resolve to 'Down' if the closing price for ETHUSDT on Binance at 12:00 PM ET on {datetime.now().strftime('%B %d, %Y')}, is higher than at 12:00 PM ET on {tomorrow_display}."),
            "yes_odds": "38%",
            "no_odds": "62%",
            "recommendation": "NO",
            "bet_amount": "$250",
            "expected_profit": "$153.23",
            "confidence": "Medium",
            "icon": "📉"
        }
    ]
    
    # Validate through Pydantic
    validated_markets = []
    for m in raw_markets:
        try:
            validated = MarketData(**m)
            validated_markets.append(validated)
        except Exception as e:
            logger.error(f"Market validation error: {e}")
            
    total_bet_amount = sum(float(market.bet_amount.replace("$", "")) for market in validated_markets)
    total_expected_profit = sum(float(market.expected_profit.replace("$", "")) for market in validated_markets)
    roi_percentage = (total_expected_profit / total_bet_amount) * 100 if total_bet_amount > 0 else 0
    
    response = MarketDataResponse(
        markets=validated_markets,
        tomorrow_display=tomorrow_display,
        total_bet_amount=total_bet_amount,
        total_expected_profit=total_expected_profit,
        roi_percentage=roi_percentage,
        current_year=datetime.now().year,
        data_source="mock"
    )
    
    return response.model_dump()

@app.route('/')
def home():
    # Get market data
    data = get_market_data()
    return render_template('index.html', **data)

@app.route('/api/markets')
@limiter.limit("10 per minute")
def api_markets():
    """API endpoint to get market data as JSON"""
    data = get_market_data()
    return jsonify(data)

@app.route('/setup')
def setup():
    """Page to guide users through setup process"""
    missing_vars = []
    if not settings.openai_api_key: missing_vars.append("OPENAI_API_KEY")
    if not settings.polygon_wallet_private_key: missing_vars.append("POLYGON_WALLET_PRIVATE_KEY")
    return render_template('setup.html', missing_vars=missing_vars)

@app.route('/troubleshooting')
def troubleshooting():
    """Page with troubleshooting information"""
    return render_template('troubleshooting.html', current_year=datetime.now().year)

if __name__ == '__main__':
    debug_mode = settings.flask_debug
    if settings.is_production() and debug_mode:
        logger.error("Debug mode disabled in production!")
        debug_mode = False
        
    print(f"Starting PollyPicks Flask app on port {settings.flask_port}...")
    app.run(
        debug=debug_mode, 
        port=settings.flask_port,
        host="127.0.0.1" if debug_mode else "0.0.0.0"
    )