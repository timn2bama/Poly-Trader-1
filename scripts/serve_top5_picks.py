#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Serve the Top 5 Picks HTML page"""
    # Check if the file exists
    if os.path.exists("top5_picks.html"):
        with open("top5_picks.html", "r") as f:
            html_content = f.read()
        return html_content
    else:
        return "Error: top5_picks.html file not found"

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat interaction with the AI analyst"""
    user_message = request.json.get('message', '')
    
    # In a real implementation, this would send the user's query to an AI model
    # and return the response. For now, we'll return a simple acknowledgment.
    
    response = {
        "status": "success",
        "message": f"Your question about '{user_message}' has been received. Our AI analyst would normally respond here with detailed market analysis based on your query.",
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000) 