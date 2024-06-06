import os
import subprocess
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.tools import tool
from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor
from langchain.agents import AgentExecutor
from langchain.agents import AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
import numpy
import asyncio
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.huggingface import ChatHuggingFace


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
def quadraticEquation(a:float, b:float, c:float):
    """Solves a quadratic equation of form: ax²+bx+c = 0 with respect to x"""
    if a != 0:
        d = (b**2)-(4*a*c)
        if d > 0:
            x1 = ((-b) + numpy.sqrt(d))/(2*a)
            x2 = ((-b) - numpy.sqrt(d))/(2*a)
            return x1, x2
        elif d == 0:
            x = (-b)/2*a 
            return x
        else:
            raise Exception("no solutions")
    else:
        raise Exception("a cannot be 0 in quadratic equation") 

@tool
def install_oceanwave3d():
    """Builds a docker image with the OceanWave3D simulator"""
    subprocess.run(["bash", "./install_oceanwave3d.sh"])

@tool
def run_oceanwave3d_simulation():
    """Run a simulation with the OceanWave3D tool."""
    subprocess.run(["bash", "./run_simulation.sh"])

@tool
def get_weather_info(city: str, country: str):
    """Get the weather information"""
    os.environ["OPENWEATHERMAP_API_KEY"] =  "a15039154ac226a73909c312586ea4c8"
    weather = OpenWeatherMapAPIWrapper()
    weather_data = weather.run(f"{city},{country}")
    return weather_data


########################################################
# Chat history: 
########################################################
chatHistList = []


######################################################
# Setup guardrails
######################################################
def topical_guardrail(user_request):
    print("Checking topical guardrail")
    os.environ["FIREWORKS_API_KEY"] = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"
    # LLM choice from HuggingFace here:
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

    # Instantiate the LLM
    llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         """Your role is to categorise the user request into topics. 
         You can only respond in lists formatted as [topic1, topic2] etc.
         Include all topics that the request is about.
         """),
        ("user", "{user_request}")
    ])

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    topics = chain.invoke({"user_request": user_request})
    print(topics)

    prompt2 = ChatPromptTemplate.from_messages([
        ("system", """
         Your role is assess whether a list of topics are allowed. 
         You can ONLY respond with 'allowed' or 'not_allowed'. 
         The allowed topic list is [Weather, Multiplication, Simulation]. 
         If the user list does contains relevant topics, respond exactly 'allowed'. 
         If the user list contains irrelevant topics, respond exactly 'not_allowed'

         Examples:
         [Weather, Celebrity Age] -> not_allowed
         [Temperature] -> allowed
         [Weather, Age] -> not_allowed

         """),
        ("user", "{topics}")
    ])
    chain = prompt2 | llm | output_parser
    answer = chain.invoke({"topics": topics})
    print(answer)
    return answer


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


    # Agent:
    tools = [add, subtract, multiply, divide, exponentiate, squareroot, get_weather_info, quadraticEquation, run_oceanwave3d_simulation, install_oceanwave3d] 
    prompt = hub.pull("hwchase17/structured-chat-agent")
    agent = create_structured_chat_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True,
    )
    
    
    agent_io = agent_executor.invoke(
    {
        "input": user_input,
        "chat_history": chatHistList,
    }
    )
    
    # Chat history:
    result = agent_io.get("output")
    chatHistList.append(HumanMessage(user_input))
    chatHistList.append(AIMessage(result))
    print(chatHistList)
    
    return result