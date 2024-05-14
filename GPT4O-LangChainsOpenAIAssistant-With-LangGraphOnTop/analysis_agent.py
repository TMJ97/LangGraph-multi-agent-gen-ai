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

    def summarize_data(self, data: str) -> str:
        # Basic summarization logic
        return f"Summary of data: {data[:100]}"  # Just a sample response

if __name__ == "__main__":
    model = ChatOpenAI(api_key=openai_api_key, temperature=0)
    agent = AnalysisAgent(assistant_id="analysis_agent", model=model)
    response = agent.summarize_data("Sample data content")
    print(response)
