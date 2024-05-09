import sys
import pandas as pd
from langchain.schema import HumanMessage
from data_analysis_workflow import workflow

def process_data(input_data):
    processed_data = {
        "messages": [HumanMessage(content=f"Please analyze the following data:\n{input_data.to_string()}")],
        "sender": "User",
        "intermediate_steps": [],  # Add an empty list for intermediate_steps
    }
    return processed_data

def get_user_input_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python data_analysis_mvp.py <csv_file_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]

    # Get user input data
    input_data = get_user_input_data(csv_file_path)

    # Process the input data
    processed_data = process_data(input_data)

    # Run the workflow
    result = workflow.invoke(processed_data)

    # Print the summary and analysis
    print("Data Summary:")
    print(result["Data Summary Agent"].content)
    print("Data Analysis:")
    print(result["Data Analysis Agent"].content)

if __name__ == "__main__":
    main()