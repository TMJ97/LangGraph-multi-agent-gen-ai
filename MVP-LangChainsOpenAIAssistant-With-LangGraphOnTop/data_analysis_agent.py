import os
from dotenv import load_dotenv
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.schema import messages_to_dict, messages_from_dict

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

class DataAnalysisAgent(OpenAIAssistantRunnable):
    def __init__(self, assistant_id, model):
        super().__init__(assistant_id=assistant_id, model=model)

    def analyze_data(self, state: dict) -> dict:
        file_content = state.get("content", "")
        analysis_results = self.invoke({"content": f"Here is the CSV data:\n{file_content}\n\nPlease provide a detailed data analysis, including the step-by-step plan, code execution, insights, and recommendations."})
        state["analysis_results"] = analysis_results.content
        return state