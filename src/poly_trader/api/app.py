#!/usr/.env/bin/env python3
import functools
import logging
from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from markupsafe import escape

from poly_trader.config import settings
from poly_trader.models import MarketData, MarketDataResponse
from poly_trader.data.fetcher import fetch_polymarket_data
from poly_trader.data.db import SessionLocal, Trade

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

# ---------------------------------------------------------------------------
# Issue 4: API key authentication decorator
# ---------------------------------------------------------------------------
def require_api_key(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key') or request.args.get('api_key')
        expected = settings.flask_secret_key.get_secret_value()
        if not key or key != expected:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated


def get_recent_trades():
    """Fetch recent trades from the database"""
    db = SessionLocal()
    try:
        trades = db.query(Trade).order_by(Trade.timestamp.desc()).limit(10).all()
        return trades
    except Exception as e:
        logger.error(f"Error fetching trades: {e}")
        return []
    finally:
        db.close()

@app.route('/')
def home():
    # Get real market data from CLOB
    data = fetch_polymarket_data()

    # Get recent trades
    trades = get_recent_trades()

    # Get tomorrow's date for display
    tomorrow_date = datetime.now() + timedelta(days=1)
    tomorrow_display = tomorrow_date.strftime('%B %d, %Y')

    return render_template(
        'index.html',
        **data,
        trades=trades,
        tomorrow_display=tomorrow_display,
        current_year=datetime.now().year,
    )

@app.route('/api/markets')
@limiter.limit("10 per minute")
@require_api_key  # Issue 4: protect market data endpoint
def api_markets():
    """API endpoint to get market data as JSON"""
    data = fetch_polymarket_data()
    return jsonify(data)

@app.route('/api/trades')
@require_api_key  # Issue 4: protect trade history endpoint
def api_trades():
    """API endpoint to get trade history as JSON"""
    trades = get_recent_trades()
    return jsonify([{
        "id": t.id,
        "question": t.question,
        "side": t.side,
        "outcome": t.outcome,
        "price": t.price,
        "size": t.size,
        "status": t.status,
        "timestamp": t.timestamp.isoformat(),
    } for t in trades])

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

    print(f"Starting PolyTrader Flask app on port {settings.flask_port}...")
    app.run(
        debug=debug_mode,
        port=settings.flask_port,
        host="127.0.0.1" if debug_mode else "0.0.0.0",
    )
