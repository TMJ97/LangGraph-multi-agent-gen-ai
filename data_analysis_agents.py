import os
import functools
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent

load_dotenv()  # Load environment variables from .env file

def create_agent(llm, tools, system_message):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
            MessagesPlaceholder(variable_name="intermediate_steps"),
        ]
    )
    agent = create_openai_functions_agent(llm, tools, prompt=prompt)
    return agent

def agent_node(state, agent, name):
    result = agent.invoke({
        "agent_scratchpad": "",
        "intermediate_steps": state["messages"]
    })
    result = HumanMessage(content=result.content, additional_kwargs={"name": name})
    return {
        "messages": [result],
        "sender": name,
    }

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", openai_api_key=openai_api_key)

# Data Summary Agent
data_summary_agent = create_agent(
    llm,
    [],
    system_message="You are a data summary agent. Your task is to provide a concise summary of the input data.",
)
data_summary_node = functools.partial(agent_node, agent=data_summary_agent, name="Data Summary Agent")

# Data Analysis Agent
data_analysis_agent = create_agent(
    llm,
    [],
    system_message="You are a data analysis agent. Your task is to provide insights and perform analysis on the input data.",
)
data_analysis_node = functools.partial(agent_node, agent=data_analysis_agent, name="Data Analysis Agent")