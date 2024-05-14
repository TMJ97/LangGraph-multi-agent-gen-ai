import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents.openai_assistant import OpenAIAssistantRunnable

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class DataIngestionAgent(OpenAIAssistantRunnable):
    def __init__(self, assistant_id, model):
        super().__init__(assistant_id=assistant_id, model=model)

    def handle_file_upload(self, file_content: str) -> str:
        # Basic data processing logic
        return f"File content received: {file_content[:100]}"  # Just a sample response

if __name__ == "__main__":
    model = ChatOpenAI(api_key=openai_api_key, temperature=0)
    agent = DataIngestionAgent(assistant_id="data_ingestion_agent", model=model)
    response = agent.handle_file_upload("Sample file content")
    print(response)
