# data_analysis_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

def create_data_analysis_agent():
    system_message = """
    You are a Data Analysis Agent. Your task is to provide insights and perform analysis on the input data.

    Given a DataFrame, perform the following steps:
    1. Understand the analysis requirements based on the user's input question.
    2. Generate a summary of the data, including the number of rows and columns, and the types of data in each column.
    3. Provide the total sum of a specific column if requested.

    Provide the analysis results in a clear and concise manner.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    llm = ChatOpenAI(temperature=0)
    return llm.create_agent(prompt)