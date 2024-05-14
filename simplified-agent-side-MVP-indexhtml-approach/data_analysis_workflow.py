from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document, HumanMessage
from langchain_community.document_loaders.csv_loader import CSVLoader
from data_analysis_agents import create_data_analysis_agent

def run_data_analysis(df, input_question):
    # Convert DataFrame to CSV string
    csv_string = df.to_csv(index=False)

    # Load CSV data using CSVLoader
    loader = CSVLoader(file_path=None, csv_str=csv_string)
    documents = loader.load()

    # Create a formatted string representation of the documents
    formatted_docs = "\n".join([f"Document {i+1}:\n{doc.page_content}\n" for i, doc in enumerate(documents)])

    messages = create_data_analysis_agent("")
    messages.append(HumanMessage(content=f"Data:\n{formatted_docs}\n\nQuestion: {input_question}"))

    chat = ChatOpenAI(temperature=0)
    response = chat.generate([messages]).generations[0][0].text

    # Extract the Python code block from the response
    code_start = response.find("```python")
    code_end = response.find("```", code_start + 1)

    if code_start != -1 and code_end != -1:
        code_block = response[code_start + 9:code_end].strip()

        # Execute the generated Python code
        locals_dict = {"documents": documents}
        try:
            exec(code_block, {}, locals_dict)
            result = locals_dict.get("result", "")
        except KeyError as e:
            result = f"Error: The key '{str(e)}' does not exist in the data."
        except Exception as e:
            result = f"Error executing code: {str(e)}"
    else:
        result = "Error: Could not find a valid Python code block in the agent's response."

    return result