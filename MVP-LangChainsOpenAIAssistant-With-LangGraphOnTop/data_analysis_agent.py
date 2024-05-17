import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def create_data_analysis_agent(model_name, temperature):
    return ChatOpenAI(model_name=model_name, temperature=temperature)

def analyze_data(agent, state: dict) -> dict:
    file_content = state.get("content", "")
    messages = [
        HumanMessage(content=f"Here is the CSV data:\n{file_content}\n\nPlease provide a detailed data analysis, including the step-by-step plan, code execution, insights, and recommendations.")
    ]
    analysis_results = agent(messages)
    state["analysis_results"] = analysis_results.content
    return state