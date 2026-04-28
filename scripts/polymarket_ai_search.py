#!/usr/bin/env python3
import openai
from datetime import datetime
import time
import sys
import os

# Set OpenAI API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create an assistant with web browsing capabilities
assistant = client.beta.assistants.create(
    name="Polymarket Researcher",
    instructions="Search for the current active markets on Polymarket.com. Focus on trending political and sports markets. Format as a numbered list with odds for each market.",
    model="gpt-4-turbo",
    tools=[{"type": "web_search"}]
)

# Create a thread
thread = client.beta.threads.create()

# Add a message to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="List the current trending markets on Polymarket.com including odds. Focus on political and sports markets."
)

# Run the assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Wait for the run to complete
while run.status != "completed":
    time.sleep(2)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"Run status: {run.status}")
    if run.status == "failed":
        print("Run failed")
        break

# Get the messages
messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

# Print the latest assistant response
print(f"\nPOLYMARKET ACTIVE MARKETS ({datetime.now().strftime('%Y-%m-%d')})")
print("=" * 70)
for message in messages.data:
    if message.role == "assistant":
        for content in message.content:
            if content.type == "text":
                print(content.text.value)

# Clean up
client.beta.assistants.delete(assistant.id) 