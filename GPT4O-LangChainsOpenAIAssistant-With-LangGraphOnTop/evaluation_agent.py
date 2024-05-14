import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents.openai_assistant import OpenAIAssistantRunnable

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class EvaluationAgent(OpenAIAssistantRunnable):
    def __init__(self, assistant_id, model):
        super().__init__(assistant_id=assistant_id, model=model)

    def evaluate_results(self, state: dict) -> dict:
        code = state.get("code", "")
        evaluation = f"Evaluation of code: {code[:100]}"  # Just a sample response
        state["evaluation"] = evaluation
        return state

if __name__ == "__main__":
    model = ChatOpenAI(api_key=openai_api_key, temperature=0)
    agent = EvaluationAgent(assistant_id="evaluation_agent", model=model)
    initial_state = {"code": "Sample code content"}
    response = agent.evaluate_results(initial_state)
    print(response)
