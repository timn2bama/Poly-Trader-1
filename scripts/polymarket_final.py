#!/usr/bin/env python3
import openai
from datetime import datetime, timedelta
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get tomorrow's date
tomorrow_date = datetime.now() + timedelta(days=1)
tomorrow = tomorrow_date.strftime('%Y-%m-%d')
tomorrow_display = tomorrow_date.strftime('%B %d, %Y')

# Create a very specific and detailed query
query = f"""
Visit Polymarket.com now and find all active markets that are scheduled to end on {tomorrow_display}.

Specifically look for these markets that I saw earlier today:
1. "Bitcoin Up or Down on {tomorrow_display}?"
2. "Ethereum Up or Down on {tomorrow_display}?"
3. "{tomorrow_date.year} March Hottest on Record?"
4. "Largest Company End of March?"

For each market, I need to know:
- The exact market question
- How the market will be resolved (the specific criteria)
- When exactly the market will end/resolve

Format your response exactly like this example:
```
MARKET: Bitcoin Up or Down on {tomorrow_display}?
DESCRIPTION: This market will resolve to 'Down' if the closing price for BTCUSDT on Binance at 12:00 PM ET on March 24, 2025, is higher than the closing price at 12:00 PM ET on {tomorrow_display}.
```

If these specific markets don't exist, please search carefully for any markets that resolve on {tomorrow_display} or the day after.
"""

# Make the request
response = client.chat.completions.create(
    model="gpt-4o-search-preview",
    messages=[
        {
            "role": "system", 
            "content": f"You are a highly accurate research assistant specialized in prediction markets. Today is {datetime.now().strftime('%B %d, %Y')}. Your task is to search the web for specific Polymarket prediction markets ending on {tomorrow_display}. Be extremely precise and thorough in your search."
        },
        {"role": "user", "content": query}
    ],
    web_search_options={}
)

# Print the response
print(f"POLYMARKET MARKETS ENDING ON {tomorrow_display}")
print("=" * 80)
print(response.choices[0].message.content) 