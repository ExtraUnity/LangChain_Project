import os
import subprocess
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.tools import tool
from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate

from langchain.chains import LLMMathChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import Optional, Type

from langchain_core.messages import HumanMessage, AIMessage
import numpy
import asyncio
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.huggingface import ChatHuggingFace


math_llm = ChatOpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key="4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk",
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    temperature=0.0,
)

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

def clearMemory():
    print(chatHistList)
    chatHistList.clear()

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
    # user_input = mathSymbolsToWords(user_input)
    print(user_input)
    
    print(APIKey)

    # API key for fireworks AI:
    if(APIKey == "") :
        os.environ["FIREWORKS_API_KEY"] = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"
    else :
        os.environ["FIREWORKS_API_KEY"] = APIKey

    llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)


    # Agent:
    tools = [CustomCalculatorTool(), get_weather_info, run_oceanwave3d_simulation, install_oceanwave3d] 
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