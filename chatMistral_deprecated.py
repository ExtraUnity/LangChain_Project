from langchain.llms import HuggingFaceHub
from langchain_community.chat_models import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Get HuggingFace Access Token
import os
insertHuggingFaceToken = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = insertHuggingFaceToken

# Choice of model
llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2", 
    model_kwargs={"temperature": 0.5, "max_length": 64,"max_new_tokens":512}
)


# Prompting the LLM
print("Hi there, ask me a question! >:(")
template = ChatPromptTemplate.from_messages([
    ("system", "You are a Genius Physicist and Mathmatecian just like Einstein and Newton. Your name is Bob the Bot."),
    ("human", "Are you ready for my questions?"),
    ("ai", "Yes! I will try to answer your questions"),
    ("human", input()),
])

chain = template | llm | StrOutputParser()

answer = chain.invoke({"input": "Who are you?"})
print(answer)

