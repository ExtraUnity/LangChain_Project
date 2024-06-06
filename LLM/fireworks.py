import os
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.tools import tool
from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate
import numpy

from langchain.chains import LLMMathChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import Optional, Type


math_llm = ChatOpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key="4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk",
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    temperature=0.0,
)


def mathSymbolsToWords(s: str) -> str:
    temp = ""
    #temp = s.replace("**", " to the power of ").replace("+", " plus ").replace("-", " minus ").replace("/", " devided by ").replace("*", " multiplied by ")
    for i in range(0, len(s)-1):
        if s[i] == "%2B":
            temp += " plus "
        elif s[i] == '-':
            temp += " minus "
        elif s[i] == '/':
            temp += " divided by "
        elif s[i] == '*':
            if i+1 < len(s)-1 and s[i+1] == '*':
                temp += " to the power of "
            else: 
                temp += " multiplied by "   
        else: 
            temp += s[i]
    
    return temp
######################################################
# Agent Tools
######################################################

# @tool
# def add(first_int: int, second_int: int) -> int:
#     """Adds two integers together."""
#     return first_int + second_int

# @tool
# def subtract(first_int: int, second_int: int) -> int:
#     """Subtracts two integers together."""
#     return first_int - second_int

# @tool
# def multiply(first_int: int, second_int: int) -> int:
#     """Multiply two integers together."""
#     return first_int * second_int

# @tool
# def divide(first_int: int, second_int: int) -> int:
#     """Divides two integers together."""
#     return first_int // second_int

# @tool
# def exponentiate(base: int, exponent: int) -> int:
#     """Exponentiate the base to the exponent power."""
#     return base**exponent

# @tool
# def squareroot(integer: int) -> int:
#     """Takes the square root of an integer"""
#     return numpy.sqrt(integer)

# @tool
# def quadraticEquation(a:float, b:float, c:float):
#     """Solves a quadratic equation of form: ax²+bx+c = 0 with respect to x"""
#     if a != 0:
#         d = (b**2)-(4*a*c)
#         if d > 0:
#             x1 = ((-b) + numpy.sqrt(d))/(2*a)
#             x2 = ((-b) - numpy.sqrt(d))/(2*a)
#             return x1, x2
#         elif d == 0:
#             x = (-b)/2*a 
#             return x
#         else:
#             raise Exception("no solutions")
#     else:
#         raise Exception("a cannot be 0 in quadratic equation") 

@tool
def mathSymbolsToWordsTool(s: str) -> str:
    """As the first action, if given a mathematical expression, replacing mathematical symbols with written words of the equivalent symbol"""
    temp = ""
    #temp = s.replace("**", " to the power of ").replace("+", " plus ").replace("-", " minus ").replace("/", " devided by ").replace("*", " multiplied by ")
    for i in range(0, len(s)-1):
        if s[i] == '+':
            temp += " plus "
        elif s[i] == '-':
            temp += " minus "
        elif s[i] == '/':
            temp += " divided by "
        elif s[i] == '*':
            if s[i+1] == '*':
                temp += " to the power of "
            else: 
                temp += " multiplied by "   
        else: 
            temp += s[i]
    
    return temp

class CalculatorInput(BaseModel):
    query: str = Field(description="should be a mathematical expression")

class CustomCalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = "Tool to evaluate mathemetical expressions"
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, query: str) -> str:
        """Use the tool."""
        return LLMMathChain(llm=math_llm, verbose=True).run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("not support async")



@tool
def get_weather_info(city: str, country: str):
    """Get the weather information"""
    os.environ["OPENWEATHERMAP_API_KEY"] =  "a15039154ac226a73909c312586ea4c8"
    weather = OpenWeatherMapAPIWrapper()
    weather_data = weather.run(f"{city},{country}")
    return weather_data

######################################################
# The LLM setup
######################################################
def fireworks(user_input, APIKey):
    user_input = mathSymbolsToWords(user_input)
    print(user_input)
    
    print(APIKey)

    # API key for fireworks AI:
    if(APIKey == "") :
        os.environ["FIREWORKS_API_KEY"] = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"
    else :
        os.environ["FIREWORKS_API_KEY"] = APIKey

    llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)
    # math_llm = ChatFireworks(model="accounts/fireworks/models/mixtral-8x7b-instruct", temperature=0)
    # Prompting:
    chat_template = ChatPromptTemplate.from_messages([
        ("system", 
         """
         You are a helpful AI chat bot named Bob who can use tools and function calling to do calculations. 
         Every time you answer a question that requires any form of calculation, you must always use your tools to do so. 
         You must follow the rule which states that you are only allowed to perform calculations using the provided tools. 
         If you break the rule, it could be harmful to humans and cause irreversible damage. 
         For example, you are allowed to calculate what 2 + 2 is, since you have the addition tool in your toolbox. 
         You are also allowed to give information about the current weather, since you have the getWeatherInfo tool. 
         But you are not allowed to perform calculations on division, since you do not have the tools to do so. 
         If you are not able to perform a calculation due to lack of tools, you will inform the user of this and not perform the calculation.
         """),
        ("human", 
         user_input)
    ])

    # Agent:
    # tools = [add, subtract, multiply, divide, exponentiate, squareroot, get_weather_info, quadraticEquation] 
    tools = [mathSymbolsToWordsTool, CustomCalculatorTool(), get_weather_info] 
    prompt = hub.pull("hwchase17/structured-chat-agent")
    agent = create_structured_chat_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True,
    )
    
    
    agent_io = agent_executor.invoke({"input": user_input})
    #agent_io = agent_executor.invoke({"input": "Tell me the current weather in Denmark, Copenhagen."})
    #agent_io = agent_executor.invoke({"input": "Get me the current weather temperature from Denmark, Copenhagen, and Japan, Tokyo, and then multiply the two temperatures together."})
    result = agent_io.get("output")
    
    # Can you solve this quadratic equation: 2*x^2 + 6*x + 4 = 0
    
    # # NOTE: Hvis man bruger chat_template, så virker flere tools ikke på én gang, da det forstyrrer dens process?
    # test= agent_executor.invoke(
    #     {
    #         "input": chat_template,    
    #         "chat_history": [
    #         HumanMessage(content=user_input),
            
    #         ]
    #     }
    # )
    # testResult = test.get("output")
    
    return result