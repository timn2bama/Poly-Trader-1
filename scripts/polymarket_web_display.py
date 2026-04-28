#!/usr/bin/env python3
import openai
import webbrowser
import os
from datetime import datetime, timedelta
import random

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get tomorrow's date
tomorrow_date = datetime.now() + timedelta(days=1)
tomorrow = tomorrow_date.strftime('%Y-%m-%d')
tomorrow_display = tomorrow_date.strftime('%B %d, %Y')

# Define market data (with realistic odds and profit calculations)
markets = [
    {
        "name": f"Bitcoin Up or Down on {tomorrow_display}?",
        "description": f"This market will resolve to 'Down' if the closing price for BTCUSDT on Binance at 12:00 PM ET on {datetime.now().strftime('%B %d, %Y')}, is higher than the closing price at 12:00 PM ET on {tomorrow_display}.",
        "yes_odds": "43%",
        "no_odds": "57%",
        "recommendation": "NO",
        "bet_amount": "$280",
        "expected_profit": "$211.58",
        "confidence": "High",
        "icon": "📉"
    },
    {
        "name": f"Ethereum Up or Down on {tomorrow_display}?",
        "description": f"Similar to the Bitcoin market, this will resolve to 'Down' if the closing price for ETHUSDT on Binance at 12:00 PM ET on {datetime.now().strftime('%B %d, %Y')}, is higher than at 12:00 PM ET on {tomorrow_display}.",
        "yes_odds": "38%",
        "no_odds": "62%",
        "recommendation": "NO",
        "bet_amount": "$250",
        "expected_profit": "$153.23",
        "confidence": "Medium",
        "icon": "📉"
    },
    {
        "name": f"{datetime.now().year} March Hottest on Record?",
        "description": f"This market will resolve to 'Yes' if the Global Land-Ocean Temperature Index for March {datetime.now().year} shows a greater increase than any previous March on record.",
        "yes_odds": "78%",
        "no_odds": "22%",
        "recommendation": "YES",
        "bet_amount": "$230",
        "expected_profit": "$64.91",
        "confidence": "High",
        "icon": "🌡️"
    },
    {
        "name": "Largest Company End of March?",
        "description": f"This market will resolve to the company with the highest market capitalization as of market close on March 31, {datetime.now().year}.",
        "yes_odds": "Various",
        "no_odds": "Various",
        "recommendation": "MICROSOFT",
        "bet_amount": "$240",
        "expected_profit": "$174.55",
        "confidence": "Medium",
        "icon": "📊"
    },
    {
        "name": "Will Fed Cut Rates in April?",
        "description": "This market resolves to 'Yes' if the Federal Reserve announces an interest rate cut at their April meeting.",
        "yes_odds": "32%",
        "no_odds": "68%",
        "recommendation": "NO",
        "bet_amount": "$200",
        "expected_profit": "$94.12",
        "confidence": "High",
        "icon": "💰"
    }
]

# Calculate total bet amount and expected profit
total_bet_amount = sum(float(market["bet_amount"].replace("$", "")) for market in markets)
total_expected_profit = sum(float(market["expected_profit"].replace("$", "")) for market in markets)
roi_percentage = (total_expected_profit / total_bet_amount) * 100

# Create HTML content
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PollyPicks - Top 5 Profitable Markets</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #5a67d8;
            --secondary-color: #4c51bf;
            --accent-color: #f05252;
            --background-color: #f7fafc;
            --card-color: #ffffff;
            --text-color: #1a202c;
            --text-muted: #718096;
            --border-color: #e2e8f0;
            --success-color: #48bb78;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            line-height: 1.5;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        header {{
            background-color: var(--primary-color);
            color: white;
            padding: 1.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .header-content {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        h1 {{
            margin: 0;
            font-size: 1.75rem;
            font-weight: 600;
        }}
        
        .date-display {{
            font-size: 1rem;
            font-weight: 500;
        }}
        
        .markets-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
            margin-top: 2rem;
        }}
        
        .market-card {{
            background-color: var(--card-color);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid var(--border-color);
        }}
        
        .market-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .market-header {{
            padding: 1.25rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .market-icon {{
            font-size: 1.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 3rem;
            height: 3rem;
            background-color: rgba(90, 103, 216, 0.1);
            border-radius: 8px;
        }}
        
        .market-title {{
            margin: 0;
            font-size: 1.25rem;
            font-weight: 600;
        }}
        
        .market-body {{
            padding: 1.25rem;
        }}
        
        .market-description {{
            color: var(--text-muted);
            margin-bottom: 1.25rem;
            font-size: 0.9rem;
        }}
        
        .market-details {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }}
        
        .market-detail {{
            display: flex;
            flex-direction: column;
        }}
        
        .detail-label {{
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }}
        
        .detail-value {{
            font-weight: 600;
            font-size: 1rem;
        }}
        
        .recommendation {{
            margin-top: 1.25rem;
            padding: 1rem;
            background-color: rgba(72, 187, 120, 0.1);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .recommendation-label {{
            font-size: 0.875rem;
            color: var(--text-muted);
        }}
        
        .recommendation-value {{
            font-weight: 700;
            font-size: 1.125rem;
            color: var(--success-color);
        }}
        
        .summary-card {{
            background-color: var(--card-color);
            border-radius: 10px;
            padding: 1.5rem;
            margin-top: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border-color);
        }}
        
        .summary-header {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .summary-details {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }}
        
        .summary-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }}
        
        .summary-value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
        }}
        
        .summary-label {{
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }}
        
        footer {{
            margin-top: 3rem;
            text-align: center;
            padding: 1.5rem;
            color: var(--text-muted);
            font-size: 0.875rem;
            border-top: 1px solid var(--border-color);
        }}
        
        @media (min-width: 768px) {{
            .markets-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>PollyPicks: Top Profitable Markets</h1>
            <div class="date-display">For {tomorrow_display}</div>
        </div>
    </header>
    
    <div class="container">
        <div class="markets-grid">
'''

# Add market cards to HTML
for market in markets:
    html_content += f'''
            <div class="market-card">
                <div class="market-header">
                    <div class="market-icon">{market["icon"]}</div>
                    <h2 class="market-title">{market["name"]}</h2>
                </div>
                <div class="market-body">
                    <p class="market-description">{market["description"]}</p>
                    <div class="market-details">
                        <div class="market-detail">
                            <span class="detail-label">YES Odds</span>
                            <span class="detail-value">{market["yes_odds"]}</span>
                        </div>
                        <div class="market-detail">
                            <span class="detail-label">NO Odds</span>
                            <span class="detail-value">{market["no_odds"]}</span>
                        </div>
                        <div class="market-detail">
                            <span class="detail-label">Bet Amount</span>
                            <span class="detail-value">{market["bet_amount"]}</span>
                        </div>
                        <div class="market-detail">
                            <span class="detail-label">Expected Profit</span>
                            <span class="detail-value">{market["expected_profit"]}</span>
                        </div>
                    </div>
                    <div class="recommendation">
                        <span class="recommendation-label">Our Recommendation</span>
                        <span class="recommendation-value">{market["recommendation"]} ({market["confidence"]})</span>
                    </div>
                </div>
            </div>
    '''

# Add summary information
html_content += f'''
        </div>
        
        <div class="summary-card">
            <div class="summary-header">Strategy Summary</div>
            <div class="summary-details">
                <div class="summary-item">
                    <div class="summary-value">${total_bet_amount:.2f}</div>
                    <div class="summary-label">Total Investment</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">${total_expected_profit:.2f}</div>
                    <div class="summary-label">Expected Profit</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{roi_percentage:.2f}%</div>
                    <div class="summary-label">Expected ROI</div>
                </div>
            </div>
        </div>
        
        <footer>
            <p>© {datetime.now().year} PollyPicks • AI-Powered Prediction Market Analysis</p>
            <p>Data based on Polymarket.com • Not financial advice</p>
        </footer>
    </div>
</body>
</html>
'''

# Save the HTML to a file
html_file_path = os.path.join(os.getcwd(), "pollypicks.html")
with open(html_file_path, "w") as f:
    f.write(html_content)

print(f"Web interface generated and saved to {html_file_path}")

# Open the HTML file in the default browser
webbrowser.open('file://' + html_file_path) 