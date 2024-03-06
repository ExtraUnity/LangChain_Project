import os
import openai
import json
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser



# API Key
client = openai.OpenAI(
    base_url = "https://api.fireworks.ai/inference/v1", 
    api_key = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"
)

# Class
class Result(BaseModel):
    winner: str


# Prompting the LLM 
print("Please ask your question")
question = input()

messages = [
    {"role": "system", "content": f"""
     Your name is Bob the Bot.
     You will only reply in one JSON."""},
    
    {"role": "user", "content": question}
]



# Combines the message prompt and tools
chat_completion = client.chat.completions.create(
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    response_format={"type": "json_object", "schema": Result.schema_json()},
    messages=messages,
    #tools=tools,
    temperature=0.1
)


# Result
print(repr(chat_completion.choices[0].message.content))




