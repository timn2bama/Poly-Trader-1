#!/usr/bin/env python3
import openai
from datetime import datetime, timedelta
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the specific markets we're interested in
specific_markets = """
1. Bitcoin Up or Down on March 25? - This market resolves to 'Down' if the closing price for BTCUSDT on Binance at 12:00 PM ET on March 24, 2025, is higher than the closing price at 12:00 PM ET on March 25, 2025.

2. Ethereum Up or Down on March 25? - Similar to the Bitcoin market, this will resolve to 'Down' if the closing price for ETHUSDT on Binance at 12:00 PM ET on March 24, 2025, is higher than at 12:00 PM ET on March 25, 2025.

3. 2025 March Hottest on Record? - This market will resolve to 'Yes' if the Global Land-Ocean Temperature Index for March 2025 shows a greater increase than any previous March on record.

4. Largest Company End of March? - This market will resolve to the company with the highest market capitalization as of market close on March 31, 2025.
"""

# Create the prompt for the OpenAI API
prompt = f"""
Search for the current odds on Polymarket.com for the following specific markets:

{specific_markets}

For each market, provide:
1. Current YES/NO odds (percentages)
2. When the market resolves
3. A recommendation on which side to bet on
4. How much to bet (from a $1000 total budget)
5. Expected profit calculation
6. Brief reasoning for the recommendation

Format your response as a clear betting strategy with a summary of total expected profit and ROI.
"""

# Get markets information
result = client.chat.completions.create(
    model="gpt-4o-search-preview",
    messages=[{"role": "user", "content": prompt}],
    web_search_options={}
)

# Print results
print(f"BETTING STRATEGY FOR POLYMARKET MARKETS ENDING TOMORROW ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 80)
print(result.choices[0].message.content) 