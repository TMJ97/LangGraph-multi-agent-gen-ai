import tempfile
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from data_analysis_agents import create_data_analysis_agent

def run_data_analysis(df, input_question):
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_file_path = f"{temp_dir}/data.csv"
        df.to_csv(csv_file_path, index=False)

        messages = create_data_analysis_agent(csv_file_path)
        messages.append(HumanMessage(content=input_question))

        chat = ChatOpenAI(temperature=0)
        response = chat.generate([messages]).generations[0][0].text

        # Extract the Python code block from the response
        code_start = response.find("```python")
        code_end = response.find("```", code_start + 1)

        if code_start != -1 and code_end != -1:
            code_block = response[code_start + 9:code_end].strip()

            # Execute the generated Python code
            locals_dict = {}
            try:
                exec(code_block, {}, locals_dict)
                result = locals_dict.get("result", "")
            except KeyError as e:
                result = f"Error: The column '{str(e)}' does not exist in the dataset."
            except Exception as e:
                result = f"Error executing code: {str(e)}"
        else:
            result = "Error: Could not find a valid Python code block in the agent's response."

    return result