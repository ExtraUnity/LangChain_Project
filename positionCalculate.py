import os
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain.agents import tool
from langchain_fireworks import ChatFireworks
from langchain import hub

from langchain.agents import AgentExecutor, create_structured_chat_agent

os.environ["FIREWORKS_API_KEY"] = "axrEA0ZczeX9IcCPEodSwYfPrYKKMiaYtjwhaHb89mkXhQ7I"
llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)


# Note that the docstrings here are crucial, as they will be passed along
# to the model along with the class name.
from langchain.agents import tool


@tool
def position(time: int, velocity: int) -> int:
    """Returns the position when given velocity and a time in seconds"""
    return time * velocity
@tool
def velocity(time: int, acceleration:int) -> int:
    """Returns the velocity given an acceleration and a time in seconds"""
    return time * acceleration

prompt = hub.pull("hwchase17/structured-chat-agent")

tools=[position, velocity]

agent = create_structured_chat_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

agent_executor.invoke({"input": "given a car with an acceleration of 2 what would be the cars position after 5 seconds"})
