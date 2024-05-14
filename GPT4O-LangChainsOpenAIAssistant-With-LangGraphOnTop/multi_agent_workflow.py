import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from data_ingestion_agent import DataIngestionAgent
from analysis_agent import AnalysisAgent
from code_generation_agent import CodeGenerationAgent
from evaluation_agent import EvaluationAgent
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize models
model = ChatOpenAI(api_key=openai_api_key, temperature=0, model="gpt-3.5-turbo-0125")

# Initialize agents
data_ingestion_agent = DataIngestionAgent(assistant_id="data_ingestion_agent", model=model)
analysis_agent = AnalysisAgent(assistant_id="analysis_agent", model=model)
code_generation_agent = CodeGenerationAgent(assistant_id="code_generation_agent", model=model)
evaluation_agent = EvaluationAgent(assistant_id="evaluation_agent", model=model)

# Define state schema as a dictionary
state_schema = {
    "content": str,
    "processed_content": str,
    "summary": str,
    "code": str,
    "evaluation": str
}

# Create LangGraph workflow
graph = StateGraph(state_schema=state_schema)

# Define nodes
graph.add_node("data_ingestion", data_ingestion_agent.handle_file_upload)
graph.add_node("analysis", analysis_agent.summarize_data)
graph.add_node("code_generation", code_generation_agent.generate_code)
graph.add_node("evaluation", evaluation_agent.evaluate_results)

# Define edges
graph.add_edge("data_ingestion", "analysis")
graph.add_edge("analysis", "code_generation")
graph.add_edge("code_generation", "evaluation")
graph.add_edge("evaluation", END)  # Adding the END node
graph.set_entry_point("data_ingestion")

# Compile and run the graph
runnable = graph.compile()

# Sample input
initial_state = {"content": "Sample file content for data ingestion"}

# Execute the workflow
output = runnable.invoke(initial_state)
print(output)
