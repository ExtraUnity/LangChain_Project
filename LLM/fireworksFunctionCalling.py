import os
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.tools import tool
from langchain_fireworks import ChatFireworks

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

# Test of remote API-integrated tools - works :)
@tool
def get_weather_info(city: str, country: str):
    """Get the weather information"""
    os.environ["OPENWEATHERMAP_API_KEY"] =  "a15039154ac226a73909c312586ea4c8"
    weather = OpenWeatherMapAPIWrapper()
    weather_data = weather.run(f"{city},{country}")
    return weather_data


# os.environ["OPENAI_API_KEY"] = "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"
os.environ["FIREWORKS_API_KEY"] = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"
llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)


#Chains
# llm_with_tools = llm.bind_tools([multiply], tool_choice={"type": "function", "function": {"name": "multiply"}})
# tool_chain = (
#     llm_with_tools 
#     | JsonOutputKeyToolsParser(key_name="multiply", first_tool_only=True) 
#     | multiply 
# )
# print(tool_chain.invoke("what's 3 * 12"))


# Agent
tools = [multiply, add, exponentiate, get_weather_info]
prompt = hub.pull("hwchase17/structured-chat-agent")
agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

agent_io = agent_executor.invoke({"input": "Take 3 to the fifth power and multiply that by the sum of twelve and three. Finally square the result"})
#agent_io = agent_executor.invoke({"input": "Tell me the current weather in Denmark, Copenhagen."})
#agent_io = agent_executor.invoke({"input": "Get me the current weather temperature from Denmark, Copenhagen, and Japan, Tokyo, and then multiply the two temperatures together."})

AI_response = agent_io.get("output")


print("User: " + agent_io.get("input"))
print("AI:" + agent_io.get("output"))