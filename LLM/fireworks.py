import math
import re
import os
from typing import Type
import matlab.engine
import subprocess
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain.pydantic_v1 import BaseModel
from langchain.tools import tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool, BaseTool
from langchain_openai import ChatOpenAI
from langchain_fireworks import ChatFireworks
from pydantic import BaseModel, Field, ValidationError
from sympy import *

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
            self.tools = [visualize_output,run_oceanwave3d_simulation, install_oceanwave3d, ChangeInputFileTool(metadata={'llm': self.llm}), list_simulation_files, mathematics, solveEquation, get_weather_info] 
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
        except Exception as e:
            print(e)
            return False
            
        
    def handle_input(self, user_input):
        try:
            chat_history = self.memory.buffer_as_messages
            agent_io = self.agent_executor.invoke({
                "input": user_input + ". Use your tools, dont just answer and use action_input!",
                "chat_history": chat_history,
            })
            result = agent_io.get("output")
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
            List your tools -> [System information]
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
            The allowed topic list is [Weather, Mathematics, Simulation, Installation, System information, Files]. 
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

######################################################
# Agent Tools
######################################################

def find_index(search_string, string_list):
    for i, s in enumerate(string_list):
        if search_string in s:
            return i
    return -1  # return -1 if the string is not found

class ChangeInputFileInput(BaseModel):
    input_file: str = Field(description="Should be a file name")
    variable: str = Field(description="Variable name")
    new_value: str = Field(description="Should be a number")

class ChangeInputFileTool(BaseTool):
    name: str = "change_input_file"
    description: str = "Loads an input file, changes a variable to a new value and saves the file"
    args_schema: Type[BaseModel] = ChangeInputFileInput
    
    def _run(self, input_file, variable, new_value):
        """Use the tool."""
        # Load the file
        curdir = os.path.dirname(os.path.abspath(__file__))
        pardir = os.path.join(curdir, os.pardir)
        file_path = os.path.join(pardir, "OceanWave3D-Fortran90", "examples", "inputfiles", input_file)
        with open(file_path, 'r') as file:
            # Read lines from the input file
            lines = file.readlines()

        # Prompt for LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
            """Your role is to take a piece of text replace the value of {variable} with {new_value}. Ignore everything in parenthesis. 
            Return ONLY the output text with the change made.
            Do not write any thoughts. Do not prefix the result with anything. Do not postfix the result with anything. ONLY the exact result!
            The output should be the same format as the input, only the one value should be changed.

            Example 1:
            replace c with 5: '1 2 3 4 <- a, b, c, d' => "1 2 5 4 <- a, b, c, d"
            
            Example 2:
            replace StoreDataOnOff with 40 '80  20 1 1 <- StoreDataOnOff, formattype, (StoreDataOnOff=0 -> no output, StoreDataOnOff=+stride-> binary, StoreDataOnOff=-stride -> ascii every stride time steps.  formattype=0, binary; =1, unformatted) If formattype=20, then the line should read: StoreDataOnOff, iKinematics, formattype, nOutFiles; and nOutFiles lines should appear below defining  [xbeg, xend, xstride, ybeg, yend, ystride, tbeg, tend, tstride] for each file.'
            => "40  20 1 1 <- StoreDataOnOff, formattype, (StoreDataOnOff=0 -> no output, StoreDataOnOff=+stride-> binary, StoreDataOnOff=-stride -> ascii every stride time steps.  formattype=0, binary; =1, unformatted) If formattype=20, then the line should read: StoreDataOnOff, iKinematics, formattype, nOutFiles; and nOutFiles lines should appear below defining  [xbeg, xend, xstride, ybeg, yend, ystride, tbeg, tend, tstride] for each file."
            """),
            ("user", "replace {variable} with {new_value}: '{input}'")
        ])

        output_parser = StrOutputParser()
        chain = prompt | self.metadata['llm'] | output_parser
        
        with open(file_path, 'w') as file:
            for line in lines:
                if variable in line:
                    try:
                        lhs, rhs = line.split('<-')
                        rhsTrim = re.sub(r'\(.*?\)', '', rhs)
                        #rhsTrim = re.split(r',\s*(?![^()]*\))', rhs)
                        rhsTrim = list(filter(None, re.split('[; ,]', rhsTrim)))
                        #rhsTrim = rhsTrim.split()
                        lhsTrim = lhs.split()
                        lhsTrim[find_index(variable, rhsTrim)] = new_value
                        line = ' '.join(lhsTrim) + '    <- ' + rhs
                        print(line)
                    except:
                        print(line)
                    # newLine = chain.invoke({
                    #     "input": line,
                    #     "variable": variable,
                    #     "new_value": new_value
                    # })
                    # print(line)
                    # print(newLine)
                    # line = newLine
                if "\n" not in line:
                    line += "\n"
                file.write(line)
        return "File has been updated."



@tool
def visualize_output():
    """Visualize output of the OceanWave3D simulation given by the input_file"""
    eng = matlab.engine.start_matlab()
    #output_path = os.path.dirname(__file__) + "../../OceanWave3D-Fortran90/docker/data"
    eng.ShowFreeSurfaceEvolution2D(nargout=0)
    return "Final answer: The output has been plotted"


@tool
def mathematics(expression):
    """Evaluates a mathematical arithmetic expression and outputs it in string form."""
    return sympify(expression)

@tool
def solveEquation(expression: str):
    """Solves a mathematical equation and outputs the result."""
    class SolveEquationInput(BaseModel):
        expression: str
    try:
        validated_input = SolveEquationInput(expression=expression)
    except: ValidationError("Invalid input, please check syntax, are any operation signs missing?")
    expression = validated_input.expression
    
    # Logic to solve the equation
    msg = "Error: Invalid input, please check syntax, are any operation signs missing? For example \"2x+5=0\" should be written as \"2*x+5=0\""    
    try:
        if "=" in expression:
                lhs_str, rhs_str = expression.split("=")
                lhs = sympify(lhs_str)
                rhs = sympify(rhs_str)
                equation = Eq(lhs, rhs)
                solution = solve(equation, symbols('x'))
                approxSolution = [sol.evalf() for sol in solution] # Convert the ugly CRootOf to numerical approximation :-)
                return approxSolution
        else:
                equation = sympify(expression)
                solution = solve(equation, symbols('x'))
                approxSolution = [sol.evalf() for sol in solution]
                return approxSolution     
    except: return msg


@tool
def install_oceanwave3d():
    """Builds a docker image with the OceanWave3D simulator"""
    try: # Test that docker is running
        subprocess.run('set -e; docker ps');
    except Exception as e:
        return "You must have docker installed and running in order to install OceanWave3D."
    
    # Install oceanwave
    try:
        res = subprocess.run(["bash", "./install_oceanwave3d.sh"], capture_output=True, shell=True)
        if res.stdout == None or res.stdout.decode() == "":
            return res.stderr.decode()
        return "Sucessfully installed the OceanWave3D program"
    except Exception as e:
        return str(e)

@tool
def run_oceanwave3d_simulation(input_file):
    """Run a simulation with the OceanWave3D tool."""
    if not os.path.isdir("OceanWave3D-Fortran90"):
        return "You need to install OceanWave3D before running the simulation"
    
    try: # Test that docker is running
        subprocess.run('set -e; docker ps');
    except Exception as e:
        return "You must have docker installed and running in order to install OceanWave3D."


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
    if not os.path.isdir("OceanWave3D-Fortran90"):
        return "You need to install OceanWave3D in order to display input files"

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