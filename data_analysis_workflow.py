from langchain.agents import AgentExecutor
from data_analysis_agents import create_data_analysis_agent

def run_data_analysis(df, input_question):
    data_analysis_agent = create_data_analysis_agent(df)
    return data_analysis_agent.run(input=input_question)