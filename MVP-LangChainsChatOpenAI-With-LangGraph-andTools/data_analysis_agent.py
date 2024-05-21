import os
import io
import sys
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

def analyze_data(agent, state: dict, instructions: str) -> dict:
    file_content = state.get("content", "")
    
    # Create the 'data.csv' file with the provided CSV data
    with open("data.csv", "w") as file:
        file.write(file_content)
    
    # Prompt the agent to generate the data analysis code
    code_generation_prompt = f"""
Please generate Python code to perform data analysis on the provided CSV data.
The data is stored in a file named 'data.csv'.
Use pandas or other relevant libraries to load and analyze the data.
Generate meaningful observations, insights, and recommendations based on the analysis.

Instructions:
{instructions}
"""
    
    # Generate the data analysis code using the agent
    data_analysis_code = agent.run(code_generation_prompt)
    
    # Save the generated code to a file
    with open("analysis_script.py", "w") as file:
        file.write(data_analysis_code)
    
    # Execute the generated code and capture the output
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    exec(data_analysis_code)
    script_output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    # Get the agent's response based on the script output
    analysis_results = agent.run(f"Please review the following output from the data analysis and provide a summary of the observations, insights, and recommendations:\n\n{script_output}")
    state["analysis_results"] = analysis_results
    return state