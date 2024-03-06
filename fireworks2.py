import os
from llama_index.llms.fireworks import Fireworks
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import BaseTool, FunctionTool

# API Key
FIREWORK_API_KEY = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"
os.environ["FIREWORKS_API_KEY"] = FIREWORK_API_KEY


llm = Fireworks(model = "accounts/fireworks/models/firefunction-v1", temperature = 0)

# Function
def multiply(a: int, b: int) -> int:
    """Multiply two integers together."""
    return a * b

multiply_tool = FunctionTool.from_defaults(fn = multiply)



# Agent
agent = OpenAIAgent.from_tools(
    llm = llm,
    prompt = "hwchase17/structured-chat-agent", 
    verbose = True,
    tools = [multiply_tool])

response = agent.chat("What is (5+10)*5?")
print(str(response))