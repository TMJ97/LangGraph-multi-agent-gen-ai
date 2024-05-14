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

        df = pd.DataFrame([row.page_content.split(",") for row in data])
        df.columns = df.iloc[0]
        df = df[1:]

        print("Input DataFrame:")
        print(df.head())
        print(df.shape)
        
        agent, prompt = create_data_analysis_agent()
        try:
            analysis_result = agent.run(prompt.format_prompt(input=df).to_string())
            summary_prompt = f"""
            Based on your analysis of the DataFrame, please provide a summary of the key findings and insights. Include answers to the following questions:
            1. What are the total sales for each product?
            2. Which country has the highest number of units sold?
            3. How do the sales vary across different segments?
            """
            summary_result = agent.run(summary_prompt)
            final_result = f"Analysis Result:\n{analysis_result}\n\nSummary:\n{summary_result}"
        except Exception as e:
            final_result = f"An error occurred during analysis: {str(e)}"

        return {"analysis_result": final_result}

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