#!/usr/bin/env python3
import openai
from datetime import datetime, timedelta
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get tomorrow's date
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

# The exact query from the web interface, with slightly improved wording
query = f"what are the active markets on polymarket.com that are ending tomorrow ({tomorrow})?"

# Make the API call with search enabled
response = client.chat.completions.create(
    model="gpt-4o-search-preview",
    messages=[
        {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. You have web browsing capabilities and can search for and retrieve current information from the internet to answer questions accurately."},
        {"role": "user", "content": query}
    ],
    web_search_options={}
)

# Print the response
print(f"Query: {query}")
print(f"Tomorrow's date: {tomorrow}")
print("=" * 80)
print(response.choices[0].message.content) 