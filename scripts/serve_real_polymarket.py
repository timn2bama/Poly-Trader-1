#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import os
import datetime
from generate_html import generate_html
from fetch_polymarket_data import fetch_polymarket_data

app = Flask(__name__)

@app.route('/')
def home():
    """Generate and serve the real-time Polymarket data HTML page"""
    # Generate the HTML with real data
    html_content = generate_html()
    return html_content

@app.route('/data')
def data():
    """API endpoint to get the raw data as JSON"""
    data = fetch_polymarket_data()
    return jsonify(data)

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat interaction with the AI analyst"""
    user_message = request.json.get('message', '')
    
    # In a real implementation, this would send the user's query to an AI model
    # and return the response. For now, we'll return a simple acknowledgment.
    
    response = {
        "status": "success",
        "message": f"Your question about '{user_message}' has been received. Our AI analyst would normally respond here with detailed market analysis based on your query.",
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    return jsonify(response)

if __name__ == "__main__":
    # Use a different port to avoid conflicts
    port = 5001
    print(f"Starting server on http://127.0.0.1:{port}")
    app.run(debug=True, port=port) 