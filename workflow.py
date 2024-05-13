# workflow.py

import pandas as pd

def data_analysis_step(state):
    with NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(state['input_data'].encode('utf-8'))
        temp_file_path = temp_file.name

    loader = CSVLoader(file_path=temp_file_path)
    data = loader.load()
    df = pd.DataFrame([d.page_content.split("\n") for d in data], columns=[
        "Segment", "Country", "Product", "Discount Band", "Units Sold",
        "Manufacturing Price", "Sale Price", "Gross Sales", "Discounts",
        "Sales", "COGS", "Profit", "Date", "Month Number", "Month Name", "Year"
    ])
    agent, prompt = create_data_analysis_agent()
    analysis_result = agent.run(prompt.format_prompt(input=df).to_string())
    return {"analysis_result": analysis_result}