import math
import os
import matlab.engine
import subprocess
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain.pydantic_v1 import BaseModel
from langchain.tools import tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_fireworks import ChatFireworks
from pydantic import BaseModel, ValidationError
from sympy import sympify, symbols, solve, Eq

class ModelExecutor:

    def __init__(self):
        self.llm = None
        self.tools = None
        self.prompt = None
        self.agent = None
        self.memory = None 
        self.agent_executor = None
        
    def updateAPIKey(self, APIKey):
        try:
            os.environ["FIREWORKS_API_KEY"] = APIKey
            self.llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)   
            self.tools = [visualize_output,run_oceanwave3d_simulation, install_oceanwave3d, list_simulation_files, mathematics, solveEquation, get_weather_info] 
            self.prompt = hub.pull("hwchase17/structured-chat-agent")   
            self.agent = create_structured_chat_agent(self.llm, self.tools, self.prompt)
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            self.agent_executor = AgentExecutor(
                    agent=self.agent, 
                    tools=self.tools, 
                    verbose=True, 
                    handle_parsing_errors=True,
                    memory = self.memory,
                    max_iterations=100,
            )
            self.llm.invoke("test")
            return True
        except:
            return False
            
        
    def handle_input(self, user_input):
        print(user_input)
        try:
            chat_history = self.memory.buffer_as_messages
            agent_io = self.agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history,
            })
            #print("Agent:", response['output'])
            result = agent_io.get("output")

            # # Chat history:
            # result = agent_io.get("output")
            # chatHistList.append(HumanMessage(user_input))
            # chatHistList.append(AIMessage(result))
            print(chat_history)
            return result
        except Exception as e:
            print(e)
            return "An error occurred while producing your answer."
        

    def clearMemory(self):
        self.memory.clear()
        print(self.memory)

    ######################################################
    # Setup guardrails
    ######################################################
    def topical_guardrail(self, user_request):
        print("Checking topical guardrail")
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
            """Your role is to categorise the user request into topics. 
            You can only respond in lists formatted as [topic1, topic2] etc.
            Include all topics that the request is about.

            Examples:
            What's the weather in Copenhagen? -> [Weather]
            Run the OceanWave3D simulation and tell me the age of Madonna -> [Simulation, Celebrity Age]
            What can you help me with? -> [System information]
            Mathematically, what is the color of grass -> [Color, Nature]
            """),
            ("user", "{user_request}")
        ])

        output_parser = StrOutputParser()

        chain = prompt | self.llm | output_parser
        topics = chain.invoke({"user_request": user_request})
        print(topics)

        prompt2 = ChatPromptTemplate.from_messages([
            ("system", """
            Your role is assess whether a list of topics are allowed. 
            You can ONLY respond with 'allowed' or 'not_allowed'. 
            The allowed topic list is [Weather, Mathematics, Simulation, System information, Files]. 
            If the user list does contains relevant topics, respond exactly 'allowed'. 
            If the user list contains ANY  irrelevant topics, respond exactly 'not_allowed'
            Be strict in your categorization to ensure only the exact allowed topics are permitted.

            Examples:
            [Weather, Celebrity Age] -> not_allowed
            [Temperature] -> allowed
            [Weather, Age] -> not_allowed
            [Chemistry] -> not_allowed
            [Physics] -> not_allowed
            [OceanWave3D simulation] -> allowed

            """),
            ("user", "{topics}")
        ])
        chain = prompt2 | self.llm | output_parser
        try: 
            answer = chain.invoke({"topics": topics})
            print(answer)
            return answer
        except Exception as e:
            return str(e)


# Instantiate the LLM's
# fw_api_key = ""
# llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)
math_llm = ChatOpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key="4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk",
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    temperature=0.0,
)

######################################################
# Agent Tools
######################################################

# @tool
# def calculator(expression):
#     """Solves math equations"""
#     chain = LLMMathChain(llm=math_llm, verbose=False)
#     res = chain.invoke(expression)
#     return res.get("answer")

# ### Build-in math-function with inspiration from https://github.com/fw-ai/cookbook/blob/main/examples/function_calling/fireworks_langchain_tool_usage.ipynb
# class CalculatorInput(BaseModel):
#     query: str = Field(description="should be a math equation")

# class CustomCalculatorTool(BaseTool):
#     name: str = "Calculator"
#     description: str = "Solves math equations"  
#     args_schema: Type[BaseModel] = CalculatorInput

#     def _run(self, query: str) -> str:
#         """Use the tool."""
#         return LLMMathChain(llm=math_llm, verbose=True).run(query)

#     async def _arun(self, query: str) -> str:
#         """Use the tool asynchronously."""
#         raise NotImplementedError("not support async")

@tool
def change_input_file(input_file, variable, new_value):
    """Loads an input file, changes a variable to a new value and saves the file"""
    f = open(input_file)
    print(f.read())


@tool
def visualize_output():
    """Visualize output of the OceanWave3D simulation given by the input_file"""
    eng = matlab.engine.start_matlab()
    #output_path = os.path.dirname(__file__) + "../../OceanWave3D-Fortran90/docker/data"
    eng.ShowFreeSurfaceEvolution2D(nargout=0)
    return "The output has been plotted"


@tool
def mathematics(expression):
    """Evaluates a mathematical expression and outputs it in string form."""
    return sympify(expression)

@tool
def solveEquation(expression: str):
    """Solves a mathematical equation and outputs the result."""
    class SolveEquationInput(BaseModel):
        expression: str
    try:
        validated_input = SolveEquationInput(expression=expression)
    except ValidationError as e:
        return f"Invalid input: {e}"
    expression = validated_input.expression
    
    # Logic to solve the equation
    msg = "Invalid input: please check syntax, are any operation signs missing?"    
    try:
        if "=" in expression:
                lhs_str, rhs_str = expression.split("=")
                lhs = sympify(lhs_str)
                rhs = sympify(rhs_str)
                equation = Eq(lhs, rhs)
                return solve(equation, symbols('x'))
        else:
                equation = sympify(expression)
                return solve(equation, symbols('x'))        
    except: return msg


@tool
def quadraticEquation(a:float, b:float, c:float):
    """Solves a quadratic equation of form: ax²+bx+c = 0 with respect to x"""
    if a != 0:
        d = (b**2)-(4*a*c)
        if d > 0:
            x1 = ((-b) + math.sqrt(d))/(2*a)
            x2 = ((-b) - math.sqrt(d))/(2*a)
            return x1, x2
        elif d == 0:
            x = (-b)/2*a 
            return x
        else:
            return "no solutions"
    else:
        return "a cannot be 0 in quadratic equation"


# @tool
# def calculator(expression):
#     """Solves math equations"""
#     chain = LLMMathChain(llm=math_llm, verbose=False)
#     res = chain.invoke(expression)
#     return res.get("answer")

# # Build-in math-function with inspiration from:
# # https://github.com/fw-ai/cookbook/blob/main/examples/function_calling/fireworks_langchain_tool_usage.ipynb
# class CalculatorInput(BaseModel):
#     query: str = Field(description="should be a math equation")

# class CustomCalculatorTool(BaseTool):
#     name: str = "Calculator"
#     description: str = "Solves math equations"  
#     args_schema: Type[BaseModel] = CalculatorInput

#     def _run(self, query: str) -> str:
#         """Use the tool."""
#         return LLMMathChain(llm=math_llm, verbose=True).run(query)

#     async def _arun(self, query: str) -> str:
#         """Use the tool asynchronously."""
#         raise NotImplementedError("not support async")

@tool
def install_oceanwave3d():
    """Builds a docker image with the OceanWave3D simulator"""
    try:
        res = subprocess.run(["bash", "./install_oceanwave3d.sh"], capture_output=True)
        if res.stdout == None or res.stdout.decode() == "":
            return res.stderr.decode()
        return res.stderr.decode()#"Sucessfully installed the OceanWave3D program"
    except Exception as e:
        return str(e)

@tool
def run_oceanwave3d_simulation(input_file):
    """Run a simulation with the OceanWave3D tool."""
    try:
        res = subprocess.run(["bash", "./run_simulation.sh", input_file], capture_output=True)
        if res.stdout == None or res.stdout.decode() == "":
            return res.stderr.decode()
        return res.stdout.decode()
    except Exception as e:
        return str(e)

@tool
def list_simulation_files():
    """Lists all valid INPUT files for the OceanWave3D simulation"""
    try:
        res = subprocess.run(["bash", "./list_inputfiles.sh"], capture_output=True)
        if res.stdout == None or res.stdout.decode() == "":
            return res.stderr.decode()
        return res.stdout.decode()
    except Exception as e:
        return str(e)
        

@tool
def get_weather_info(city: str, country: str):
    """Get the weather information"""
    os.environ["OPENWEATHERMAP_API_KEY"] =  "a15039154ac226a73909c312586ea4c8"
    weather = OpenWeatherMapAPIWrapper()
    weather_data = weather.run(f"{city},{country}")
    return weather_data




########################################################
# Chat history: 
########################################################
#chatHistList = []
# chat_messages = ConversationBufferMemory()
# current_chat_history = ConversationSummaryBufferMemory(max_token_limit=)
# conversation = ConversationChain(memory=current_chat_history,llm=llm,verbose=True)


######################################################
# The agent setup
######################################################

# Prompt that allows us to add memory to both the AgentExecutor and the chat itself. 
# Source: https://github.com/ThreeRiversAINexus/sample-langchain-agents/blob/main/structured_chat.py#L13
# prompt = ChatPromptTemplate.from_messages([
#     ("system", """
#      Respond to the human as helpfully and accurately as possible. You have access to the following tools:

#     {tools}

#     Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

#     Valid "action" values: "Final Answer" or {tool_names}

#     Provide only ONE action per $JSON_BLOB, as shown:

#     ```
#     {{
#     "action": $TOOL_NAME,
#     "action_input": $INPUT
#     }}
#     ```

#     Follow this format:

#     Question: input question to answer
#     Thought: consider previous and subsequent steps
#     Action:
#     ```
#     $JSON_BLOB
#     ```
#     Observation: action result
#     ... (repeat Thought/Action/Observation N times)
#     Thought: I know what to respond
#     Action:
#     ```
#     {{
#     "action": "Final Answer",
#     "action_input": "Final response to human"
#     }}

#     Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation
#      """),
#     MessagesPlaceholder("chat_history", optional=True),
#     ("human", """
#     {input}
#     {agent_scratchpad}
#     (reminder to respond in a JSON blob no matter what)
#      """),
# ])
