# reflection_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

def create_reflection_agent():
    system_message = """
    You are a Reflection Agent. Your task is to assess the performance of the other agents and provide feedback for improvement.

    Given the input data, the preprocessing steps, the analysis results, and the visualizations, perform the following steps:
    1. Evaluate the quality and effectiveness of each agent's output.
    2. Identify areas where the agents can improve their performance.
    3. Provide constructive feedback and suggestions for each agent.
    4. Assess the overall workflow and suggest any optimizations or modifications.

    Your feedback should be clear, specific, and actionable. Aim to help the agents enhance their capabilities and deliver better results.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    return prompt.format_prompt(input="{input}").to_messages()