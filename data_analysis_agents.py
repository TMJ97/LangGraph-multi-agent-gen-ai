import os
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

def execute_python_code(code: str, df: pd.DataFrame) -> str:
    try:
        locals_dict = {'df': df, 'result': None}
        exec(code, globals(), locals_dict)
        if locals_dict['result'] is None:
            return "Error: No result was stored in the 'result' variable. Please make sure to store the final result in 'result'."
        return str(locals_dict['result'])
    except KeyError as e:
        return f"Error: The column '{str(e)}' does not exist in the dataset. Use the 'Dataset Columns' tool to check the available columns and try again with the correct column name."
    except Exception as e:
        return f"Error executing code: {str(e)}"

def create_data_analysis_agent(df, model_name="gpt-3.5-turbo-0613"):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model_name)

    tools = [
        Tool(
            name="Python REPL",
            func=lambda code: execute_python_code(code, df),
            description="A Python shell. Use this to execute Python code for data analysis and manipulation. The dataset is available as the 'df' variable. Store the result in the 'result' variable.",
        ),
        Tool(
            name="Dataset Columns",
            func=lambda _: ", ".join(df.columns),
            description="Returns the column names of the dataset. Use this to inspect the available columns before performing any operations.",
        ),
    ]

    system_message = """
    You are a data analysis agent. Your task is to provide insights and perform analysis on the input data.
    The dataset is available as a pandas DataFrame called 'df'.

    When using the Python REPL tool:
    - Store the final result in a variable called 'result'.
    - If a column name is not found in the dataset, use the 'Dataset Columns' tool to inspect the available columns and retry with the correct column name.

    Always use the 'Dataset Columns' tool to check the available columns before attempting any operations on the dataset.

    Provide the output in a clear and concise manner, focusing on the key insights and results.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, MessagesPlaceholder(variable_name="history"), human_message_prompt])

    agent = initialize_agent(tools, chat, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_prompt=prompt)

    return agent