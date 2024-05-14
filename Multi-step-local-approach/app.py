# app.py

from flask import Flask, render_template, request, jsonify, send_file
from workflow import run_workflow
import subprocess
import os

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    uploaded_file = request.files['file']
    if uploaded_file:
        try:
            input_data = uploaded_file.read().decode('utf-8')
            result = run_workflow(input_data)

            # Run the generated code locally
            subprocess.run(["python", "generated_analysis_code.py"])

            # Load the analysis results from a file (assuming the generated code saves the results to a file)
            with open("analysis_results.txt", "r") as file:
                analysis_results = file.read()

            # Pass the analysis results to the agent for interpretation
            agent = create_data_analysis_interpretation_agent()
            interpreted_results = agent.run(analysis_results)

            return jsonify({'analysis_plan_and_code': result['analysis_plan_and_code'], 'interpreted_results': interpreted_results})
        except Exception as e:
            print(f"Error: {str(e)}")  # Add this line to log the error
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No file uploaded'}), 400
    
if __name__ == '__main__':
    app.run(debug=True)