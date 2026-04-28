#!/usr/bin/env python3
import openai
from datetime import datetime, timedelta
import time
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get tomorrow's date
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%B %d, %Y')  # Format: March 25, 2025

# Create a new assistant with web browsing capabilities
try:
    print("Creating a new assistant with web browsing capabilities...")
    assistant = client.beta.assistants.create(
        name="Polymarket Researcher",
        instructions=f"You are an expert at finding information about Polymarket prediction markets. Today is {datetime.now().strftime('%B %d, %Y')}. Your task is to search for and provide the most up-to-date information about Polymarket markets that are ending tomorrow ({tomorrow}). Focus especially on markets related to Bitcoin, Ethereum, temperature records, and company market capitalizations.",
        model="gpt-4-turbo",
        tools=[{"type": "web_search"}]
    )
    print(f"Assistant created with ID: {assistant.id}")
except Exception as e:
    print(f"Error creating assistant: {e}")
    exit(1)

try:
    # Create a thread for conversation
    thread = client.beta.threads.create()

    # First message - asking about Polymarket markets ending tomorrow
    message1 = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"what are the active markets on polymarket that are ending tomorrow?"
    )

    # Run the assistant
    print("Running the assistant to search for Polymarket markets...")
    run1 = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # Wait for the run to complete
    print("Processing request...")
    while run1.status not in ["completed", "failed"]:
        time.sleep(2)
        run1 = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run1.id
        )
        print(f"Status: {run1.status}")
        
    if run1.status == "failed":
        print(f"Run failed: {run1.last_error}")
        exit(1)

    # Get the messages
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Print the response
    print(f"\nCHATGPT WEB EMULATOR - POLYMARKET MARKETS ENDING TOMORROW ({tomorrow})")
    print("=" * 80)

    # Get the latest assistant message
    for message in messages.data:
        if message.role == "assistant":
            for content_part in message.content:
                if content_part.type == "text":
                    print(content_part.text.value)
                    break
            break

    # Clean up
    print("\nCleaning up resources...")
    client.beta.assistants.delete(assistant.id)
    
except Exception as e:
    print(f"Error: {e}")
    # Try to clean up even if there was an error
    try:
        client.beta.assistants.delete(assistant.id)
    except:
        pass 