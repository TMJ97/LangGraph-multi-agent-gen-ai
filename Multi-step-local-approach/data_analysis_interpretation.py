# data_analysis_interpretation.py

from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

def create_data_analysis_interpretation_agent():
    system_message = """
    You are a Data Analysis Interpretation Agent. Your task is to interpret the results of a data analysis and provide insights and recommendations based on the findings.

    The analysis results will be provided to you. Based on this information, you should:
    1. Review the analysis results and identify key insights and patterns.
    2. Provide a summary of the main findings and their implications.
    3. Offer recommendations or suggestions based on the analysis results.
    4. Present the insights and recommendations in a clear and concise manner, using bullet points or numbered lists.

    Your goal is to help stakeholders understand the outcomes of the data analysis and guide them in making data-driven decisions.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    llm = ChatOpenAI(temperature=0)
    agent = initialize_agent([], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent, prompt