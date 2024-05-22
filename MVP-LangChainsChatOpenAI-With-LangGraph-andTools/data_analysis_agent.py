import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from e2b_code_interpreter import CodeInterpreter
from langchain_core.tools import Tool
from langchain_core.messages import ToolMessage

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
e2b_api_key = os.getenv("E2B_API_KEY")

class CodeInterpreterTool:
    def __init__(self):
        self.code_interpreter = CodeInterpreter()

    def langchain_call(self, code: str):
        execution = self.code_interpreter.notebook.exec_cell(code)
        return {
            "results": execution.results,
            "stdout": execution.logs.stdout,
            "stderr": execution.logs.stderr,
            "error": execution.error,
        }

    def to_langchain_tool(self) -> Tool:
        return Tool(
            name="code_interpreter",
            description="Execute Python code in a Jupyter notebook cell and return results, stdout, stderr, and error.",
            func=self.langchain_call,
        )

def create_data_analysis_agent(model_name, temperature):
    code_interpreter_tool = CodeInterpreterTool()
    tools = [code_interpreter_tool.to_langchain_tool()]
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True
    )
    return agent

def analyze_data(agent, csv_data: str, instructions: str) -> dict:
    # Prompt the agent to perform data analysis
    analysis_prompt = f"""
Here is the CSV data:
{csv_data}

{instructions}

Please provide the Python code to perform the data analysis and generate insights and recommendations.
"""
    analysis_code = agent.run(input=analysis_prompt)

    # Execute the generated code using the code interpreter
    analysis_results = agent.run(input=analysis_code)

    return {"analysis_results": analysis_results}