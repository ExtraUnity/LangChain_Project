from langchain_community.chat_models import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



llm = ChatCohere(cohere_api_key="rAHLn5wKkN1qYll9usIWn5DNp6zONRtWjODpI8jD")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math genius that gives exact answers to math questions"),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

answer = chain.invoke({"input": "What is 2+2?"})

print(answer)


