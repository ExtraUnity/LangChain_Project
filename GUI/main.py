from flask import Flask, render_template
from flask import Flask, jsonify, request
from LLM.fireworks import fireworks
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
    print(prompt)
    return jsonify(result=fireworks(prompt, apiKey))

