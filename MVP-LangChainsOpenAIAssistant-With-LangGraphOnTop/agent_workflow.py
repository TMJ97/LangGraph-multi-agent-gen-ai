import os
from dotenv import load_dotenv
from data_analysis_agent import create_data_analysis_agent, analyze_data

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo"
temperature = 0.7

data_analysis_agent = create_data_analysis_agent(model_name=model_name, temperature=temperature)

initial_state = {
    "content": """date,revenue,expenses,profit
2023-01-01,10000,8000,2000
2023-02-01,12000,9000,3000
2023-03-01,11000,9500,1500
2023-04-01,13000,10000,3000
2023-05-01,15000,11000,4000"""
}

output = analyze_data(data_analysis_agent, initial_state)
print(f"Final output: {output}")