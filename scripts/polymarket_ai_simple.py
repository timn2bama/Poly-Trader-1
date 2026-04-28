#!/usr/bin/env python3
import openai
from datetime import datetime
import os

# Set OpenAI API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a prompt asking about current Polymarket markets
prompt = """Based on your most recent knowledge, list the current popular markets on Polymarket.com.
Include political markets like presidential elections and sports betting markets.
For each market, include:
1. The market question
2. The current odds or probability
3. The expected resolution date

Format as a numbered list of at least 10 markets. If you don't have current information,
provide the most recent markets you're aware of and clearly note that the information might
be outdated."""

# Get response from OpenAI API
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

# Print results
print(f"POLYMARKET ACTIVE MARKETS ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 70)
print(response.choices[0].message.content) 