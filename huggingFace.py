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
HUGGINGFACEHUB_API_TOKEN = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN


question = "How old is lady gaga today? "

template = """Question: {question}
Use Wikipedia as your source and quote it.
Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

llm = HuggingFaceEndpoint(
    repo_id=repo_id, max_length=128, temperature=0.5, token=HUGGINGFACEHUB_API_TOKEN
)
llm_chain = LLMChain(prompt=prompt, llm=llm)
print(llm_chain.invoke(question).get("text"))
