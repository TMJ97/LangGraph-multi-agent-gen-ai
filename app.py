# app.py

from flask import Flask, render_template, request, jsonify, send_file
from workflow import run_workflow

app = Flask(__name__)

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
            return jsonify({'analysis_result': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(debug=True)