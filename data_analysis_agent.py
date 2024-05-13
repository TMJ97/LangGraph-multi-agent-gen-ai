# data_analysis_agent.py

from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_experimental.utilities import PythonREPL

def create_data_analysis_agent():
    system_message = """
    You are a Data Analysis Agent. Your task is to provide insights and perform analysis on the input data.

    The input data will be provided as a pandas DataFrame called 'df'.

    To perform the analysis, follow these steps:
    1. Analyze the structure and content of the DataFrame.
    2. Identify relevant data analysis tasks based on the DataFrame.
    3. Generate Python code using the pandas library to perform the identified analysis tasks.
    4. Execute the generated code using the PythonREPL tool, referring to the DataFrame as 'df'.
    5. Provide a summary of the analysis results and key insights.

    Be dynamic and adaptable in your approach based on the specific input data provided.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    llm = ChatOpenAI(temperature=0)

    python_repl = PythonREPL()
    tools = [
        Tool(
            name="PythonREPL",
            func=python_repl.run,
            description="A Python shell for executing Python code."
        )
    ]

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent, prompt