# app.py

from flask import Flask, render_template, request, jsonify, send_file
from workflow import run_workflow
from data_analysis_interpretation import create_data_analysis_interpretation_agent
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

            # Save the generated code to a file
            with open("generated_analysis_code.py", "w") as file:
                file.write(result['analysis_plan_and_code'])

            # Run the generated code locally
            try:
                subprocess.run(["python", "generated_analysis_code.py"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running generated analysis code: {str(e)}")
                return jsonify({'error': f"Error running generated analysis code: {str(e)}"}), 500

            # Load the analysis results from a file (assuming the generated code saves the results to a file)
            try:
                with open("analysis_results.txt", "r") as file:
                    analysis_results = file.read()
            except FileNotFoundError as e:
                print(f"Error loading analysis results: {str(e)}")
                return jsonify({'error': f"Error loading analysis results: {str(e)}"}), 500

            # Pass the analysis results to the agent for interpretation
            agent = create_data_analysis_interpretation_agent()
            interpreted_results = agent.run(analysis_results)

            return jsonify({'analysis_plan_and_code': result['analysis_plan_and_code'], 'interpreted_results': interpreted_results})
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No file uploaded'}), 400
    
if __name__ == '__main__':
    app.run(debug=True)