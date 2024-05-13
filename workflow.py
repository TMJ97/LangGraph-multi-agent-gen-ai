# workflow.py

from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
from data_analysis_agent import create_data_analysis_agent

class AgentState(TypedDict):
    input_data: str
    analysis_result: str

def run_workflow(input_data):
    workflow = StateGraph(AgentState)

    workflow.add_node("Data Analysis Agent", create_data_analysis_agent())
    workflow.add_edge("Data Analysis Agent", END)

    workflow.set_entry_point("Data Analysis Agent")

    compiled_workflow = workflow.compile()

    state = AgentState(
        input_data=input_data,
        analysis_result=""
    )

    result = compiled_workflow.invoke(state)
    return result