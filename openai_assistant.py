import openai
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent

def create_openai_assistant(model_name="gpt-3.5-turbo-0125"):
    llm = ChatOpenAI(model_name=model_name)  # Use ChatOpenAI from langchain_openai
    tools = [{"type": "code_interpreter"}]
    agent = create_openai_functions_agent(llm, tools)
    return AgentExecutor.from_agent_and_tools(agent, tools)

def execute_data_cleaning(openai_assistant, agent_state):
    cleaning_plan = agent_state.cleaning_plan
    input_data = agent_state.input_data

    # Execute the cleaning plan using the OpenAI Assistant
    result = openai_assistant.run({
        "input": f"Input data: {input_data.to_dict(orient='records')}\n\nCleaning plan: {cleaning_plan}",
        "agent_scratchpad": True,
    })

    # Update the cleaned_data attribute of the AgentState
    cleaned_data = pd.DataFrame(result.get("result", {}))
    agent_state.cleaned_data = cleaned_data

    return agent_state