from flask import Flask, render_template
from flask import Flask, jsonify, request
from LLM.fireworks import fireworks, topical_guardrail
import os
import subprocess
import asyncio
app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')




# Define a route to invoke the function
@app.route('/invoke_python_function', methods=['GET'])
def invoke_python_function():
    prompt = request.args.get('prompt')
    llm = request.args.get('llm')
    apiKey = request.args.get('api')
    
    print(apiKey)
    guard_rail = topical_guardrail(prompt)
    if guard_rail.lower() == "allowed" or guard_rail.lower() == "allowed.":
        return jsonify(result=fireworks(prompt, apiKey))
    else:
        return jsonify(result="I'm sorry, but I can't help with that.")

