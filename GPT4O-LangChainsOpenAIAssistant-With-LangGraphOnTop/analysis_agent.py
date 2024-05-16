import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents.openai_assistant import OpenAIAssistantRunnable

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class AnalysisAgent(OpenAIAssistantRunnable):
    def __init__(self, assistant_id, model):
        super().__init__(assistant_id=assistant_id, model=model)

    def summarize_data(self, state: dict) -> dict:
        processed_content = state.get("processed_content", "")
        summary = f"Summary of data: This is a summary of the processed content - {processed_content}"
        state["summary"] = summary
        print(f"Debug: AnalysisAgent state: {state}")  # Debugging print
        return state

if __name__ == "__main__":
    model = ChatOpenAI(api_key=openai_api_key, temperature=0)
    agent = AnalysisAgent(assistant_id="analysis_agent", model=model)
    initial_state = {"processed_content": "Sample processed content"}
    response = agent.summarize_data(initial_state)
    print(response)