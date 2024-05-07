from flask import Flask, render_template, request, jsonify, send_file
from typing import List
from dotenv import load_dotenv
import os
import logging
import pandas as pd
import tempfile
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langchain_core.utils.function_calling import format_tool_to_openai_function

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
openai_api_key = os.getenv('OPENAI_API_KEY')

def create_agent(llm, tools, system_message: str):
    """Create an agent."""
    functions = [format_tool_to_openai_function(t) for t in tools]
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="messages"),
    ])
    return prompt | llm.bind_functions(functions)

data_cleaning_planning_agent = create_agent(
    llm=ChatOpenAI(temperature=1),
    tools=[],
    system_message="You are a Data Cleaning Planning Agent. Provide a comprehensive data cleaning plan based on the 'input_data', with detailed instructions. Update the 'cleaning_plan' attribute of the AgentState with the generated plan."
)

data_cleaning_reviewing_agent = create_agent(
    llm=ChatOpenAI(temperature=1),
    tools=[],
    system_message="You are a Data Cleaning Reviewing Agent. Review and revise a comprehensive data cleaning plan ('cleaning_plan') for the 'input_data', with detailed instructions. Update the 'cleaning_plan' attribute of the AgentState with the improved plan."
)

data_cleaning_execution_agent = create_agent(
    llm=ChatOpenAI(temperature=1),
    tools=[],
    system_message="You are a Data Cleaning Execution Agent. Carry out the data cleaning task ('cleaning_plan') on the 'input_data'. Update the 'cleaned_data' attribute of the AgentState with the cleaned data."
)

class AgentState:
    messages: List[BaseMessage] = []
    input_data: str = ""
    cleaning_plan: str = ""
    cleaned_data: str = ""

workflow = StateGraph(AgentState)

workflow.add_node("Data Cleaning Planning Agent", data_cleaning_planning_agent)
workflow.add_node("Data Cleaning Reviewing Agent", data_cleaning_reviewing_agent)
workflow.add_node("Data Cleaning Execution Agent", data_cleaning_execution_agent)

workflow.add_edge("Data Cleaning Planning Agent", "Data Cleaning Reviewing Agent")
workflow.add_edge("Data Cleaning Reviewing Agent", "Data Cleaning Execution Agent")
workflow.add_edge("Data Cleaning Execution Agent", END)

workflow.set_entry_point("Data Cleaning Planning Agent")  # Set the entry point

workflow.compile()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    uploaded_file = request.files['file']
    if uploaded_file:
        # Read the uploaded file using pandas
        df = pd.read_excel(uploaded_file)
        input_data = df.to_json(orient='records')

        state = AgentState(messages=[{"role": "user", "content": "Data cleaning request"}], input_data=input_data)
        logging.info(f"User uploaded file: {uploaded_file.filename}")
        response = workflow.run(state)
        logging.info(f"Agent response: {response.messages[-1].content}")

        agent_steps = []
        for message in response.messages[1:-1]:
            agent_steps.append(f"{message.role}: {message.content}")

        cleaned_data = response.cleaned_data
        cleaned_df = pd.read_json(cleaned_data)

        # Save the cleaned data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            cleaned_df.to_csv(temp_file.name, index=False)
            download_filename = 'cleaned_data.csv'

        return jsonify({
            'response': response.messages[-1].content,
            'agent_steps': agent_steps,
            'download_url': f"/download/{temp_file.name}",
            'download_filename': download_filename
        })
    else:
        return jsonify({'error': 'No file uploaded'})

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)