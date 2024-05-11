from langchain.agents import AgentExecutor
from data_analysis_agents import data_summary_agent, data_analysis_agent

def run_data_summary(input_data):
    return data_summary_agent.run(input_data)

def run_data_analysis(input_data):
    return data_analysis_agent.run(input_data)