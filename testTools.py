from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain import hub
import os
from langchain.agents import AgentExecutor, load_tools
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    ReActJsonSingleInputOutputParser,
)
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain.tools.render import render_text_description
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
import os
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_fireworks import Fireworks 

# API TOKEN
HUGGINGFACEHUB_API_TOKEN = "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"
TAVILY_API_KEY = "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"
FIREWORKS_API_KEY = "3A00naxWKfpuDASPDArEKLgrSNXWAQWGJ4m0jrWXE9LrArCt"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
os.environ["FIREWORKS_API_KEY"] = FIREWORKS_API_KEY


# Instantiates the LLM
llm = Fireworks(
    fireworks_api_key=FIREWORKS_API_KEY,
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    max_tokens=256)
llm("Name 3 sports.")

