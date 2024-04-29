from flask import Flask, render_template, request, jsonify, send_file
from typing import List, Dict
from dotenv import load_dotenv
import os
import logging
import pandas as pd
import tempfile
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_agent
from langgraph.agents import create_agent_executor
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_agent_executor

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
openai_api_key = os.getenv('OPENAI_API_KEY')

def create_agent_with_memory(name, task, tools):
    llm = ChatOpenAI(temperature=0) #(model_name="gpt-4", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = create_agent(
        name=name,
        task=task,
        tools=tools,
        llm=llm,
        memory=memory,
        #agent_type="openai-functions",
    )
    return agent

data_cleaning_planning_agent = create_agent_with_memory(
    name="Data Cleaning Planning Agent",
    task="Provide a comprehensive data cleaning plan based on the 'input_data', with detailed instrucitons. Update the 'cleaning_plan' attribute of the AgentState with the generated plan.",
    tools=[],
)

data_cleaning_reviewing_agent = create_agent_with_memory(
    name="Data Cleaning Reviewing Agent",
    task="Review and revise a comprehensive data cleaning plan ('cleaning_plan') for the 'input_data', with detailed instrucitons. Update the 'cleaning_plan' attribute of the AgentState with the improved plan.",
    tools=[],
)

data_cleaning_execution_agent = create_agent_with_memory(
    name="Data Cleaning Execution Agent",
    task="Carry out the data cleaning task ('cleaning_plan') on the 'input_data'. Update the 'cleaned_data' attribute of the AgentState with the cleaned data.",
    tools=[],
)

agent_executor = create_agent_executor(
    agents=[data_cleaning_planning_agent, data_cleaning_reviewing_agent, data_cleaning_execution_agent],
    llm=ChatOpenAI(temperature=0),
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

workflow.set_agent_executor(agent_executor)

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
