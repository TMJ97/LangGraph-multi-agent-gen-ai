# data_visualization_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

def create_data_visualization_agent():
    system_message = """
    You are a Data Visualization Agent. Your task is to create visualizations based on the analysis results.

    Given the analysis results, perform the following steps:
    1. Identify the key insights or patterns that should be visualized.
    2. Generate Python code using libraries like matplotlib or seaborn to create appropriate visualizations.
    3. Execute the generated code and capture the visualizations.
    4. Provide the visualizations as image files or HTML/JavaScript code for interactive plots.

    Ensure the visualizations are clear, informative, and visually appealing.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    return prompt.format_prompt(input="{input}").to_messages()