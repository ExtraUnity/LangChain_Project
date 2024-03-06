import os
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser


# Note that the docstrings here are crucial, as they will be passed along
# to the model along with the class name.
class Multiply(BaseModel):
    """Multiply two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

def multiply(a: int, b: int) -> int:
    """Multiply two integers together.

    Args:
        a: First integer
        b: Second integer
    """
    return a * b

# os.environ["OPENAI_API_KEY"] = "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"
os.environ["FIREWORKS_API_KEY"] = "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk"

from langchain_fireworks import ChatFireworks

llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)
llm_with_tools = llm.bind_tools([multiply], tool_choice="multiply")
tool_chain = llm_with_tools | JsonOutputToolsParser()
print(tool_chain.invoke("what's 3 * 12"))