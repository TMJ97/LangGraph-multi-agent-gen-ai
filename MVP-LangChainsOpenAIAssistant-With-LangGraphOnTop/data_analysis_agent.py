import os
from dotenv import load_dotenv
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.schema import messages_to_dict, messages_from_dict

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

def create_data_analysis_agent(assistant_id, model):
    return OpenAIAssistantRunnable(assistant_id=assistant_id, model=model, tools=[{"type": "code_interpreter"}])

def analyze_data(agent, state: dict) -> dict:
    file_content = state.get("content", "")
    analysis_results = agent.invoke({"content": f"Here is the CSV data:\n{file_content}\n\nPlease provide a detailed data analysis, including the step-by-step plan, code execution, insights, and recommendations. Make sure to execute the code using the Code Interpreter and return the code execution results."})
    state["analysis_results"] = analysis_results.content
    return state