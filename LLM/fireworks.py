import os
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.tools import tool
from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import GoogleSearchAPIWrapper
import numpy


######################################################
# Agent Tools
######################################################
@tool
def add(first_int: int, second_int: int) -> int:
    """Adds two integers together."""
    return first_int + second_int

@tool
def subtract(first_int: int, second_int: int) -> int:
    """Subtracts two integers together."""
    return first_int - second_int

@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int

@tool
def divide(first_int: int, second_int: int) -> int:
    """Divides two integers together."""
    return first_int // second_int

@tool
def exponentiate(base: int, exponent: int) -> int:
    """Exponentiate the base to the exponent power."""
    return base**exponent

@tool
def squareroot(integer: int) -> int:
    """Takes the square root of an integer"""
    return numpy.sqrt(integer)

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
    print(user_input)
    
    print(APIKey)

    # API key for fireworks AI:
    if(APIKey == "") :
        os.environ["FIREWORKS_API_KEY"] = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"
    else :
        os.environ["FIREWORKS_API_KEY"] = APIKey

    llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)

    # Prompting:
    chat_template = ChatPromptTemplate.from_messages([
        ("system", 
         """
         You are a helpful AI bot named Bob who can use tools and function calling to do calculations. 
         Everytime you answer a question that requires any form of calculation, you must always use your tools to do so.
         You are only allowed to perform calculations using the tools, since it is harmful for humans if you break this rule.
         """),
        ("human", 
         user_input)
    ])

    # Agent:
    tools = [add, subtract, multiply, divide, exponentiate, squareroot, get_weather_info] 
    prompt = hub.pull("hwchase17/structured-chat-agent")
    agent = create_structured_chat_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True,
    )
    

    agent_io = agent_executor.invoke({"input": chat_template})
    
    test= agent_executor.invoke(
        {
            "input": chat_template,    
            "chat_history": [
            HumanMessage(content=user_input),
            
            ]
        }
    )



    #agent_io = agent_executor.invoke({"input": "Tell me the current weather in Denmark, Copenhagen."})
    #agent_io = agent_executor.invoke({"input": "Get me the current weather temperature from Denmark, Copenhagen, and Japan, Tokyo, and then multiply the two temperatures together."})


    return (agent_io.get("output"))