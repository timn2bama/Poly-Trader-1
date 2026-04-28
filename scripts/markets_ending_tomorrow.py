#!/usr/bin/env python3
import openai
from datetime import datetime, timedelta
import os

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the specific markets we want information about
markets = [
    "Bitcoin Up or Down on March 25?",
    "Ethereum Up or Down on March 25?",
    "2025 March Hottest on Record?",
    "Largest Company End of March?"
]

# Create the prompt
prompt = f"""
Please provide detailed information about the following specific Polymarket markets:

1. {markets[0]} - This market resolves to 'Down' if the closing price for BTCUSDT on Binance at 12:00 PM ET on March 24, 2025, is higher than the closing price at 12:00 PM ET on March 25, 2025.

2. {markets[1]} - Similar to the Bitcoin market, this will resolve to 'Down' if the closing price for ETHUSDT on Binance at 12:00 PM ET on March 24, 2025, is higher than at 12:00 PM ET on March 25, 2025.

3. {markets[2]} - This market will resolve to 'Yes' if the Global Land-Ocean Temperature Index for March 2025 shows a greater increase than any previous March on record.

4. {markets[3]} - This market will resolve to the company with the highest market capitalization as of market close on March 31, 2025.

For each market, provide:
1. The current YES/NO odds
2. When exactly the market resolves
3. A recommendation on which position to take
4. Your reasoning behind the recommendation

Use only data from Polymarket.com for your response.
"""

# Get markets information
result = client.chat.completions.create(
    model="gpt-4o-search-preview",
    messages=[{"role": "user", "content": prompt}],
    web_search_options={}
)

# Print results
print("POLYMARKET MARKETS ENDING SOON")
print("=" * 70)
print(result.choices[0].message.content) 