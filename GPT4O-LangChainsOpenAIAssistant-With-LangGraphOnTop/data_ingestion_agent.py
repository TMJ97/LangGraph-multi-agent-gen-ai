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

    def handle_file_upload(self, state: dict) -> dict:
        file_content = state.get("content", "")
        processed_content = f"File content received: {file_content[:100]}"  # Just a sample response
        state["processed_content"] = processed_content
        print(f"Debug: DataIngestionAgent state: {state}")  # Debugging print
        return state

if __name__ == "__main__":
    model = ChatOpenAI(api_key=openai_api_key, temperature=0)
    agent = DataIngestionAgent(assistant_id="data_ingestion_agent", model=model)
    initial_state = {"content": "Sample file content"}
    response = agent.handle_file_upload(initial_state)
    print(response)