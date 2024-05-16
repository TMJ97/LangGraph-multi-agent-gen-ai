import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents.openai_assistant import OpenAIAssistantRunnable

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class CodeGenerationAgent(OpenAIAssistantRunnable):
    def __init__(self, assistant_id, model):
        super().__init__(assistant_id=assistant_id, model=model)

    def generate_code(self, state: dict) -> dict:
        summary = state.get("summary", "")
        code = f"Generated code based on summary: print('{summary}')"
        state["code"] = code
        print(f"Debug: CodeGenerationAgent state: {state}")  # Debugging print
        return state

if __name__ == "__main__":
    model = ChatOpenAI(api_key=openai_api_key, temperature=0)
    agent = CodeGenerationAgent(assistant_id="code_generation_agent", model=model)
    initial_state = {"summary": "Sample summary content"}
    response = agent.generate_code(initial_state)
    print(response)