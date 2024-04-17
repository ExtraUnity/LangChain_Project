import os
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.tools import tool
from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate


######################################################
# Arithmetic Tools
######################################################
@tool
def add(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int + second_int

@tool
def subtract(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int - second_int

@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int

@tool
def divide(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int // second_int


@tool
def exponentiate(base: int, exponent: int) -> int:
    """Exponentiate the base to the exponent power."""
    return base**exponent


######################################################
# Remote API Tools (some requires API keys)
######################################################
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
def fireworks(user_input):
    print(user_input)

    # API key for fireworks AI:
    os.environ["FIREWORKS_API_KEY"] = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"
    llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)

    # Prompting:
    chat_template = ChatPromptTemplate.from_messages([
        ("system", 
         """
         Your name is Bob the Bot.
         You are a helpful AI bot that can use tools and function calling to do calculations. 
         Everytime you answer a question that requires any form of calculation, you must always use your tools and function calling to do so.
         You are only allowed to perform calculations using the tools that you have available, and this is an absolute and strict rule you must obey.
         Your very first response will start with "Hello, I am Bob the Bot. I have the following tools available: " followed by the tools that you have available. ".
         """),
        ("human", 
         user_input)
    ])

    # Agent:
    tools = [add, subtract, multiply, divide, exponentiate, get_weather_info]
    prompt = hub.pull("hwchase17/structured-chat-agent")
    agent = create_structured_chat_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    agent_io = agent_executor.invoke({"input": chat_template})

    #agent_io = agent_executor.invoke({"input": "Tell me the current weather in Denmark, Copenhagen."})
    #agent_io = agent_executor.invoke({"input": "Get me the current weather temperature from Denmark, Copenhagen, and Japan, Tokyo, and then multiply the two temperatures together."})

    #AI_response = agent_io.get("output")


    #print("User: " + agent_io.get("input"))
    return (agent_io.get("output"))