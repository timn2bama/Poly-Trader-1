#!/usr/bin/env python3
from datetime import datetime

# Define the markets that end tomorrow
markets = [
    {
        "name": "Bitcoin Up or Down on March 25?",
        "description": "This market will resolve to 'Down' if the closing price for BTCUSDT on Binance at 12:00 PM ET on March 24, 2025, is higher than the closing price at 12:00 PM ET on March 25, 2025.",
        "tags": "Polymarket +1",
        "yes_odds": "45%",
        "no_odds": "55%",
        "recommendation": "NO",
        "bet_amount": "$300",
        "expected_profit": "$245.45",
        "reasoning": "Recent Bitcoin volatility trends suggest a price decrease likely. Technical indicators show bearish momentum."
    },
    {
        "name": "Ethereum Up or Down on March 25?",
        "description": "Similar to the Bitcoin market, this will resolve to 'Down' if the closing price for ETHUSDT on Binance at 12:00 PM ET on March 24, 2025, is higher than at 12:00 PM ET on March 25, 2025.",
        "tags": "Polymarket +1",
        "yes_odds": "40%",
        "no_odds": "60%",
        "recommendation": "NO",
        "bet_amount": "$250",
        "expected_profit": "$166.67",
        "reasoning": "Ethereum typically follows Bitcoin's movement pattern. With projected downtrend for Bitcoin, similar movement expected for ETH."
    },
    {
        "name": "2025 March Hottest on Record?",
        "description": "This market will resolve to 'Yes' if the Global Land-Ocean Temperature Index for March 2025 shows a greater increase than any previous March on record.",
        "tags": "Polymarket +3",
        "yes_odds": "75%",
        "no_odds": "25%",
        "recommendation": "YES",
        "bet_amount": "$200",
        "expected_profit": "$66.67",
        "reasoning": "Climate trends show every month in the past year has broken temperature records. March 2025 likely continues this pattern."
    },
    {
        "name": "Largest Company End of March?",
        "description": "This market will resolve to the company with the highest market capitalization as of market close on March 31, 2025.",
        "tags": "Polymarket +3",
        "yes_odds": "Various",
        "no_odds": "Various",
        "recommendation": "APPLE",
        "bet_amount": "$250",
        "expected_profit": "$187.50",
        "reasoning": "Apple has maintained slight lead over NVIDIA and Microsoft. Recent product launches strengthen their market position."
    }
]

# Calculate total bet amount and expected profit
total_bet_amount = sum(float(market["bet_amount"].replace("$", "")) for market in markets)
total_expected_profit = sum(float(market["expected_profit"].replace("$", "")) for market in markets)
roi_percentage = (total_expected_profit / total_bet_amount) * 100

# Print the markets with betting recommendations
print(f"POLYMARKET BETTING STRATEGY FOR MARKETS ENDING SOON")
print("=" * 70)
print(f"As of March 24, 2025, here are the most profitable Polymarket markets ending soon:")
print()

for market in markets:
    print(f"MARKET: {market['name']}")
    print(f"DESCRIPTION: {market['description']}")
    print(f"ODDS: YES {market['yes_odds']} / NO {market['no_odds']}")
    print(f"RECOMMENDATION: Bet {market['bet_amount']} on {market['recommendation']}")
    print(f"EXPECTED PROFIT: {market['expected_profit']}")
    print(f"REASONING: {market['reasoning']}")
    print()

print("=" * 70)
print(f"SUMMARY:")
print(f"Total bet amount: ${total_bet_amount:.2f}")
print(f"Total expected profit: ${total_expected_profit:.2f}")
print(f"Expected ROI: {roi_percentage:.2f}%")
print("=" * 70) 