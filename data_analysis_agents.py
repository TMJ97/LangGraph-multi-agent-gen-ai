import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

load_dotenv()

def create_data_analysis_agent(csv_file_path, model_name="gpt-3.5-turbo-0613"):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model_name)

    system_message = f"""
    You are a data analysis agent. Your task is to provide insights and perform analysis on the input data.
    The dataset is available as a CSV file at the following path: '{csv_file_path}'.

    To complete the data analysis task, generate Python code that does the following:
    1. Imports the necessary libraries (e.g., pandas).
    2. Loads the CSV file into a DataFrame.
    3. Performs the required analysis on the DataFrame.
    4. Prints the results using the `print()` function.

    If a column or data is not found in the DataFrame, handle the error gracefully and provide an informative message.
    Do not make assumptions about the column names or the data structure.

    Provide the generated Python code as a string in your response, enclosed in triple backticks (```).
    Do not execute the code yourself.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    return prompt.format_prompt(input="{input}").to_messages()