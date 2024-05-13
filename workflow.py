# workflow.py

from langchain_community.document_loaders.csv_loader import CSVLoader
from typing_extensions import TypedDict
from data_analysis_agent import create_data_analysis_agent
from tempfile import NamedTemporaryFile
import pandas as pd
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    input_data: str
    analysis_result: str

def run_workflow(input_data):
    workflow = StateGraph(AgentState)

    def data_analysis_step(state):
        with NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(state['input_data'].encode('utf-8'))
            temp_file_path = temp_file.name

        loader = CSVLoader(file_path=temp_file_path)
        data = loader.load()

        data_dicts = [
            {
                key: value
                for key, value in zip(row.split(","), row.split(","))
            }
            for row in [d.page_content for d in data]
        ]

        df = pd.DataFrame(data_dicts)

        agent, prompt = create_data_analysis_agent()
        try:
            analysis_result = agent.run(prompt.format_prompt(input=df).to_string())
        except Exception as e:
            analysis_result = f"An error occurred during analysis: {str(e)}"

        return {"analysis_result": analysis_result}

    workflow.add_node("Data Analysis Agent", data_analysis_step)
    workflow.add_edge("Data Analysis Agent", END)

    workflow.set_entry_point("Data Analysis Agent")

    compiled_workflow = workflow.compile()

    state = AgentState(
        input_data=input_data,
        analysis_result=""
    )

    result = compiled_workflow.invoke(state)
    return result["analysis_result"]