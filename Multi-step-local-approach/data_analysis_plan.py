# data_analysis_plan.py

from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain

def create_data_analysis_plan_agent():
    system_message = """
    You are a Data Analysis Planning Agent. Your task is to create a comprehensive, step-by-step plan for analyzing a given dataset and generate the necessary Python code to perform the analysis.

    The dataset will be described to you, including the column names and data types. Based on this information, you should:
    1. Create a detailed, MECE (Mutually Exclusive, Collectively Exhaustive) plan for analyzing the dataset. Consider various aspects such as data cleaning, exploration, aggregation, visualization, and statistical analysis.
    2. Generate Python code using the pandas library to execute the analysis plan. The code should be well-structured, modular, and include appropriate comments.
    3. Provide the analysis plan and the generated Python code as your final output.

    Remember, you won't have access to the actual dataset. Your task is to create a robust analysis plan and code based on the dataset description provided.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    llm = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

def generate_data_analysis_plan(data_description):
    chain = create_data_analysis_plan_agent()
    try:
        analysis_plan_and_code = chain.run(data_description)
        if "error" in analysis_plan_and_code.lower():
            raise Exception(f"Model produced an error: {analysis_plan_and_code}")
        return analysis_plan_and_code
    except Exception as e:
        error_message = f"Error generating data analysis plan: {str(e)}"
        print(error_message)
        return error_message