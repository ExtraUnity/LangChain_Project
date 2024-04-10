from flask import Flask, render_template
from flask import Flask, jsonify, request
#from LLM.fireworksFunctionCalling import * 

app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')



# Your Python function
def fetchAIResponse():
    # Do something here

    return "Hello from Python"

# Define a route to invoke the function
@app.route('/invoke_python_function', methods=['GET'])
def invoke_python_function():
    result = fetchAIResponse()
    return jsonify(result=result)