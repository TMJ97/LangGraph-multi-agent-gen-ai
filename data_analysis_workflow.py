import operator
from typing import Annotated, List, Sequence, TypedDict
from langchain.schema import BaseMessage
from langgraph.graph import StateGraph, END
from data_analysis_agents import data_summary_node, data_analysis_node

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str

# Define the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("Data Summary Agent", data_summary_node)
graph.add_node("Data Analysis Agent", data_analysis_node)

# Set the entry point
graph.set_entry_point("Data Summary Agent")

# Add edges
graph.add_edge("Data Summary Agent", "Data Analysis Agent")
graph.add_edge("Data Analysis Agent", END)

# Compile the graph
workflow = graph.compile()