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
        
    print(f"Starting PolyTrader via run.py on port {settings.flask_port}...")
    app.run(
        debug=debug_mode, 
        port=settings.flask_port,
        host="127.0.0.1" if debug_mode else "0.0.0.0"
    )
