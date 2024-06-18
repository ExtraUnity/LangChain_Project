import os
from LLM.tools import *
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_fireworks import ChatFireworks
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
        