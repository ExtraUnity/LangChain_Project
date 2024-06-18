from flask import Flask, render_template
from flask import Flask, jsonify, request
from LLM.ModelExecutor import ModelExecutor
app = Flask(__name__)
modelExecutor = ModelExecutor()
@app.route("/")
def index():
    return render_template('index.html')

# This function is made by Christian
# Define a route to invoke the function
@app.route('/generate_response', methods=['GET'])
def generate_response():
    prompt = request.args.get('prompt')
    guard_rail = modelExecutor.topical_guardrail(prompt)
    if guard_rail.lower() == "allowed" or guard_rail.lower() == "allowed.":
        return jsonify(result=modelExecutor.handle_input(user_input=prompt))
    else:
        return jsonify(result="I'm sorry, but I can't help with that.")

# This function is made by Tobias
@app.route('/clear_history')
def clear():
    modelExecutor.clearMemory()
    return ""

# This function is made by Christian
@app.route('/updateAPIKey')
def update_api_key():
    apiKey = request.args.get('apiKey')
    if(apiKey==""):
        return jsonify(result="")
    if(modelExecutor.updateAPIKey(apiKey)):
        return jsonify(result=apiKey)
    else:
        return jsonify(result="Error")
