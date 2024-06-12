from flask import Flask, render_template
from flask import Flask, jsonify, request
from LLM.fireworks import ModelExecutor
app = Flask(__name__)
modelExecutor = ModelExecutor()
@app.route("/")
def index():
    return render_template('index.html')


# Define a route to invoke the function
@app.route('/generate_response', methods=['GET'])
def generate_response():
    prompt = request.args.get('prompt')
    llm = request.args.get('llm')
    apiKey = request.args.get('api')
    
    print(apiKey)
    guard_rail = modelExecutor.topical_guardrail(prompt)
    if guard_rail.lower() == "allowed" or guard_rail.lower() == "allowed.":
        return jsonify(result=modelExecutor.handle_input(user_input=prompt, APIKey=apiKey))
    else:
        return jsonify(result="I'm sorry, but I can't help with that.")


@app.route('/clear_history')
def clear():
    modelExecutor.clearMemory()
    return ""