#!/usr/bin/env python3
from datetime import datetime

# Define the markets that end tomorrow
markets = [
    {
        "name": "Bitcoin Up or Down on March 25?",
        "description": "This market will resolve to 'Down' if the closing price for BTCUSDT on Binance at 12:00 PM ET on March 24, 2025, is higher than the closing price at 12:00 PM ET on March 25, 2025.",
        "tags": "Polymarket +1"
    },
    {
        "name": "Ethereum Up or Down on March 25?",
        "description": "Similar to the Bitcoin market, this will resolve to 'Down' if the closing price for ETHUSDT on Binance at 12:00 PM ET on March 24, 2025, is higher than at 12:00 PM ET on March 25, 2025.",
        "tags": "Polymarket +1"
    },
    {
        "name": "2025 March Hottest on Record?",
        "description": "This market will resolve to 'Yes' if the Global Land-Ocean Temperature Index for March 2025 shows a greater increase than any previous March on record.",
        "tags": "Polymarket +3"
    },
    {
        "name": "Largest Company End of March?",
        "description": "This market will resolve to the company with the highest market capitalization as of market close on March 31, 2025.",
        "tags": "Polymarket +3"
    }
]

# Print the markets
print(f"As of March 24, 2025, here are some active Polymarket prediction markets scheduled to conclude on March 25, 2025:")
print()

for market in markets:
    print(f"{market['name']}")
    print(f"{market['description']}")
    print(f"{market['tags']}")
    print() 