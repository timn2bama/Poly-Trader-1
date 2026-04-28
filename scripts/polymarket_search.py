#!/usr/bin/env python3
import openai
from datetime import datetime
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a completion using the search model
try:
    completion = client.chat.completions.create(
        model="gpt-4o-search-preview",
        messages=[
            {
                "role": "user", 
                "content": """
                Search Polymarket.com and tell me:
                1. What are the current top 10 trending markets on Polymarket.com?
                2. For each market, provide the market name, current YES/NO odds or prices, and resolution date if available.
                3. Focus especially on US election markets, sports markets, and celebrity markets.
                4. Format as a numbered list with clearly stated odds as percentages.
                """
            }
        ],
        web_search_options={}
    )
    
    # Print results
    print(f"POLYMARKET ACTIVE MARKETS ({datetime.now().strftime('%Y-%m-%d')})")
    print("=" * 70)
    print(completion.choices[0].message.content)
    
except Exception as e:
    print(f"Error: {e}") 