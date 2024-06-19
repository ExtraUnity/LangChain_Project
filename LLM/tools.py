import os
import subprocess
from typing import Type
from langchain.tools import tool
from langchain_core.tools import tool, BaseTool
from langchain.pydantic_v1 import BaseModel
from pydantic import BaseModel, Field, ValidationError
from sympy import *
from langchain_community.utilities import OpenWeatherMapAPIWrapper
import matlab.engine


######################################################
# Agent Tools
######################################################
# This function is made by Christian
def find_index(search_string, string_list):
    for i, s in enumerate(string_list):
        if search_string in s:
            return i
    return -1  # return -1 if the string is not found

# This class is made by Christian
class ChangeInputFileInput(BaseModel):
    input_file: str = Field(description="Should be a file name")
    variable: str = Field(description="Variable name")
    new_value: str = Field(description="Should be a number")

# This class is made by Christian
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

                if "\n" not in line:
                    line += "\n"
                file.write(line)
        return "File has been updated."


# This function is made by Christian
@tool
def visualize_output():
    """Visualize output of the OceanWave3D simulation given by the input_file"""
    eng = matlab.engine.start_matlab()
    #output_path = os.path.dirname(__file__) + "../../OceanWave3D-Fortran90/docker/data"
    eng.ShowFreeSurfaceEvolution2D(nargout=0)
    return "Final answer: The output has been plotted"

# This function is made by Nikolaj
@tool
def mathematics(expression):
    """Evaluates a mathematical arithmetic expression and outputs it in string form."""
    return sympify(expression)

# This function is made by Nikolaj
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

# This function is made by Christian
@tool
def install_oceanwave3d():
    """Builds a docker image with the OceanWave3D simulator"""
    r = subprocess.run(["bash", "./test_docker.sh"], capture_output=True, shell=True) # Check that docker is installed and running
    if r.returncode != 0:
        return "You must have docker installed and running in order to install OceanWave3D."
    
    # Install oceanwave
    try:
        res = subprocess.run(["bash", "./install_oceanwave3d.sh"], capture_output=True, shell=True)
        if res.stdout == None or res.stdout.decode() == "":
            return res.stderr.decode()
        return "Sucessfully installed the OceanWave3D program"
    except Exception as e:
        return str(e)

# This function is made by Christian
@tool
def run_oceanwave3d_simulation(input_file):
    """Run a simulation with the OceanWave3D tool."""
    if not os.path.isdir("OceanWave3D-Fortran90"):
        return "You need to install OceanWave3D before running the simulation"
    
    r = subprocess.run(["bash", "./test_docker.sh"], capture_output=True, shell=True) # Check that docker is installed and running
    if r.returncode != 0:
        return "You must have docker installed and running in order to install OceanWave3D."


    try:
        res = subprocess.run(["bash", "./run_simulation.sh", input_file], capture_output=True)
        if res.stdout == None or res.stdout.decode() == "":
            return res.stderr.decode()
        return res.stdout.decode()
    except Exception as e:
        return str(e)


# This function is made by Christian
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
        
# This function is made by Nikolaj
@tool
def get_weather_info(city: str, country: str):
    """Get the weather information"""
    os.environ["OPENWEATHERMAP_API_KEY"] =  "a15039154ac226a73909c312586ea4c8"
    weather = OpenWeatherMapAPIWrapper()
    weather_data = weather.run(f"{city},{country}")
    return weather_data