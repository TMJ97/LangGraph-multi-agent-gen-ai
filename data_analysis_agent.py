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
    1. Analyze the structure and content of the DataFrame. Use df.head() to view the first few rows, df.columns to view the column names, and df.shape to check the number of rows and columns.
    2. If needed, rename the columns to meaningful names using df.columns = ['new_name1', 'new_name2', ...].
    3. Identify relevant data analysis tasks based on the DataFrame.
    4. Generate Python code using the pandas library to perform the identified analysis tasks.
    5. Execute the generated code using the PythonREPL tool, referring to the DataFrame as 'df'.
    6. Provide a summary of the analysis results and key insights.

    Be dynamic and adaptable in your approach based on the specific input data provided.
    When using the PythonREPL tool, make sure to provide the code as a single string without any special formatting.
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
            description="A Python shell for executing Python code. Provide the code as a single string."
        )
    ]

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent, prompt