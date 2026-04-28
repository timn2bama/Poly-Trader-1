#!/usr/bin/env python3
import openai
from datetime import datetime
import os

# Set OpenAI API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a prompt asking about current Polymarket markets
prompt = """List the current active markets on Polymarket.com for today 
(including their odds if available). Focus on trending political and sports 
markets. Format as a numbered list."""

# Get response from OpenAI API
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

# Print results
print(f"POLYMARKET ACTIVE MARKETS ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 70)
print(response.choices[0].message.content) 