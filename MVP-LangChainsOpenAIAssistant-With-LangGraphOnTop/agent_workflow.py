import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from data_analysis_agent import DataAnalysisAgent
from langchain_openai import ChatOpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
model = "gpt-3.5-turbo-0125"

data_analysis_agent = DataAnalysisAgent(assistant_id=assistant_id, model=model)

state_schema = {
    "content": str,
    "analysis_results": str,
}

graph = StateGraph(state_schema=state_schema)

graph.add_node("data_analysis", data_analysis_agent.analyze_data)

graph.add_edge("data_analysis", END)
graph.set_entry_point("data_analysis")

runnable = graph.compile()

initial_state = {
    "content": """date,revenue,expenses,profit
2023-01-01,10000,8000,2000
2023-02-01,12000,9000,3000
2023-03-01,11000,9500,1500
2023-04-01,13000,10000,3000
2023-05-01,15000,11000,4000"""
}

output = runnable.invoke(initial_state)
print(f"Final output: {output}")