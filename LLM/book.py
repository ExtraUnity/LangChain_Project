import os
from langchain.llms import HuggingFaceHub
from langchain.agents import (
    AgentExecutor, AgentType, initialize_agent, load_tools
)

def load_agent() -> AgentExecutor:
        llm = HuggingFaceHub (
                model_kwargs={"temperature": 0.5, "max_length": 64},
                repo_id="google/flan-t5-xxl"
        )
        tools = load_tools(
                tool_names=["wikipedia"],
                llm=llm
        )
        return initialize_agent(
                tools=tools, llm=llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True, handle_parsing_errors=True,
        )

HUGGINGFACEHUB_API_TOKEN = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
print("ready to load agent")
chain = load_agent()
print("agent loaded")
prompt = "When was Madonna born?"
response = chain.run(prompt)
print(response)