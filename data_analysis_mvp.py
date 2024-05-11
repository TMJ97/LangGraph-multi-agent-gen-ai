import sys
import pandas as pd
from data_analysis_workflow import run_data_summary, run_data_analysis

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
    input_data = get_user_input_data(csv_file_path)

    print("Running data summary...")
    summary_result = run_data_summary(input_data.to_string())
    print("Data Summary:")
    print(summary_result)

    print("Running data analysis...")
    analysis_result = run_data_analysis(input_data.to_string())
    print("Data Analysis:")
    print(analysis_result)

if __name__ == "__main__":
    main()