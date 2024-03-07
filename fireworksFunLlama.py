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


def quadraticEQ(a: int, b: int, c: int):
    """Solve for x in the quadratic equation ax^2 + bx + c = 0"""
    d = (numpy.square(b)) - (4*a*c)
    if (d > 0) : 
        print(f"discrimant is positive: d = {d}. Two solutions")
        return (-b + numpy.sqrt(d))/(2*a), (-b - numpy.sqrt(d))/(2*a)
    elif (d == 0):
        print(f"discrimant is zero: d = {d}. One solution")
        return -b/(2*a)
    else: 
        print(f"discrimant is negative: d = {d}. No real solutions")
        return 

# --------------------------------------------------------- #
# Step 2) Form a tool from the function and add it to the toolbox
# --------------------------------------------------------- #
multiply_tool = FunctionTool.from_defaults(fn = multiply)
add_tool = FunctionTool.from_defaults(fn = add)
quadraticEQ_tool = FunctionTool.from_defaults(fn = quadraticEQ)

toolbox = [multiply_tool, add_tool, quadraticEQ_tool]

# --------------------------------------------------------- #
# Step 3) Construct an agent and add the toolbox at the parameter "tools" 
# --------------------------------------------------------- #
agent = OpenAIAgent.from_tools(
    llm = llm,
    prompt = "hwchase17/structured-chat-agent", 
    verbose = True,
    tools = toolbox)



# --------------------------------------------------------- #
# Step 4) Test the agent with different tools
# --------------------------------------------------------- #

# Note1: If the agent is using function calling, it will be clear since "=== Calling Function ===" will be printed out.

# TEST 1: Using the add_tool and multiply_tool

# response = agent.chat("What is 5*(5+5)?")
# print(str(response))
# print("___________________________________________")

# response = agent.chat("What is (5*5)+5?")
# print(str(response))
# print("___________________________________________")

# Observations: 
#   Doing Arithmetic expression, paranthesis is important, for instance "5*5+5" will not result in function calling


# TEST 3: Using the quadraticEQ_tool
response = agent.chat("What is x in this quadratic equation 2*x^2 + 2*x = 0?")  
print(str(response))
print("___________________________________________")

# Example where result is a decimal
response = agent.chat("What is x in this quadratic equation 2*x^2 + 3*x = 0?")  
print(str(response))
print("___________________________________________")

# Observartions: 
#   The quadratic equation format seems to work best when including all operators explicit (include "*" for multiplication)
