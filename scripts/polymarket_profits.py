#!/usr/bin/env python3
import openai
from datetime import datetime
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get profitable markets with detailed betting strategy
result = client.chat.completions.create(
    model="gpt-4o-search-preview",
    messages=[{"role": "user", "content": """Visit Polymarket.com right now and research the CURRENT real markets. Create a detailed, actionable betting strategy:

1. Find 5 SPECIFIC markets currently trading on Polymarket that have high potential ROI
2. For each market:
   - List the EXACT market name
   - Provide the CURRENT odds in percentages (YES/NO prices)
   - Recommend which position to take (YES/NO) based on your research
   - Suggest a specific amount to bet from a $1000 total budget
   - Calculate potential profit in dollars
   - Estimate your confidence level and expected value

3. Create a simple, compact summary table with:
   [Market Name | Position | Bet Amount | Expected Profit]

4. Calculate total expected profit across all bets and ROI percentage

Focus on REAL markets currently available on Polymarket.com with exact numbers and calculations.
Use a maximum of 250 words for your response to ensure all information fits in the output.
"""}],
    max_tokens=1000,
    web_search_options={}
)

# Print results
print(f"POLYMARKET BETTING STRATEGY ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 80)
print(result.choices[0].message.content) 