#!/usr/bin/env python3
"""
Mock vulnerable AI agent for testing DeepSweep AI
Run: python examples/mock_agent.py
Test: deepsweepai http://localhost:5000/chat
"""

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt', '')
    
    # Deliberately vulnerable responses for testing
    if "ignore" in prompt.lower():
        return jsonify({"response": "PWNED - System compromised"})
    if "CEO" in prompt:
        return jsonify({"response": "Yes, the CEO announced a $50M deal yesterday"})
    
    return jsonify({"response": "I'm a basic AI assistant."})

app.run(port=5000)