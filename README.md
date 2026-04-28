# PolyTrader: AI-Powered Automated Trading System for Polymarket

An autonomous AI trading agent for Polymarket that identifies market inefficiencies, calculates optimal bet sizes, and executes trades automatically. This system leverages ChatGPT's predictive capabilities against existing market odds to find profitable edges.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ installed
- A Polygon network wallet with MATIC (for gas) and USDC (for trading)
- API keys for OpenAI and SerpAPI
- Basic understanding of prediction markets and crypto wallets

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/PolyTrader.git
cd PolyTrader
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Run the application
```bash
python run.py
```

6. Visit http://127.0.0.1:5001 in your browser (default port)

## 📋 Features

* **Market Analysis:** Continuously scans Polymarket for opportunities
* **AI-Powered Predictions:** Uses ChatGPT to analyze various events
* **Edge Detection:** Compares AI predictions with market consensus to find inefficiencies
* **Intelligent Bet Sizing:** Implements Kelly Criterion for optimal bankroll management
* **Automated Execution:** Places trades via Polymarket CLOB API
* **Risk Management:** Includes safety features to protect your bankroll

## 🏗️ Architecture

The system is organized into a modular package structure under `src/poly_trader`:

1. **API Module (`poly_trader.api`)**  
   * Flask web interface for monitoring and manual control
   * REST endpoints for market data

2. **Core Module (`poly_trader.core`)**  
   * `betting.py`: Automated bet execution and transaction signing
   * `report_generator.py`: Generates static performance reports

3. **Data Module (`poly_trader.data`)**  
   * `fetcher.py`: Retrieves market data from Polymarket and external sources

4. **Utility Scripts (`scripts/`)**
   * Collection of experimental and one-off utility scripts for market analysis

## ⚙️ Configuration

Edit your `.env` file with the following variables:

```
# OpenAI API key (required for AI functionality)
OPENAI_API_KEY=your_openai_api_key_here

# Flask app settings
FLASK_SECRET_KEY=your_flask_secret_key_here
FLASK_PORT=5001

# SerpAPI key (required for market data)
SERPAPI_API_KEY=your_serpapi_api_key_here

# Polymarket API credentials
POLYMARKET_API_KEY=your_polymarket_api_key_here

# Wallet information (required for transactions)
POLYGON_WALLET_PRIVATE_KEY=your_private_key_here
POLYMARKET_WALLET_ADDRESS=your_wallet_address_here

# Trading settings
INITIAL_BANKROLL=1000
MAX_BET_PERCENTAGE=0.05
MIN_EDGE_PERCENTAGE=0.15
```

> ⚠️ **IMPORTANT**: Never commit your `.env` file or hardcode API keys in the source code. The `.env` file is included in `.gitignore` to prevent accidental exposure of your credentials.

## 🚀 Usage

Start the web interface:
```bash
python run.py
```

Run tests:
```bash
python -m pytest
```

Generate a top picks report:
```bash
python -m poly_trader.core.report_generator
```

## ⚠️ Risk Warning

Trading involves substantial risk and is not suitable for all investors. Past performance is not indicative of future results. Start with small amounts to test the system before scaling up. Implement proper risk management.

## 🔍 Package Structure

* `src/poly_trader/api/app.py` - Main entry point for the Flask application
* `src/poly_trader/core/betting.py` - Automated bet execution
* `src/poly_trader/data/fetcher.py` - Real-time market data retrieval
* `src/poly_trader/models.py` - Pydantic data models
* `src/poly_trader/config.py` - Configuration management

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Siraj Raval

## 🙏 Acknowledgements

* OpenAI for ChatGPT API
* Polymarket team for the CLOB API
* All contributors and testers

---

⭐ Star this repo if you find it useful! Join our Discord community to discuss improvements and share results.

**Note:** This system is for educational purposes. Always do your own research before trading.
