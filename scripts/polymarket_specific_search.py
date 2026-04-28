#!/usr/bin/env python3
import openai
from datetime import datetime, timedelta
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get tomorrow's date
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

# Specific query mentioning the types of markets we're looking for
query = f"""
Search Polymarket.com for active prediction markets ending tomorrow ({tomorrow}).
Specifically, check for markets like:
1. "Bitcoin Up or Down on March 25?"
2. "Ethereum Up or Down on March 25?"
3. Any markets related to temperature records for March 2025
4. Markets about company market capitalizations ending in March 2025

For each market, provide details about how they will be resolved.
"""

# Make the API call with search enabled
response = client.chat.completions.create(
    model="gpt-4o-search-preview",
    messages=[
        {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. You have web browsing capabilities to find current information about Polymarket prediction markets."},
        {"role": "user", "content": query}
    ],
    web_search_options={}
)

# Print the response
print(f"POLYMARKET MARKETS ENDING TOMORROW ({tomorrow})")
print("=" * 80)
print(response.choices[0].message.content) 