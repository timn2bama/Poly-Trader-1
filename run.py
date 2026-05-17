#!/usr/bin/env python3
import sys
import os

# Add src to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from poly_trader.api.app import app, settings

if __name__ == "__main__":
    debug_mode = settings.flask_debug
    if settings.is_production() and debug_mode:
        debug_mode = False

    # Railway injects PORT; fall back to config for local dev
    port = int(os.environ.get("PORT", settings.flask_port))
    print(f"Starting PolyTrader via run.py on port {port}...")
    app.run(debug=debug_mode, port=port, host="0.0.0.0")
