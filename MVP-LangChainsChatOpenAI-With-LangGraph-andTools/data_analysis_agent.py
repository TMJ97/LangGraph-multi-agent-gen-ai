import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_experimental.utilities import PythonREPL

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def create_data_analysis_agent(model_name, temperature):
    python_repl = PythonREPL()
    tools = [
        Tool(
            name="Python REPL",
            func=python_repl.run,
            description="A Python shell. Use this to execute Python code."
        )
    ]
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True
    )
    return agent

def analyze_data(agent, state: dict) -> dict:
    file_content = state.get("content", "")
    
    # Create the 'data.csv' file with the provided CSV data
    with open("data.csv", "w") as file:
        file.write(file_content)
    
    code_snippet = """
import pandas as pd

df = pd.read_csv('data.csv')
print(df.head())
    """
    analysis_results = agent.run(f"Please execute the following code using the Python REPL tool:\n{code_snippet}")
    state["analysis_results"] = analysis_results
    return state