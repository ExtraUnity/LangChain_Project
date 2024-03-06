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
tool_add = {
        "type": "function",
        "function": {
            "name": "add",
            "parameters": {
                "type": "object",
                "properties": {
                    "first_int": {
                        "type": "integer"
                    },
                    "second_int": {
                        "type": "integer", 
                    }
                },
                "required": ["first_int", "second_int"],
            },
        },
    }

def add(first_int: int, second_int: int) -> int:
    print("called")
    return first_int + second_int



# Prompting the LLM 
print("Please ask your question")
question = input()

messages = [
    {"role": "system", "content": f"You are a helpful assistant with access to functions."},
    {"role": "user", "content": question}
]

tools = [tool_add]


# Combines the message prompt and tools
chat_completion = client.chat.completions.create(
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    messages=messages,
    tools=tools,
    temperature=0.1
)





# Result
# print(repr(chat_completion.choices[0].message.content))
print(chat_completion.choices[0].message.model_dump_json(indent=4))



