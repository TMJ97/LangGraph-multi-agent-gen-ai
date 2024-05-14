# workflow.py

from langchain_community.document_loaders.csv_loader import CSVLoader
from typing_extensions import TypedDict
from data_analysis_plan import generate_data_analysis_plan
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

        df = pd.DataFrame([row.page_content.split(",") for row in data])
        df.columns = df.iloc[0]
        df = df[1:]

        data_description = f"""
        The dataset contains sales data with the following columns:
        {', '.join(df.columns)}

        The data types for each column are:
        {df.dtypes}
        """

        analysis_plan_and_code = generate_data_analysis_plan(data_description)

        # Save the generated code to a file
        with open("generated_analysis_code.py", "w") as file:
            file.write(analysis_plan_and_code)

        return {"analysis_plan_and_code": analysis_plan_and_code}

    workflow.add_node("Data Analysis Plan", data_analysis_step)
    workflow.add_edge("Data Analysis Plan", END)

    workflow.set_entry_point("Data Analysis Plan")

    compiled_workflow = workflow.compile()

    state = AgentState(
        input_data=input_data,
        analysis_result=""
    )

    result = compiled_workflow.invoke(state)
    return result