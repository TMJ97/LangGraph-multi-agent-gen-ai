from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

openai_api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json['message']
    # TODO: Process the message and generate a response using the multi-agent workflow
    response = "Sample response"
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)