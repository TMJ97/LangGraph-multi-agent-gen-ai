import os
from dotenv import load_dotenv
from data_analysis_agent import create_data_analysis_agent, analyze_data

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo"
temperature = 0.7

data_analysis_agent = create_data_analysis_agent(model_name=model_name, temperature=temperature)

initial_state = {
    "content": """
date,product,category,sales,revenue,profit_margin
2023-01-01,Product A,Category 1,100,5000,0.2
2023-01-02,Product B,Category 2,200,8000,0.25
2023-01-03,Product C,Category 1,150,7500,0.3
2023-01-04,Product A,Category 1,120,6000,0.2
2023-01-05,Product D,Category 3,80,4800,0.4
2023-01-06,Product B,Category 2,180,7200,0.25
2023-01-07,Product E,Category 3,90,5400,0.35
2023-01-08,Product C,Category 1,200,10000,0.3
2023-01-09,Product A,Category 1,110,5500,0.2
2023-01-10,Product D,Category 3,95,5700,0.4
"""
}

instructions = """
Please perform a complete data analysis on the provided dataset and generate the following:

1. Observations: Provide 5-10 key observations about the data, including patterns, trends, and any notable insights.

2. Insights: Discuss 3-5 meaningful insights derived from the data analysis, such as product performance, category-wise analysis, and profit margin analysis.

3. Recommendations: Based on the observations and insights, provide a paragraph with recommendations for improving sales, revenue, and profitability.

Please use the Python REPL tool to execute any necessary code for data analysis and visualization. Format your response with clear headings for Observations, Insights, and Recommendations.
"""

output = analyze_data(data_analysis_agent, initial_state, instructions)
print(f"Final output: {output}")