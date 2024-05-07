from flask import Flask, render_template, request, jsonify, send_file
from typing import List, Any, Dict
from dotenv import load_dotenv
import os
import logging
import pandas as pd
import tempfile
import openai
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool, PythonREPL
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_core.utils.function_calling import format_tool_to_openai_function
from typing_extensions import TypedDict

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
openai_api_key = os.getenv('OPENAI_API_KEY')

class AgentState(TypedDict):
    messages: List[BaseMessage]
    input_data: pd.DataFrame
    cleaning_plan: str
    cleaned_data: pd.DataFrame

def create_agent(llm, system_message: str):
    """Create an agent."""
    prompt = ChatPromptTemplate.from_template(system_message)
    return prompt | llm

# Define the tools
python_repl = PythonREPL()
tools = [
    Tool(
        name="Python REPL",
        func=python_repl.run,
        description="A Python REPL (Read-Eval-Print Loop) to execute Python code. Use this to analyze data, write data cleaning scripts, or perform any other Python operations."
    )
]

data_cleaning_planning_agent = create_agent(
    llm=ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo-0125"),
    system_message="You are a Data Cleaning Planning Agent. Provide a comprehensive data cleaning plan based on the 'input_data', with detailed instructions. Update the 'cleaning_plan' attribute of the AgentState with the generated plan. You have access to a Python REPL tool to execute Python code and analyze the data."
)

data_cleaning_reviewing_agent = create_agent(
    llm=ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo-0125"),
    system_message="You are a Data Cleaning Reviewing Agent. Review and revise a comprehensive data cleaning plan ('cleaning_plan') for the 'input_data', with detailed instructions. Update the 'cleaning_plan' attribute of the AgentState with the improved plan. You have access to a Python REPL tool to execute Python code and analyze the data."
)

data_cleaning_execution_agent = create_agent(
    llm=ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo-0125"),
    system_message="You are a Data Cleaning Execution Agent. Carry out the data cleaning task ('cleaning_plan') on the 'input_data'. Update the 'cleaned_data' attribute of the AgentState with the cleaned data. You have access to a Python REPL tool to execute Python code and perform data cleaning operations."
)

workflow = StateGraph(AgentState)

workflow.add_node("Data Cleaning Planning Agent", data_cleaning_planning_agent)
workflow.add_node("Data Cleaning Reviewing Agent", data_cleaning_reviewing_agent)
workflow.add_node("Data Cleaning Execution Agent", data_cleaning_execution_agent)

workflow.add_edge("Data Cleaning Planning Agent", "Data Cleaning Reviewing Agent")
workflow.add_edge("Data Cleaning Reviewing Agent", "Data Cleaning Execution Agent")
workflow.add_edge("Data Cleaning Execution Agent", END)

workflow.set_entry_point("Data Cleaning Planning Agent")

compiled_workflow = workflow.compile()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    uploaded_file = request.files['file']
    if uploaded_file:
        try:
            # Read the uploaded file using pandas
            input_data_df = pd.read_excel(uploaded_file)

            state = AgentState(
                messages=[{"role": "user", "content": "Data cleaning request"}],
                input_data=input_data_df,
                cleaning_plan="",
                cleaned_data=pd.DataFrame()
            )
            logging.info(f"User uploaded file: {uploaded_file.filename}")
            response = compiled_workflow.invoke(state)
            logging.info(f"Agent response: {response.messages[-1].content}")

            agent_steps = []
            for message in response.messages[1:-1]:
                agent_steps.append(f"{message.role}: {message.content}")

            cleaned_data_df = response.cleaned_data

            # Save the cleaned data to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
                cleaned_data_df.to_csv(temp_file.name, index=False)
                download_filename = 'cleaned_data.csv'

            return jsonify({
                'response': str(response.messages[-1].content),
                'agent_steps': agent_steps,
                'download_url': f"/download/{temp_file.name}",
                'download_filename': download_filename
            }, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error during agent execution: {str(e)}")
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No file uploaded'})

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)