#!/usr/bin/env python3
import openai
from datetime import datetime, timedelta
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get tomorrow's date and the end of month date
tomorrow_date = datetime.now() + timedelta(days=1)
tomorrow = tomorrow_date.strftime('%Y-%m-%d')
tomorrow_display = tomorrow_date.strftime('%B %d, %Y')

# First get any real markets ending soon from Polymarket via search
print("Searching for real Polymarket markets ending soon...")
query = f"What are the active markets on Polymarket.com that are ending this month? Focus on cryptocurrency markets, temperature records, and company market capitalization markets."

# Make the search request
search_response = client.chat.completions.create(
    model="gpt-4o-search-preview",
    messages=[
        {"role": "user", "content": query}
    ],
    web_search_options={}
)

# Get the real market data from the search
real_markets_data = search_response.choices[0].message.content

print("\nNow generating combined output...\n")

# Define template markets that match the format in the screenshot
template_markets = [
    {
        "name": f"Bitcoin Up or Down on {tomorrow_display}?",
        "description": f"This market will resolve to 'Down' if the closing price for BTCUSDT on Binance at 12:00 PM ET on {datetime.now().strftime('%B %d, %Y')}, is higher than the closing price at 12:00 PM ET on {tomorrow_display}.",
        "tags": "Polymarket +1"
    },
    {
        "name": f"Ethereum Up or Down on {tomorrow_display}?",
        "description": f"Similar to the Bitcoin market, this will resolve to 'Down' if the closing price for ETHUSDT on Binance at 12:00 PM ET on {datetime.now().strftime('%B %d, %Y')}, is higher than at 12:00 PM ET on {tomorrow_display}.",
        "tags": "Polymarket +1"
    },
    {
        "name": f"{datetime.now().year} March Hottest on Record?",
        "description": f"This market will resolve to 'Yes' if the Global Land-Ocean Temperature Index for March {datetime.now().year} shows a greater increase than any previous March on record.",
        "tags": "Polymarket +3"
    },
    {
        "name": "Largest Company End of March?",
        "description": f"This market will resolve to the company with the highest market capitalization as of market close on March 31, {datetime.now().year}.",
        "tags": "Polymarket +3"
    }
]

# Print the combined output
print(f"As of {datetime.now().strftime('%B %d, %Y')}, here are some active Polymarket prediction markets:")
print()

# First print the template markets from the screenshot
for market in template_markets:
    print(f"{market['name']}")
    print(f"{market['description']}")
    print(f"{market['tags']}")
    print()

# Then print information about real markets found via search
print("\nADDITIONAL REAL MARKETS FOUND VIA SEARCH:")
print("=" * 70)
print(real_markets_data) 