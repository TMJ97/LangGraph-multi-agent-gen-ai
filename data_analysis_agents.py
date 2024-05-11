import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

def create_agent(system_message, model_name="gpt-3.5-turbo-0125"):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model_name)

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")
    prompt = ChatPromptTemplate.from_messages([system_message_prompt, MessagesPlaceholder(variable_name="history"), human_message_prompt])

    agent = initialize_agent([], chat, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_prompt=prompt)

    return agent

data_summary_agent = create_agent("You are a data summary agent. Your task is to provide a concise summary of the input data.")
data_analysis_agent = create_agent("You are a data analysis agent. Your task is to provide insights and perform analysis on the input data.")