from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
import pandas as pd
import subprocess
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)

def process_answer(answer):
    file_path = 'assets/Metrics.csv'
    df = pd.read_csv(file_path)
    df.rename(columns={'Metric ': 'Metric'}, inplace=True)
    metrics_list = df['Metric']
    metrics_string = ", ".join(metrics_list)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assessor to a question on a test, your job is to assign a score between 1 and 10 for each of the 40 metrics provided to you for an answer to a test question"},
            {"role": "user", "content": f"Given the following metrics: {metrics_string}. You are tasked with the job of assessing an applicant who answered the question with the answer: {answer}. In your response, don't give me any explanations, just provide me with each metric and the answer's score for each. separate each metric name and number with a : so i can deal with it easily in my code"}
        ]
    )

    print(completion)

    scores = completion.choices[0].message.content

    print(scores)

    lines = scores.strip().split("\n")
    scores_dict = dict(line.split(": ", 1) for line in lines)

    return scores_dict

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Uncomment these following two lines in order to process the user answer from the textarea element on site
    user_answer = request.json['answer'] 
    user_scores = process_answer(user_answer)

    # Run nnKDtree.py to get the result
    result = subprocess.check_output(['python', 'src/nnKDtree.py', json.dumps(user_scores)]).decode().strip()

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
