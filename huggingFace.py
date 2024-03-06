from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from getpass import getpass
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)

# API-TOKEN from https://huggingface.co/settings/tokens
HUGGINGFACEHUB_API_TOKEN = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

# LLM choice from HuggingFace here:
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

# Instantiate the LLM
llm = HuggingFaceEndpoint(
    repo_id=repo_id, max_length=128, temperature=0.5, token=HUGGINGFACEHUB_API_TOKEN
)

chat_model = ChatHuggingFace(llm=llm)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math genius that gives exact answers to math questions"),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

answer = chain.invoke({"input": "What is 2+2*4?"})

print(answer)
