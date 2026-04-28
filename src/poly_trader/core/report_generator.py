#!/usr/bin/env python3
from poly_trader.data.fetcher import fetch_polymarket_data
import datetime

def generate_html():
    """Generate HTML using real Polymarket data"""
    # Get the data
    data = fetch_polymarket_data()
    markets = data["markets"]
    total_bet_amount = data["total_bet_amount"]
    total_expected_profit = data["total_expected_profit"]
    roi_percentage = data["roi_percentage"]
    
    # Get current date for display
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    
    # Generate the HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PollyPicks: Top 5 Polymarket Opportunities</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #6366f1;
            --primary-dark: #4f46e5;
            --secondary-color: #10b981;
            --accent-color: #f97316;
            --background-color: #f8fafc;
            --card-color: #ffffff;
            --text-color: #1e293b;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.5;
        }}
        
        .container {{
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        header {{
            background: linear-gradient(to right, var(--primary-color), var(--primary-dark));
            color: white;
            padding: 1.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .header-content {{
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.75rem;
            font-weight: 700;
        }}
        
        .date-display {{
            font-size: 1rem;
            font-weight: 500;
            padding: 0.5rem 1rem;
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 9999px;
        }}
        
        .section-header {{
            font-size: 1.5rem;
            font-weight: 700;
            margin: 2rem 0 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--primary-dark);
        }}
        
        .markets-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }}
        
        .market-card {{
            background-color: var(--card-color);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid var(--border-color);
        }}
        
        .market-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
        }}
        
        .market-header {{
            padding: 1.5rem;
            background: linear-gradient(to right, #f1f5f9, #ffffff);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .market-icon {{
            font-size: 1.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 3.5rem;
            height: 3.5rem;
            background-color: rgba(99, 102, 241, 0.1);
            border-radius: 10px;
            flex-shrink: 0;
        }}
        
        .market-title-wrapper {{
            flex: 1;
        }}
        
        .market-rank {{
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--primary-color);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .market-rank span {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.5rem;
            height: 1.5rem;
            background-color: var(--primary-color);
            color: white;
            border-radius: 999px;
            font-size: 0.75rem;
        }}
        
        .market-title {{
            margin: 0;
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-color);
        }}
        
        .confidence-badge {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.9rem;
            font-weight: 700;
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            background-color: #dcfce7;
            color: #166534;
            white-space: nowrap;
        }}
        
        .market-body {{
            padding: 1.5rem;
        }}
        
        .market-description {{
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
            padding: 0 1.5rem;
            padding-top: 1.5rem;
        }}
        
        .market-details {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            padding: 0 1.5rem;
        }}
        
        .market-detail {{
            display: flex;
            flex-direction: column;
        }}
        
        .detail-label {{
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }}
        
        .detail-value {{
            font-weight: 600;
            font-size: 1.1rem;
            color: var(--text-color);
        }}
        
        .recommendation {{
            margin: 1.5rem;
            padding: 1.25rem;
            background-color: #f8fafc;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border: 1px dashed var(--border-color);
        }}
        
        .recommendation-info {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .recommendation-label {{
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 500;
        }}
        
        .recommendation-value {{
            font-weight: 800;
            font-size: 1.5rem;
            color: var(--success-color);
        }}
        
        .bet-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.25rem;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: background-color 0.2s;
            text-decoration: none;
        }}
        
        .bet-button:hover {{
            background-color: var(--primary-dark);
        }}
        
        .summary-card {{
            background-color: var(--card-color);
            border-radius: 12px;
            padding: 2rem;
            margin-top: 2.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid var(--border-color);
        }}
        
        .summary-header {{
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--primary-dark);
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
            padding: 1.25rem;
            background-color: #f8fafc;
            border-radius: 10px;
        }}
        
        .summary-value {{
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }}
        
        .summary-label {{
            font-size: 0.9rem;
            color: var(--text-muted);
            font-weight: 500;
        }}
        
        .chat-prompt {{
            background-color: var(--card-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid var(--border-color);
            text-align: center;
        }}
        
        .chat-title {{
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--primary-dark);
        }}
        
        .chat-description {{
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
        }}
        
        .chat-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.2s;
        }}
        
        .chat-button:hover {{
            background-color: var(--primary-dark);
        }}
        
        @media (min-width: 768px) {{
            .markets-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (min-width: 1024px) {{
            .markets-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        footer {{
            text-align: center;
            padding: 2rem 0;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div class="logo">
                <span>🔮</span>
                PollyPicks
            </div>
            <div class="date-display">Updated: {current_date}</div>
        </div>
    </header>
    
    <div class="container">
        <div class="section-header">
            <span>🔥 TOP 5 HIGHEST-PROFIT OPPORTUNITIES</span>
        </div>
        
        <div class="markets-grid">
"""
    
    # Add market cards
    for i, market in enumerate(markets):
        rank_labels = ["TOP PICK", "HIGH YIELD", "HIGH CONFIDENCE", "TRENDING", "UNDERVALUED"]
        
        html += f"""
            <!-- Market {i+1} -->
            <div class="market-card">
                <div class="market-header">
                    <div class="market-icon">{market['icon']}</div>
                    <div class="market-title-wrapper">
                        <div class="market-rank"><span>{i+1}</span> {rank_labels[i]}</div>
                        <h2 class="market-title">{market['name']}</h2>
                    </div>
                    <div class="confidence-badge">
                        <span>⭐</span>
                        {market['confidence']}
                    </div>
                </div>
                <div class="market-body">
                    <p class="market-description">{market['description']}</p>
                    
                    <div class="market-details">
                        <div class="market-detail">
                            <span class="detail-label">YES Odds</span>
                            <span class="detail-value">{market['yes_odds']}</span>
                        </div>
                        <div class="market-detail">
                            <span class="detail-label">NO Odds</span>
                            <span class="detail-value">{market['no_odds']}</span>
                        </div>
                        <div class="market-detail">
                            <span class="detail-label">Bet Amount</span>
                            <span class="detail-value">{market['bet_amount']}</span>
                        </div>
                        <div class="market-detail">
                            <span class="detail-label">Expected Profit</span>
                            <span class="detail-value">{market['expected_profit']}</span>
                        </div>
                    </div>
                    
                    <div class="recommendation">
                        <div class="recommendation-info">
                            <span class="recommendation-label">RECOMMENDED POSITION</span>
                            <span class="recommendation-value">{market['recommendation']}</span>
                        </div>
                        <a href="{market['url']}" target="_blank" class="bet-button">
                            Place Bet Now
                            <span>→</span>
                        </a>
                    </div>
                </div>
            </div>
"""
    
    # Add summary and chat sections
    html += f"""
        </div>
        
        <div class="summary-card">
            <div class="summary-header">PORTFOLIO SUMMARY</div>
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
                    <div class="summary-value">{roi_percentage}%</div>
                    <div class="summary-label">Expected ROI</div>
                </div>
            </div>
        </div>
        
        <div class="chat-prompt">
            <div class="chat-title">Need More Analysis?</div>
            <p class="chat-description">Chat with our AI analyst for deeper insights on these markets or to find custom opportunities tailored to your preferences.</p>
            <button class="chat-button">
                <span>💬</span>
                Chat with PollyPicks AI
            </button>
        </div>
    </div>
    
    <footer>
        <p>PollyPicks © {datetime.datetime.now().year} | Real-time prediction market analytics</p>
        <p><small>Not financial advice. Always do your own research before placing bets.</small></p>
    </footer>
</body>
</html>
"""
    
    # Save the HTML to a file
    with open("real_top5_picks.html", "w") as f:
        f.write(html)
    
    return html

if __name__ == "__main__":
    generate_html()
    print("HTML generated and saved to real_top5_picks.html") 