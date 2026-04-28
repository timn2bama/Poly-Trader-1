#!/usr/bin/env python3
import openai
from datetime import datetime
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get profitable markets ending soon with betting recommendations
result = client.chat.completions.create(
    model="gpt-4o-search-preview",
    messages=[{"role": "user", "content": """Visit Polymarket.com and analyze:
    1. Find the top 10 most potentially profitable markets that are ending within the next 24 hours
    2. For each market, list: market name, current odds, ending time, and your recommendation on which outcome to bet on
    3. Recommend how much to bet on each market in USD (assume a $1000 total budget)
    4. Calculate expected profit for each bet and total expected profit
    5. Focus on markets with clear mispricing or high potential returns
    """}],
    web_search_options={}
)

# Print results
print(f"POLYMARKET PROFIT OPPORTUNITIES ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 70)
print(result.choices[0].message.content) 