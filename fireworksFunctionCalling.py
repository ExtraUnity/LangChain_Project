import os
from langchain import hub
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.tools import tool
@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int

@tool
def add(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int + second_int

@tool
def exponentiate(base: int, exponent: int) -> int:
    "Exponentiate the base to the exponent power."
    return base**exponent

# os.environ["OPENAI_API_KEY"] = "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"
os.environ["FIREWORKS_API_KEY"] = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"

from langchain_fireworks import ChatFireworks
llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)


# Chains
llm_with_tools = llm.bind_tools([multiply], tool_choice={"type": "function", "function": {"name": "multiply"}})
tool_chain = (
    llm_with_tools 
    | JsonOutputKeyToolsParser(key_name="multiply", first_tool_only=True) 
    | multiply 
)
print(tool_chain.invoke("what's 3 * 12"))


# Agent
tools = [multiply, add, exponentiate]
prompt = hub.pull("hwchase17/structured-chat-agent")
agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
print(agent_executor.invoke({"input": "Take 3 to the fifth power and multiply that by the sum of twelve and three. Finally square the result"}))