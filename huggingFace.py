from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from getpass import getpass
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

from langchain.schema import (
    HumanMessage,
    SystemMessage,
)

# API-TOKENS from https://huggingface.co/settings/tokens
HUGGINGFACEHUB_API_TOKEN = "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"
TAVILY_API_KEY = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY


# LLM choice from HuggingFace here:
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

# Instantiates the LLM
llm = HuggingFaceEndpoint(
    repo_id=repo_id, max_length=128, temperature=0.5, token=HUGGINGFACEHUB_API_TOKEN
)

# Template and prompting
template = """Question: {question}
Your name is Bob the Bot.
Use Wikipedia as your source and quote it.
Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)


# LLM Chain output

# chain = prompt | llm | StrOutputParser()
# answer = chain.invoke({question})
# print(answer)

chain = LLMChain(prompt=prompt, llm=llm)

print("Hi I am Bob the bot, please ask your question >:)")
user_input = input()
print(chain.invoke(user_input).get("text"))

print("----------------------------------------------")
#tools[0].invoke({"query": "What happened during 2020 in the context of pandemics?"})