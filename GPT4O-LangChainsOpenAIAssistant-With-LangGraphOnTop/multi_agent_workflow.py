import os
from dotenv import load_dotenv
from langgraph.graph import MessageGraph, END
from langchain_core.messages import HumanMessage
from data_ingestion_agent import DataIngestionAgent
from analysis_agent import AnalysisAgent
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize models
model = ChatOpenAI(api_key=openai_api_key, temperature=0)

# Initialize agents
data_ingestion_agent = DataIngestionAgent(assistant_id="data_ingestion_agent", model=model)
analysis_agent = AnalysisAgent(assistant_id="analysis_agent", model=model)

# Create LangGraph workflow
graph = MessageGraph()

# Define nodes
graph.add_node("data_ingestion", data_ingestion_agent.handle_file_upload)
graph.add_node("analysis", analysis_agent.summarize_data)

# Define edges
graph.add_edge("data_ingestion", "analysis")
graph.add_edge("analysis", END)  # Adding the END node
graph.set_entry_point("data_ingestion")

# Compile and run the graph
runnable = graph.compile()

# Sample input
input_message = HumanMessage(content="Sample file content for data ingestion")

# Execute the workflow
output = runnable.invoke(input_message)
print(output)
