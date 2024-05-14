# data_preprocessing_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

def create_data_preprocessing_agent():
    system_message = """
    You are a Data Preprocessing Agent. Your task is to clean and prepare the input data for analysis.
    
    Given a DataFrame, perform the following steps:
    1. Check for missing values and handle them appropriately (e.g., remove rows or fill with suitable values).
    2. Identify and handle outliers if necessary.
    3. Ensure the data types of each column are appropriate for analysis.
    4. Perform any necessary data transformations or feature engineering.

    Provide the preprocessed DataFrame as a CSV string in your response.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    return prompt.format_prompt(input="{input}").to_messages()