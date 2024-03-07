import os
from llama_index.llms.fireworks import Fireworks
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import BaseTool, FunctionTool
import numpy

# --------------------------------------------------------- #
# Guide is based on this link: https://docs.llamaindex.ai/en/stable/examples/llm/fireworks_cookbook.html 
# --------------------------------------------------------- #


# Get the API-key from Fireworks AI website (https://fireworks.ai/)
FIREWORK_API_KEY = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"
os.environ["FIREWORKS_API_KEY"] = FIREWORK_API_KEY

# Instantiate the LLM
llm = Fireworks(model = "accounts/fireworks/models/firefunction-v1", temperature = 0)



# --------------------------------------------------------- #
# Step 1) Add new functions/tool
# --------------------------------------------------------- #
def multiply(a: int, b: int) -> int:
    """Multiply two integers together."""
    return a * b


def add(a: int, b: int) -> int:
    """Square an integer once with exponent of 2"""
    return a+b


# --------------------------------------------------------- #
# Step 2) Form a tool from the function and add it to the toolbox
# --------------------------------------------------------- #
multiply_tool = FunctionTool.from_defaults(fn = multiply)
add_tool = FunctionTool.from_defaults(fn = add)

toolbox = [multiply_tool, add_tool]

# --------------------------------------------------------- #
# Step 3) Construct an agent and add the toolbox at the parameter "tools" 
# --------------------------------------------------------- #
agent = OpenAIAgent.from_tools(
    llm = llm,
    prompt = "hwchase17/structured-chat-agent", 
    verbose = True,
    tools = toolbox)


# Note: If the agent is using function calling, it will be clear since "=== Calling Function ===" will be printed out.
response = agent.chat("What is 5*(5+5)?")
print(str(response))
print("___________________________________________")

response = agent.chat("What is (5*5)+5?")
print(str(response))
print("___________________________________________")



# Note2: When doing arithmetic expression, paranthesis is important, for instance "5*5+5" will not result in function calling
response = agent.chat("What is 5*5+5?")
print(str(response))
